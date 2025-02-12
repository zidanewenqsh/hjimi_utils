# hjimi_openai

An AI conversation management tool based on LangChain, supporting multi-session management, streaming output, automatic saving and backup, and other features. Focused on providing flexible and powerful conversation management solutions.

## Key Features

- Multi-Session Management
  - Support for managing multiple independent conversation sessions
  - Automatic session saving and recovery
  - Flexible session configuration system
  - Session history management support

- Multiple Output Format Support
  - Markdown format output
  - JSON format output
  - Plain text (TXT) output
  - HTML format output

- Automation Features
  - Automatic conversation history saving
  - Periodic backup functionality
  - Automatic history length management

- Input/Output Processing
  - Support for streaming output
  - Support for batch loading questions from files
    - JSON format support
    - TXT format support
  - Flexible output formatting

- System Features
  - Complete logging system
  - Error handling and recovery
  - Environment variable configuration
  - Session state management

## Installation Requirements

- Python 3.8 or higher
- Required dependencies:
  - langchain-openai>=0.0.3
  - langchain-core>=0.1.4
  - langchain-community>=0.0.6
  - langchain>=0.1.0

## Quick Start

1. Install Package
```bash
pip install hjimi-openai
```

2. Set Environment Variables
```bash
# Set API Key
export DASHSCOPE_API_KEY="your_api_key_here"
```

3. Basic Usage
```python
from hjimi_openai import AIConversationManager, ConversationConfig

# Create configuration
config = ConversationConfig(
    output_dir="output",
    model_name="qwen-plus",
    temperature=0.7
)

# Initialize manager
manager = AIConversationManager(config)

# Process single question
response = manager.process_conversation("What is artificial intelligence?")
print(response)
```

## Configuration Options

### Basic Configuration
- `model_name`: Model name to use (default: "qwen-plus")
- `temperature`: Temperature parameter (default: 0.0)
- `max_tokens`: Maximum tokens (default: 1024)
- `streaming`: Enable streaming output (default: True)
- `output_dir`: Output directory (default: "output")
- `output_format`: Output format (supports markdown/json/txt/html)

### Advanced Configuration
- `system_prompt`: System prompt
- `api_base`: API base URL
- `api_key_env`: API key environment variable name
- `save_interval`: Auto-save interval
- `max_history_length`: Maximum history length
- `backup_enabled`: Enable backup
- `session_id_prefix`: Session ID prefix

## Advanced Usage

### Multi-Session Management
```python
# Create multiple sessions
sessions = {
    "ai_basics": [
        "What is machine learning?",
        "What's the difference between deep learning and machine learning?"
    ],
    "python_tips": [
        "What are Python decorators?",
        "How to use generators to improve performance?"
    ]
}

manager.process_questions(sessions)
```

### Loading Questions from File
```python
# JSON format example
questions_json = {
    "session1": {
        "title": "AI Basics",
        "questions": [
            "What are neural networks?",
            "What is backpropagation?"
        ]
    }
}

# Load from file
manager.process_questions("questions.json")
```

### Custom Output Format
```python
from hjimi_openai import ConversationConfig, OutputFormat

config = ConversationConfig(
    output_format=OutputFormat.MARKDOWN,
    markdown_template="""
# {title}
## Q&A Records
{content}
"""
)

manager = AIConversationManager(config)
```

### Basic Conversation Example
```python
# Create manager instance
manager = AIConversationManager()

# Simple conversation
questions = [
    "What's the difference between lists and tuples in Python?",
    "How to handle exceptions in Python?"
]

for question in questions:
    response = manager.process_conversation(question)
    print(f"Question: {question}")
    print(f"Answer: {response}\n")
```

### Batch Processing Example
```python
# Prepare batch questions
batch_questions = {
    "programming": {
        "title": "Programming Basics",
        "questions": [
            "What is object-oriented programming?",
            "What are design patterns?",
            "What is functional programming?"
        ]
    },
    "database": {
        "title": "Database Basics",
        "questions": [
            "What is database indexing?",
            "What's the difference between SQL and NoSQL?"
        ]
    }
}

# Batch processing
manager.process_questions(batch_questions)
```

### Custom Configuration Example
```python
config = ConversationConfig(
    model_name="qwen-plus",
    temperature=0.7,
    max_tokens=2048,
    streaming=True,
    output_dir="custom_output",
    output_format=OutputFormat.MARKDOWN,
    system_prompt="You are a professional programming assistant. Please answer questions concisely.",
    save_interval=3,
    max_history_length=100,
    backup_enabled=True
)

manager = AIConversationManager(config)
```

## Version History

### 0.1.0 (Current)
- Initial release
- Multi-session management support
- Multiple output format support
- Streaming output support
- Automatic saving and backup support
- File-based question loading support

## Contributing

Issues and Pull Requests are welcome to help improve the project.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Author

wenquanshan (wenquanshan@sximi.com)

## Contact

- GitHub: [https://github.com/zidanewenqsh/openai_demo](https://github.com/zidanewenqsh/openai_demo)
- Email: wenquanshan@sximi.com
- Bug Reports: [https://github.com/zidanewenqsh/openai_demo/issues](https://github.com/zidanewenqsh/openai_demo/issues)