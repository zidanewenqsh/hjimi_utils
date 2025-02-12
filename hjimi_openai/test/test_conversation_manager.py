#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import tempfile
from pathlib import Path
from hjimi_openai import AIConversationManager, ConversationConfig, OutputFormat

def test_basic_conversation(output_dir: str):
    """测试基本对话功能"""
    config = ConversationConfig(
        output_dir=output_dir,
        model_name="qwen-plus",
        temperature=0.7,
        streaming=True,
        output_format=OutputFormat.MARKDOWN
    )
    
    manager = AIConversationManager(config)
    
    # 测试单个问题
    response = manager.process_conversation("什么是Python？")
    print(f"\n单个问题测试结果:\n{response}\n")
    
    # 验证输出文件是否创建
    output_file = Path(output_dir) / f"conversation.{config.output_format.value}"
    assert output_file.exists(), "输出文件未创建"
    
    # 清理资源
    manager.clear_history()

def test_multi_session(output_dir: str):
    """测试多会话管理功能"""
    config = ConversationConfig(
        output_dir=output_dir,
        model_name="qwen-plus",
        temperature=0.7
    )
    
    manager = AIConversationManager(config)
    
    try:
        # 创建多个测试会话
        sessions = {
            "python_basics": {
                "title": "Python基础知识",
                "questions": [
                    "Python的列表和元组有什么区别？",
                    "什么是Python的装饰器？"
                ]
            },
            "ai_concepts": {
                "title": "AI概念",
                "questions": [
                    "什么是机器学习？",
                    "深度学习与机器学习有什么区别？"
                ]
            }
        }
        
        # 处理会话
        manager.process_questions(sessions)
        
        # 验证会话输出文件
        session_files = list(Path(output_dir).glob("session_*.md"))
        assert len(session_files) > 0, "会话输出文件未创建"
        print(f"\n已创建的会话文件: {[f.name for f in session_files]}\n")
        
    finally:
        manager.clear_history()
        del manager

def test_file_loading(output_dir: str):
    """测试从文件加载问题功能"""
    # 创建测试文件目录
    test_files_dir = os.path.join(output_dir, "test_files")
    os.makedirs(test_files_dir, exist_ok=True)
    
    # 1. 创建测试用的JSON问题文件（完整格式）
    questions_json_full = Path(test_files_dir) / "test_questions_full.json"
    test_questions_full = {
        "session1": {
            "title": "编程概念测试",
            "questions": [
                "什么是面向对象编程？",
                "什么是设计模式？"
            ]
        },
        "session2": {
            "title": "Python基础",
            "questions": [
                "Python的GIL是什么？",
                "Python的装饰器原理是什么？"
            ]
        }
    }
    
    with open(questions_json_full, 'w', encoding='utf-8') as f:
        json.dump(test_questions_full, f, ensure_ascii=False, indent=2)
    
    # 2. 创建测试用的JSON问题文件（简单列表格式）
    questions_json_simple = Path(test_files_dir) / "test_questions_simple.json"
    test_questions_simple = [
        "什么是人工智能？",
        "机器学习和深度学习的区别是什么？",
        "神经网络的基本原理是什么？"
    ]
    
    with open(questions_json_simple, 'w', encoding='utf-8') as f:
        json.dump(test_questions_simple, f, ensure_ascii=False, indent=2)
    
    # 3. 创建测试用的TXT问题文件
    questions_txt = Path(test_files_dir) / "test_questions.txt"
    txt_questions = [
        "什么是数据结构？",
        "常见的排序算法有哪些？",
        "什么是时间复杂度和空间复杂度？"
    ]
    
    with open(questions_txt, 'w', encoding='utf-8') as f:
        f.write('\n'.join(txt_questions))
    
    config = ConversationConfig(
        output_dir=output_dir,
        model_name="qwen-plus"
    )
    
    manager = AIConversationManager(config)
    
    try:
        print("\n测试加载完整格式的JSON文件:")
        manager.process_questions(str(questions_json_full))
        
        print("\n测试加载简单列表格式的JSON文件:")
        manager.process_questions(str(questions_json_simple))
        
        print("\n测试加载TXT文件:")
        manager.process_questions(str(questions_txt))
        
        # 验证输出
        session_files = list(Path(output_dir).glob("session_*.md"))
        assert len(session_files) > 0, "会话输出文件未创建"
        print(f"\n已创建的会话文件: {[f.name for f in session_files]}\n")
        
        # 检查文件内容
        print("\n生成的测试文件内容:")
        print("\n1. 完整格式JSON文件内容:")
        with open(questions_json_full, 'r', encoding='utf-8') as f:
            print(json.dumps(json.load(f), ensure_ascii=False, indent=2))
        
        print("\n2. 简单列表JSON文件内容:")
        with open(questions_json_simple, 'r', encoding='utf-8') as f:
            print(json.dumps(json.load(f), ensure_ascii=False, indent=2))
        
        print("\n3. TXT文件内容:")
        with open(questions_txt, 'r', encoding='utf-8') as f:
            print(f.read())
        
    finally:
        manager.clear_history()
        del manager

def test_different_output_formats(output_dir: str):
    """测试不同输出格式"""
    for output_format in OutputFormat:
        config = ConversationConfig(
            output_dir=output_dir,
            output_format=output_format,
            model_name="qwen-plus"
        )
        
        manager = AIConversationManager(config)
        
        try:
            # 测试简单对话
            response = manager.process_questions(
                ["请用一句话解释什么是人工智能。", "请用一句话说明什么是深度学习"]
            )
            
            # 验证输出文件
            output_file = Path(output_dir) / f"conversation.{output_format.value}"
            assert output_file.exists(), f"{output_format.value}格式输出文件未创建"
            print(f"\n{output_format.value}格式输出文件已创建-{output_file}")
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            manager.clear_history()
            del manager

def main():
    """运行所有测试"""
    print("开始测试 hjimi_openai 包...")
    
    # 创建临时测试目录
    temp_dir = tempfile.mkdtemp(prefix="hjimi_test_")
    try:
        print(f"\n使用测试目录: {temp_dir}")
        
        print("\n1. 测试基本对话功能")
        test_basic_conversation(temp_dir)
        
        print("\n2. 测试多会话管理")
        test_multi_session(temp_dir)
        
        print("\n3. 测试从文件加载问题")
        test_file_loading(temp_dir)
        
        print("\n4. 测试不同输出格式")
        test_different_output_formats(temp_dir)
        
        print("\n所有测试完成！")
        
    except Exception as e:
        print(f"\n测试过程中出现错误: {str(e)}")
        raise
    finally:
        # 保留临时目录并打印相关信息
        print(f"\n测试文件和输出保存在临时目录: {temp_dir}")
        print("目录内容:")
        for root, dirs, files in os.walk(temp_dir):
            level = root.replace(temp_dir, '').count(os.sep)
            indent = ' ' * 4 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print(f"{subindent}{f}")

if __name__ == "__main__":
    main()