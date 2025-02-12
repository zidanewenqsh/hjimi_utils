# hjimi_openai

一个基于 LangChain 的 AI 对话管理工具，支持多会话管理、流式输出、自动保存和备份等功能。专注于提供灵活且强大的对话管理解决方案。

## 主要功能

- 多会话管理
  - 支持管理多个独立的对话会话
  - 自动会话保存和恢复
  - 灵活的会话配置系统
  - 会话历史记录管理支持

- 多种输出格式支持
  - Markdown 格式输出
  - JSON 格式输出
  - 纯文本 (TXT) 输出
  - HTML 格式输出

- 自动化功能
  - 自动保存对话历史
  - 定期备份功能
  - 自动管理历史记录长度

- 输入/输出处理
  - 支持流式输出
  - 支持从文件批量加载问题
    - 支持 JSON 格式
    - 支持 TXT 格式
  - 灵活的输出格式化

- 系统功能
  - 完整的日志系统
  - 错误处理和恢复
  - 环境变量配置
  - 会话状态管理

## 安装要求

- Python 3.8 或更高版本
- 必需的依赖包：
  - langchain-openai>=0.0.3
  - langchain-core>=0.1.4
  - langchain-community>=0.0.6
  - langchain>=0.1.0

## 快速开始

1. 安装包
```bash
pip install hjimi-openai
```

2. 设置环境变量
```bash
# 设置 API 密钥
export DASHSCOPE_API_KEY="your_api_key_here"
```

3. 基本使用
```python
from hjimi_openai import AIConversationManager, ConversationConfig

# 创建配置
config = ConversationConfig(
    output_dir="output",
    model_name="qwen-plus",
    temperature=0.7
)

# 初始化管理器
manager = AIConversationManager(config)

# 处理单个问题
response = manager.process_conversation("什么是人工智能？")
print(response)
```

## 配置选项

### 基础配置
- `model_name`: 使用的模型名称（默认: "qwen-plus"）
- `temperature`: 温度参数（默认: 0.0）
- `max_tokens`: 最大令牌数（默认: 1024）
- `streaming`: 是否启用流式输出（默认: True）
- `output_dir`: 输出目录（默认: "output"）
- `output_format`: 输出格式（支持 markdown/json/txt/html）

### 高级配置
- `system_prompt`: 系统提示词
- `api_base`: API 基础 URL
- `api_key_env`: API 密钥环境变量名
- `save_interval`: 自动保存间隔
- `max_history_length`: 最大历史记录长度
- `backup_enabled`: 是否启用备份
- `session_id_prefix`: 会话 ID 前缀

## 高级用法

### 多会话管理
```python
# 创建多个会话
sessions = {
    "ai_basics": [
        "什么是机器学习？",
        "深度学习与机器学习的区别是什么？"
    ],
    "python_tips": [
        "Python的装饰器是什么？",
        "如何使用生成器提高性能？"
    ]
}

manager.process_questions(sessions)
```

### 从文件加载问题
```python
# JSON 格式示例
questions_json = {
    "session1": {
        "title": "AI基础知识",
        "questions": [
            "什么是神经网络？",
            "什么是反向传播？"
        ]
    }
}

# 从文件加载
manager.process_questions("questions.json")
```

### 自定义输出格式
```python
from hjimi_openai import ConversationConfig, OutputFormat

config = ConversationConfig(
    output_format=OutputFormat.MARKDOWN,
    markdown_template="""
# {title}
## 问答记录
{content}
"""
)

manager = AIConversationManager(config)
```

### 基本对话示例
```python
# 创建管理器实例
manager = AIConversationManager()

# 简单对话
questions = [
    "Python中的列表和元组有什么区别？",
    "如何在Python中处理异常？"
]

for question in questions:
    response = manager.process_conversation(question)
    print(f"问题：{question}")
    print(f"回答：{response}\n")
```

### 批量处理示例
```python
# 准备批量问题
batch_questions = {
    "programming": {
        "title": "编程基础",
        "questions": [
            "什么是面向对象编程？",
            "什么是设计模式？",
            "什么是函数式编程？"
        ]
    },
    "database": {
        "title": "数据库基础",
        "questions": [
            "什么是数据库索引？",
            "SQL和NoSQL的区别是什么？"
        ]
    }
}

# 批量处理
manager.process_questions(batch_questions)
```

### 自定义配置示例
```python
config = ConversationConfig(
    model_name="qwen-plus",
    temperature=0.7,
    max_tokens=2048,
    streaming=True,
    output_dir="custom_output",
    output_format=OutputFormat.MARKDOWN,
    system_prompt="你是一个专业的编程助手，请用简洁的语言回答问题。",
    save_interval=3,
    max_history_length=100,
    backup_enabled=True
)

manager = AIConversationManager(config)
```

## 版本历史

### 0.1.0 (当前版本)
- 初始版本发布
- 支持多会话管理
- 支持多种输出格式
- 支持流式输出
- 支持自动保存和备份
- 支持从文件加载问题

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

## 作者

wenquanshan (wenquanshan@sximi.com)

## 联系方式

- GitHub: [https://github.com/zidanewenqsh/openai_demo](https://github.com/zidanewenqsh/openai_demo)
- Email: wenquanshan@sximi.com
- Bug 反馈: [https://github.com/zidanewenqsh/openai_demo/issues](https://github.com/zidanewenqsh/openai_demo/issues)