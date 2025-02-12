import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from langchain_openai.chat_models.base import BaseChatOpenAI
from langchain.callbacks.base import BaseCallbackHandler
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.memory import BaseMemory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# 加载环境变量
load_dotenv()

class OutputFormat(Enum):
    """输出格式枚举类"""
    MARKDOWN = "markdown"
    JSON = "json"
    TXT = "txt"
    HTML = "html"

@dataclass
class ConversationConfig:
    """对话配置数据类"""
    model_name: str = "qwen-plus"
    temperature: float = 0.0
    max_tokens: int = 1024
    streaming: bool = True
    output_dir: str = "output"
    output_format: OutputFormat = OutputFormat.MARKDOWN
    system_prompt: str = "你是一个专业的AI助手，请基于历史上下文（如果有）简单回答问题。"
    api_base: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    api_key_env: str = "DASHSCOPE_API_KEY"  # 环境变量名称
    log_level: int = logging.INFO
    save_interval: int = 5  # 每多少轮对话自动保存一次
    max_history_length: int = 50  # 最大历史记录长度
    backup_enabled: bool = True
    session_id_prefix: str = "session"  # 会话ID前缀
    questions_file: str = ""  # 问题文件路径
    markdown_template: str = """
# {title}

## 会话ID: {session_id}
开始时间: {start_time}
结束时间: {end_time}

{content}
"""

class ConversationOutputHandler(BaseCallbackHandler):
    """增强的对话输出处理器"""
    
    def __init__(self, output_format: OutputFormat, output_path: str):
        self.output_format = output_format
        self.output_path = output_path
        self.current_content = []
        self.ensure_output_dir()
        self.initialize_output_file()
        
    def ensure_output_dir(self):
        """确保输出目录存在"""
        Path(os.path.dirname(self.output_path)).mkdir(parents=True, exist_ok=True)
        
    def initialize_output_file(self):
        """初始化输出文件"""
        header = {
            OutputFormat.MARKDOWN: "# AI对话记录\n\n",
            OutputFormat.HTML: "<html><head><title>AI对话记录</title></head><body><h1>AI对话记录</h1>",
            OutputFormat.TXT: "=== AI对话记录 ===\n\n",
            OutputFormat.JSON: "[]"
        }
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(header.get(self.output_format, ""))
            
    def on_llm_new_token(self, token: str, **kwargs):
        """处理新token"""
        self.current_content.append(token)
        print(token, end='', flush=True)
        
    def format_content(self, problem: str, response: str, metadata: dict) -> str:
        """根据不同格式格式化内容"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if self.output_format == OutputFormat.MARKDOWN:
            return (f"\n## 问题 {metadata['number']} - {timestamp}\n\n"
                   f"### 问题描述：\n{problem}\n\n"
                   f"### 回答：\n{response}\n\n---\n")
        elif self.output_format == OutputFormat.HTML:
            return (f"<div class='qa-pair'>"
                   f"<h2>问题 {metadata['number']} - {timestamp}</h2>"
                   f"<h3>问题描述：</h3><p>{problem}</p>"
                   f"<h3>回答：</h3><p>{response}</p>"
                   f"<hr></div>")
        elif self.output_format == OutputFormat.JSON:
            return json.dumps({
                "number": metadata['number'],
                "timestamp": timestamp,
                "problem": problem,
                "response": response,
                "metadata": metadata
            }, ensure_ascii=False)
        else:
            return f"\n=== 问题 {metadata['number']} - {timestamp} ===\n" \
                   f"问题：{problem}\n回答：{response}\n\n"

class EnhancedMemory(BaseMemory, BaseModel):
    """增强的对话记忆系统"""
    
    chat_history: ChatMessageHistory = Field(default_factory=ChatMessageHistory)
    max_history_length: int = Field(default=50)
    memory_key: str = Field(default="chat_history")
    
    @property
    def memory_variables(self) -> List[str]:
        return [self.memory_key]
        
    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        return {self.memory_key: self.chat_history.messages}
        
    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        if len(self.chat_history.messages) >= self.max_history_length:
            half_length = self.max_history_length // 2
            self.chat_history.messages = self.chat_history.messages[-half_length:]
            
        if inputs.get("problem"):
            self.chat_history.add_user_message(inputs["problem"])
        if outputs.get("text"):
            self.chat_history.add_ai_message(outputs["text"])
            
    def clear(self) -> None:
        self.chat_history.clear()

class QuestionSession:
    """问题会话类，用于管理相关问题组"""
    
    def __init__(self, session_id: str, questions: List[str], title: str = None):
        self.session_id = session_id
        self.questions = questions
        self.title = title or f"问题会话 {session_id}"
        self.start_time = None
        self.end_time = None
        self.content = []

class AIConversationManager:
    """AI对话管理器"""
    
    def __init__(self, config: ConversationConfig = None):
        self.config = config or ConversationConfig()
        self.setup_logging()
        self.memory = EnhancedMemory()
        self.conversation_count = 0
        self.output_handler = self._create_output_handler()
        self.llm = self._setup_llm()
        self.prompt_template = self._create_prompt_template()
        self.sessions = {}  # 存储多个会话
        self.current_session_id = None
        
    def setup_logging(self):
        """配置日志系统"""
        # 确保日志目录存在
        os.makedirs(self.config.output_dir, exist_ok=True)
        
        logging.basicConfig(
            level=self.config.log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"{self.config.output_dir}/conversation.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def _create_output_handler(self) -> ConversationOutputHandler:
        """创建输出处理器"""
        output_path = os.path.join(
            self.config.output_dir,
            f"conversation.{self.config.output_format.value}"
        )
        return ConversationOutputHandler(self.config.output_format, output_path)
        
    def _setup_llm(self) -> BaseChatOpenAI:
        """设置语言模型"""
        api_key = os.getenv(self.config.api_key_env)
        if not api_key:
            raise ValueError(f"API key not found in environment variable: {self.config.api_key_env}")
            
        return BaseChatOpenAI(
            model=self.config.model_name,
            openai_api_key=api_key,
            openai_api_base=self.config.api_base,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            streaming=self.config.streaming,
            callbacks=[self.output_handler, StreamingStdOutCallbackHandler()]
        )
        
    def _create_prompt_template(self) -> ChatPromptTemplate:
        """创建提示模板"""
        return ChatPromptTemplate.from_messages([
            ("system", self.config.system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{problem}")
        ])
        
    def process_conversation(self, problem: str, metadata: dict = None) -> str:
        """处理对话"""
        try:
            self.conversation_count += 1
            metadata = metadata or {}
            metadata['number'] = self.conversation_count
            
            self.logger.info(f"Processing conversation {self.conversation_count}: {problem[:100]}...")
            
            # 创建对话链
            chain = self.prompt_template | self.llm
            
            # 执行对话并直接获取内容
            response = chain.invoke({
                "problem": problem,
                "chat_history": self.memory.chat_history.messages
            })
            
            # 获取实际的响应内容
            content = response.content if hasattr(response, 'content') else str(response)
            
            # 保存对话内容
            self.memory.save_context({"problem": problem}, {"text": content})
            
            # 格式化并保存输出
            formatted_content = self.output_handler.format_content(
                problem, content, metadata
            )
            
            with open(self.output_handler.output_path, 'a', encoding='utf-8') as f:
                f.write(formatted_content)
                
            # 自动保存和备份
            if self.conversation_count % self.config.save_interval == 0:
                self.save_history()
                if self.config.backup_enabled:
                    self.create_backup()
                    
            return content
            
        except Exception as e:
            self.logger.error(f"Error processing conversation: {str(e)}", exc_info=True)
            raise
            
    def save_history(self, filename: str = None):
        """保存对话历史"""
        if not filename:
            filename = f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
        filepath = os.path.join(self.config.output_dir, filename)
        history = self.get_chat_history()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
            
        self.logger.info(f"Chat history saved to {filepath}")
        
    def create_backup(self):
        """创建备份"""
        backup_dir = os.path.join(self.config.output_dir, "backups")
        Path(backup_dir).mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(
            backup_dir,
            f"conversation_backup_{timestamp}.{self.config.output_format.value}"
        )
        
        # 复制当前输出文件作为备份
        import shutil
        shutil.copy2(self.output_handler.output_path, backup_path)
        self.logger.info(f"Backup created at {backup_path}")
        
    def get_chat_history(self) -> List[Dict[str, str]]:
        """获取对话历史"""
        return [{
            "role": "user" if isinstance(msg, HumanMessage) else
                   "assistant" if isinstance(msg, AIMessage) else
                   "system" if isinstance(msg, SystemMessage) else "unknown",
            "content": msg.content
        } for msg in self.memory.chat_history.messages]
        
    def clear_history(self):
        """清空历史记录"""
        self.memory.clear()
        self.logger.info("Chat history cleared")

    def create_session(self, questions: List[str], session_id: str = None, title: str = None) -> str:
        """创建新的问题会话"""
        if session_id is None:
            session_id = f"{self.config.session_id_prefix}_{len(self.sessions) + 1}"
        
        self.sessions[session_id] = QuestionSession(session_id, questions, title)
        return session_id
        
    def load_questions_from_file(self, file_path: str) -> List[Dict[str, Any]]:
        """从文件加载问题
        支持的格式：
        1. 纯文本文件：每行一个问题
        2. JSON文件：支持多种格式：
           - 简单列表格式
           - 单个会话字典格式
           - 多会话嵌套字典格式
        """
        if file_path.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                sessions_data = []
                
                # 处理嵌套字典格式
                if isinstance(data, dict):
                    for session_id, session_info in data.items():
                        if isinstance(session_info, dict):
                            # 处理完整的会话信息
                            sessions_data.append({
                                "session_id": session_id,
                                "title": session_info.get("title", f"Session {session_id}"),
                                "questions": session_info.get("questions", [])
                            })
                        elif isinstance(session_info, list):
                            # 处理简单的问题列表
                            sessions_data.append({
                                "session_id": session_id,
                                "title": f"Session {session_id}",
                                "questions": session_info
                            })
                elif isinstance(data, list):
                    # 处理简单的问题列表
                    sessions_data.append({
                        "session_id": f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        "title": "Questions List",
                        "questions": data
                    })
                
                return sessions_data
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                questions = [line.strip() for line in f if line.strip()]
                return [{
                    "questions": questions,
                    "title": f"Text File Questions",
                    "session_id": f"text_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                }]

    def process_session(self, session_id: str) -> None:
        """处理单个问题会话"""
        if session_id not in self.sessions:
            self.logger.error(f"Session {session_id} not found")
            return
        
        session = self.sessions[session_id]
        session.start_time = datetime.now()
        self.current_session_id = session_id
        
        # 清空当前会话的历史记录
        self.memory.clear()
        
        try:
            # 处理会话中的所有问题
            for i, question in enumerate(session.questions, 1):
                response = self.process_conversation(
                    question,
                    metadata={"number": i, "session_id": session_id}
                )
                session.content.append({
                    "question": question,
                    "response": response,
                    "number": i
                })
            
        finally:
            session.end_time = datetime.now()
            self.current_session_id = None
            
            # 生成会话的markdown文件
            self._save_session_markdown(session)
        
    def _save_session_markdown(self, session: QuestionSession) -> None:
        """将会话保存为Markdown文件"""
        content = []
        for qa in session.content:
            content.append(f"### 问题 {qa['number']}\n")
            content.append(f"**问题描述：**\n{qa['question']}\n")
            content.append(f"**回答：**\n{qa['response']}\n")
            content.append("---\n")
            
        markdown_content = self.config.markdown_template.format(
            title=session.title,
            session_id=session.session_id,
            start_time=session.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            end_time=session.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            content="\n".join(content)
        )
        
        output_path = os.path.join(
            self.config.output_dir,
            f"session_{session.session_id}_{session.start_time.strftime('%Y%m%d_%H%M%S')}.md"
        )
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
            
        self.logger.info(f"Session markdown saved to {output_path}")
        
    def process_all_sessions(self) -> None:
        """处理所有会话"""
        for session_id in self.sessions:
            self.process_session(session_id)
            
    def process_questions(self, questions: Union[str, List[str], Dict[str, List[str]]]) -> None:
        """处理问题（支持多种输入格式）"""
        # 清空现有会话
        self.sessions.clear()
        
        try:
            if isinstance(questions, str):
                # 单个问题或文件路径
                if os.path.exists(questions):
                    sessions_data = self.load_questions_from_file(questions)
                    for data in sessions_data:
                        # 添加类型检查和错误处理
                        if not isinstance(data, dict):
                            self.logger.error(f"Invalid data format: {data}")
                            continue
                        
                        questions_list = data.get("questions")
                        if not questions_list:
                            self.logger.error(f"No questions found in data: {data}")
                            continue
                        
                        session_id = data.get("session_id")
                        title = data.get("title")
                        
                        self.create_session(
                            questions=questions_list,
                            title=title,
                            session_id=session_id
                        )
                else:
                    self.create_session([questions])
            elif isinstance(questions, list):
                # 问题列表（作为一个会话）
                self.create_session(questions)
            elif isinstance(questions, dict):
                # 多个会话
                for session_id, session_questions in questions.items():
                    if isinstance(session_questions, dict):
                        # 处理包含标题和问题的字典格式
                        self.create_session(
                            questions=session_questions.get("questions", []),
                            title=session_questions.get("title"),
                            session_id=session_id
                        )
                    else:
                        # 处理简单的问题列表
                        self.create_session(session_questions, session_id=session_id)
            
            self.process_all_sessions()
        except Exception as e:
            self.logger.error(f"Error processing questions: {str(e)}", exc_info=True)
            raise

def main():
    """主函数：演示各种使用方式"""
    config = ConversationConfig(
        output_dir="output/enhanced5",
        system_prompt="你是一个专业的AI助手，请基于历史上下文（如果有）简单回答问题。",
        output_format=OutputFormat.MARKDOWN,
        temperature=0.7,
        save_interval=5,
        api_key_env="DASHSCOPE_API_KEY",  # 指定使用 .env 中的哪个环境变量
        api_base = "https://dashscope.aliyuncs.com/compatible-mode/v1",
        model_name="qwen-plus"
    )
    
    manager = AIConversationManager(config)
    
    # 示例1：处理单个相关问题序列
    related_questions = [
        "解释一下量子计算的基本原理。",
        "基于上文，量子比特和经典比特有什么区别？",
        "量子纠缠现象是什么？它在量子计算中起什么作用？"
    ]
    
    # 示例2：处理多个独立的问题序列
    independent_sessions = {
        "math": [
            "什么是微积分？",
            "微积分在实际生活中有什么应用？"
        ],
        "physics": [
            "什么是相对论？",
            "为什么光速是宇宙速度的上限？"
        ]
    }
    
    
    # 处理所有示例
    manager.process_questions(related_questions)  # 处理相关问题序列
    
    manager.process_questions(independent_sessions)  # 处理独立问题序列
    
    # 示例3：从文件读取问题
    questions_file = "questions.json"  # 或 "questions.txt"
    if os.path.exists(questions_file):
        manager.process_questions(questions_file)  # 从文件处理问题

    questions_file = "questions.txt"  # 或 "questions.json"
    if os.path.exists(questions_file):
        manager.process_questions(questions_file)  # 从文件处理问题 

if __name__ == "__main__":
    main() 