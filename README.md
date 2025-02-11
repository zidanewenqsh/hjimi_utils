# hjimi_utils

hjimi_utils 是一个Python工具集合项目（发布包名为 hjimi_tools），主要包含以下功能模块：

## 主要功能

1. Python包结构生成器
   - 自动创建标准的Python包目录结构
   - 生成必要的配置文件（pyproject.toml, README.md等）
   - 支持自定义包信息（版本号、作者、描述等）

2. C项目结构生成器
   - 创建标准的C项目目录结构
   - 支持Make和CMake两种构建系统
   - 可自定义模块生成
   - 自动生成基础源文件和头文件

3. 文件收集器
   - 支持从多个目录递归收集指定类型的文件
   - 自动识别多种编程语言的文件类型
   - 将收集的文件内容格式化输出为Markdown文档
   - 支持自定义文件扩展名过滤

4. PDF 文件处理器（hjimi_pdf_processor）
   - PDF 文件分割（按大小、页数、书签）
   - PDF 文件合并
   - PDF 文件信息获取
   - 文件名规范化处理

## 安装要求

- Python 3.8 或更高版本
- pip 包管理器

## 安装方法
> 注意：虽然项目目录名为 hjimi_utils，但发布到 PyPI 的包名为 hjimi_tools
```bash
pip install hjimi_tools
pip install hjimi_pdf_processor  # PDF处理器模块
```

## 使用说明

### Python包结构生成器

用于快速创建标准的Python包结构，包括：
- src目录结构
- 测试目录
- 配置文件
- 许可证文件
- README文件

```python
from hjimi_tools.generators import PythonProjectGenerator

# 创建Python项目生成器实例
generator = PythonProjectGenerator(
    project_name="my_project",
    author="Your Name",
    version="0.1.0",
    description="Your project description"
)

# 生成项目结构
generator.generate()
```

### C项目结构生成器

用于创建标准的C语言项目结构，包括：
- 源代码目录
- 头文件目录
- 库文件目录
- 构建系统配置
- 测试目录
- 文档目录

```python
from hjimi_tools.generators import CProjectGenerator

# 创建C项目生成器实例
generator = CProjectGenerator(
    project_name="my_c_project",
    build_system="cmake",  # 或 "make"
    modules=["core", "utils"]
)

# 生成项目结构
generator.generate()
```

### 文件收集器

用于收集和整理项目文件，功能包括：
- 递归遍历目录
- 按扩展名筛选文件
- 生成带语法高亮的Markdown文档
- 支持多种编程语言

```python
from hjimi_tools.collectors import FileCollector

# 创建文件收集器实例
collector = FileCollector(
    source_dirs=["src", "tests"],
    file_extensions=[".py", ".c", ".h"],
    exclude_patterns=["__pycache__", "*.pyc"]
)

# 收集文件并生成Markdown文档
collector.collect()
collector.generate_markdown("project_files.md")
```

### PDF 文件处理器

用于处理 PDF 文件的工具集，功能包括：
- 按指定大小分割 PDF 文件
- 按页数分割 PDF 文件
- 按书签分割 PDF 文件（支持一级书签）
- 合并多个 PDF 文件
- 获取 PDF 文件信息

```python
from hjimi_pdf_processor import PDFProcessor

# 获取 PDF 页数
page_count = PDFProcessor.get_pdf_page_count("document.pdf")

# 按页数分割
PDFProcessor.split_pdf_by_pages("large_doc.pdf", pages_per_split=10)

# 按大小分割（KB）
PDFProcessor.split_pdf_by_size("large_doc.pdf", max_size_kb=1024)

# 按书签分割
PDFProcessor.split_pdf_by_bookmarks("book.pdf")

# 合并 PDF 文件
pdf_files = ["part1.pdf", "part2.pdf", "part3.pdf"]
PDFProcessor.merge_pdfs(pdf_files, "merged.pdf")
```

## 许可证

MIT License

## 贡献指南

欢迎提交问题和建议到我们的GitHub仓库。

## 联系方式

- 作者：wenquanshan
- 邮箱：wenquanshan@sximi.com
- 项目主页：https://github.com/zidanewenqsh/hjimi_utils