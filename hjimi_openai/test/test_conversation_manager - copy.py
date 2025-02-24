#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import tempfile
from pathlib import Path
from hjimi_openai import AIConversationManager, ConversationConfig, OutputFormat

def test_basic_conversation():
    """测试基本对话功能"""
    # 创建临时输出目录
    with tempfile.TemporaryDirectory() as temp_dir:
        config = ConversationConfig(
            output_dir=temp_dir,
            model_name="qwen-plus",
            temperature=0.7,
            streaming=True,
            output_format=OutputFormat.MARKDOWN
        )
        
        manager = AIConversationManager(config)
        
        try:
            # 测试单个问题
            response = manager.process_conversation("什么是Python？")
            print(f"\n单个问题测试结果:\n{response}\n")
            
            # 验证输出文件是否创建
            output_file = Path(temp_dir) / f"conversation.{config.output_format.value}"
            assert output_file.exists(), "输出文件未创建"
            
            # 确保所有文件操作完成
            manager.cleanup()
        finally:
            # 确保关闭所有可能的文件句柄
            if hasattr(manager, 'close'):
                manager.close()

def test_multi_session():
    """测试多会话管理功能"""
    with tempfile.TemporaryDirectory() as temp_dir:
        config = ConversationConfig(
            output_dir=temp_dir,
            model_name="qwen-plus",
            temperature=0.7
        )
        
        manager = AIConversationManager(config)
        
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
        session_files = list(Path(temp_dir).glob("session_*.md"))
        assert len(session_files) > 0, "会话输出文件未创建"
        print(f"\n已创建的会话文件: {[f.name for f in session_files]}\n")

def test_file_loading():
    """测试从文件加载问题功能"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # 1. 创建测试用的JSON问题文件（完整格式）
        questions_json_full = Path(temp_dir) / "test_questions_full.json"
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
        questions_json_simple = Path(temp_dir) / "test_questions_simple.json"
        test_questions_simple = [
            "什么是人工智能？",
            "机器学习和深度学习的区别是什么？",
            "神经网络的基本原理是什么？"
        ]
        
        with open(questions_json_simple, 'w', encoding='utf-8') as f:
            json.dump(test_questions_simple, f, ensure_ascii=False, indent=2)
            
        # 3. 创建测试用的TXT问题文件
        questions_txt = Path(temp_dir) / "test_questions.txt"
        txt_questions = [
            "什么是数据结构？",
            "常见的排序算法有哪些？",
            "什么是时间复杂度和空间复杂度？"
        ]
        
        with open(questions_txt, 'w', encoding='utf-8') as f:
            f.write('\n'.join(txt_questions))
            
        # 测试处理不同格式的文件
        config = ConversationConfig(
            output_dir=temp_dir,
            model_name="qwen-plus"
        )
        
        manager = AIConversationManager(config)
        
        print("\n测试加载完整格式的JSON文件:")
        manager.process_questions(str(questions_json_full))
        
        print("\n测试加载简单列表格式的JSON文件:")
        manager.process_questions(str(questions_json_simple))
        
        print("\n测试加载TXT文件:")
        manager.process_questions(str(questions_txt))
        
        # 验证输出
        session_files = list(Path(temp_dir).glob("session_*.md"))
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

def test_different_output_formats():
    """测试不同输出格式"""
    with tempfile.TemporaryDirectory() as temp_dir:
        for output_format in OutputFormat:
            config = ConversationConfig(
                output_dir=temp_dir,
                output_format=output_format,
                model_name="qwen-plus"
            )
            
            manager = AIConversationManager(config)
            
            # 测试简单对话
            response = manager.process_conversation(
                "请用一句话解释什么是人工智能。"
            )
            
            # 验证输出文件
            output_file = Path(temp_dir) / f"conversation.{output_format.value}"
            assert output_file.exists(), f"{output_format.value}格式输出文件未创建"
            print(f"\n{output_format.value}格式输出文件已创建")

def main():
    """运行所有测试"""
    print("开始测试 hjimi_openai 包...")
    
    try:
        print("\n1. 测试基本对话功能")
        test_basic_conversation()
        
        print("\n2. 测试多会话管理")
        test_multi_session()
        
        print("\n3. 测试从文件加载问题")
        test_file_loading()
        
        print("\n4. 测试不同输出格式")
        test_different_output_formats()
        
        print("\n所有测试完成！")
        
    except Exception as e:
        print(f"\n测试过程中出现错误: {str(e)}")
        raise

if __name__ == "__main__":
    main()