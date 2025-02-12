# hjimi_tools

## 安装说明

### 前置条件

在安装 `hjimi_tools` 之前，请确保您的系统已安装 Python 3.8 或更高版本。您可以通过在终端中运行以下命令来检查 Python 版本：

```bash
python --version
```

### 安装步骤
您可以使用 Python 包管理器 `pip` 来安装 `hjimi_tools`。在终端中执行以下命令：
```bash
pip install hjimi-tools
```
此命令将从 Python 包索引（PyPI）下载并安装最新版本的 hjimi_tools 及其依赖项。如果您想安装特定版本的 hjimi_tools，可以这样指定版本号：

```bash
pip install hjimi-tools==<版本号>
```
请将 <版本号> 替换为您想安装的实际版本。

### 验证安装
安装完成后，您可以通过在 Python 脚本或交互式会话中导入来验证 hjimi_tools 是否正确安装。打开 Python 解释器并尝试以下操作：
```python
import hjimi_tools
```
如果没有出现错误，说明 `hjimi_tools` 已成功安装并可以使用。现在您可以开始在 Python 项目中使用 `hjimi_tools` 提供的各种工具了。

## Python 包设置脚本

这个脚本是一个用于自动设置新 Python 包结构的工具。它会创建包的目录结构，以及几个重要的文件，如 `pyproject.toml`、`README.md`、`LICENSE` 和 `requirements.txt`。

### 参数说明

- `-p`, `--package_name`: (str) 要设置的包名称。这是必需的参数。
- `-v`, `--version`: (str, 可选) 包的版本。默认为 '0.0.1'。
- `-d`, `--description`: (str, 可选) 包的简要描述。默认为 '一个小型示例包'。
- `-a`, `--author`: (str, 可选) 作者姓名。默认为 '示例作者'。
- `-e`, `--author_email`: (str, 可选) 作者邮箱。默认为 'author@example.com'。
- `-u`, `--homepage`: (str, 可选) 包的主页 URL。默认为 'https://github.com/YOUR_USERNAME/YOUR_REPOSITORY'。
- `-b`, `--bug_tracker`: (str, 可选) 包的问题追踪器 URL。默认为 'https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/issues'。
- `-r`, `--requirements`: (str, 可选) 包的依赖列表。可以指定多个依赖，用空格分隔。

### 使用方法

要使用此脚本，只需使用 Python 运行它，并将要创建的包名作为命令行参数传递。例如：

```bash
python setup_package.py --package_name my_new_package
```
或者

```python
# 在你的应用中
from hjimi_tools import PackageSetup

# 创建一个新的 Python 包结构
package_setup = PackageSetup(package_name='my_new_package', version='1.0.0')
package_setup.setup_package()
```

这将创建一个名为 `hjimi_tools` 的新目录，结构如下：

```
my_new_package/
├── src/
│   └── my_new_packages/
│       └── __init__.py
├── test/
├── pyproject.toml
├── README.md
├── LICENSE
└── requirements.txt
```

## C 项目生成器

这个 Python 类 `CProjectGenerator` 是一个用于自动设置新 C 项目结构的工具。它会创建项目的目录结构，以及根据所选构建系统生成重要文件，如 `main.c`、`Makefile` 或 `CMakeLists.txt`。

### 类初始化

`CProjectGenerator` 类使用以下参数初始化：

- `project_name`: 要设置的项目名称。这是必需的参数。
- `modules`: 要创建的模块名称。这是可选参数，默认为空字符串。
- `build_system`: 要使用的构建系统。可以是 'make' 或 'cmake'。默认为 'make'。

示例：

```python
gen = CProjectGenerator("my_project", "module1 module2", "cmake")
```

### 目录结构

将创建以下目录结构：

```
my_project/
├── src/
│   └── main.c
├── include/
├── lib/
├── bin/
├── obj/
├── test/
└── docs/
```

### 生成的文件

该类将在 `src/` 目录中生成 `main.c` 文件，并根据所选的构建系统在项目根目录中生成 `Makefile` 或 `CMakeLists.txt`。如果指定了模块，将在 `src/` 和 `include/` 目录中分别创建相应的 `.c` 和 `.h` 文件。

### 参数
- `project_name`: (str) 要设置的项目名称。这是必需的参数。
- `-b` 或 `--build`: (str, 可选) 要使用的构建系统。可以是 'make' 或 'cmake'。默认为 'make'。
- `-m` 或 `--modules`: (str, 可选) 以逗号分隔的模块名称列表。这些模块将创建相应的 `.c` 和 `.h` 文件。如果未指定，则不会创建模块。

## 文件收集器

FileCollector 类是一个工具，用于从给定路径列表中收集具有特定扩展名的文件，递归遍历目录以查找这些文件，并将其内容写入格式化的 Markdown 文件中。它支持多种文件类型，根据文件扩展名自动确定适当的语法高亮显示，例如 .py 文件使用 Python 语法，.js 文件使用 JavaScript 语法。该类可以处理多个根目录，并通过将文件分组到各自的项目根目录下来组织输出，为每个项目使用一级标题，为每个文件使用二级标题。它会写入文件的相对路径，然后是代码块中的内容，使用户能够以结构化和易读的格式记录代码和其他文本文件。此外，它还可以优雅地处理读取文件时可能出现的编码错误，在输出中包含错误消息。整个过程通过 run 方法执行，该方法首先收集文件，然后生成 Markdown 输出，确保生成的文件可用于文档或共享目的。

### 参数
- `paths`: 要收集文件的文件或目录路径列表。
- `extensions`: 要收集的文件扩展名列表。
- `output_path`: 输出 markdown 文件的路径。

### 使用方法

```python
from hjimi_tools import FileCollector

# 初始化 FileCollector，指定要收集的路径、文件扩展名和输出路径
collector = FileCollector(paths=['/path/to/project'], extensions=['.py', '.md', '.txt'], output_path="output.md")

# 收集文件并将其内容保存到指定的 Markdown 文件中
collector.run()
```

## 许可证

MIT 许可证

## 联系方式

- 作者：wenquanshan
- 邮箱：wenquanshan@sximi.com
- 项目主页：https://github.com/zidanewenqsh/pdf_processor
- 问题追踪：https://github.com/zidanewenqsh/pdf_processor/issues

## 版本历史

### 0.1.0 (最新)
- 添加命令行参数的短格式支持
  - `-p` 对应 `--package_name`
  - `-v` 对应 `--version`
  - `-d` 对应 `--description`
  - `-a` 对应 `--author`
  - `-e` 对应 `--author_email`
  - `-u` 对应 `--homepage`
  - `-b` 对应 `--bug_tracker`
  - `-r` 对应 `--requirements`
- 新增 requirements 参数支持
  - 支持通过命令行直接指定项目依赖包
  - 可以同时指定多个依赖包，以空格分隔
  - 自动将依赖写入 pyproject.toml 和 requirements.txt

### 0.0.5
- 初始版本发布
- 支持基本的 Python 包结构生成
- 支持 C 项目结构生成
- 支持文件收集器功能