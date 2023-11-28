# hjimi_tools

# Python Package Setup Script

This script is a utility for automatically setting up a new Python package structure. It creates a directory structure for the package, as well as several important files such as \`pyproject.toml\`, \`README.md\`, \`LICENSE\`, and \`requirements.txt\`.

## Usage

To use this script, you simply need to run it with Python and pass the name of the package you want to create as a command line argument. For example:

\```bash
python setup_package.py --package_name hjimi_tools
\```

This will create a new directory called \`hjimi_tools\` with the following structure:

\```
hjimi_tools/
├── src/
│   └── hjimi_tools/
│       └── __init__.py
├── test/
├── pyproject.toml
├── README.md
├── LICENSE
└── requirements.txt
\```

## Command Line Arguments

The script accepts several command line arguments for customizing the package:

- \`package_name\`: The name of the package to set up. This is a required argument.
- \`--version\`: The version of the package. Defaults to '0.0.1'.
- \`--description\`: The description of the package. Defaults to 'A small example package'.
- \`--author\`: The author of the package. Defaults to 'Example Author'.
- \`--author_email\`: The email of the author. Defaults to 'author@example.com'.
- \`--homepage\`: The homepage URL of the package. Defaults to 'https://github.com/YOUR_USERNAME/YOUR_REPOSITORY'.
- \`--bug_tracker\`: The bug tracker URL of the package. Defaults to 'https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/issues'.

## Requirements

This script requires Python 3.8 or higher.
---

# C Project Generator

This Python class, `CProjectGenerator`, is a utility for automatically setting up a new C project structure. It creates a directory structure for the project, as well as several important files such as `main.c`, `Makefile` or `CMakeLists.txt` depending on the chosen build system.

## Class Initialization

The `CProjectGenerator` class is initialized with the following parameters:

- `project_name`: The name of the project to set up. This is a required argument.
- `modules`: The names of the modules to be created. This is an optional argument and defaults to an empty string.
- `build_system`: The build system to use. This can be either 'make' or 'cmake'. Defaults to 'make'.

Example:

```python
gen = CProjectGenerator("my_project", "module1 module2", "cmake")
```

## Directory Structure

The following directory structure will be created:

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

## Generated Files

The class will generate a `main.c` file in the `src/` directory as well as a `Makefile` or `CMakeLists.txt` in the project root directory depending on the chosen build system. If modules are specified, corresponding `.c` and `.h` files will be created in the `src/` and `include/` directories respectively.

## Usage

To use this class to generate a project, you simply need to create an instance of the class and call the `generate_project` method. For example:

```python
gen = CProjectGenerator("my_project", "module1,module2", "cmake")
gen.generate_project()
```

This will create a new project with the specified name, modules and build system.



