import os
import argparse

# Function to create file with initial content if it doesn't exist
def create_file(path, content=''):
    if not os.path.isfile(path):
        with open(path, 'w') as f:
            f.write(content)
    else:
        print(f"File {path} already exists.")

# Function to create directory if it doesn't exist
def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    else:
        print(f"Directory {path} already exists.")

# Function to set up the package structure
def setup_package(args):
    # Create the src directory to hold the package
    src_dir = os.path.join(args.package_name, 'src')
    package_dir = os.path.join(src_dir, args.package_name)
    create_dir(package_dir)
    # Create the test directory to hold the test script
    test_dir = os.path.join(args.package_name, "test")
    create_dir(test_dir)
    # Create empty __init__.py
    create_file(os.path.join(package_dir, '__init__.py'))

    # Create pyproject.toml file with dynamic content
    pyproject_content = f"""[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{args.package_name}"
version = "{args.version}"
authors = [
    {{ name = "{args.author}", email = "{args.author_email}" }},
]
description = "{args.description}"
readme = "README.md"
requires-python = ">=3.8"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
keywords = "{args.keywords}"

[project.urls]
Homepage = "{args.homepage}"
Bug Tracker = "{args.bug_tracker}"

[tool.setuptools]
packages = find:
    where = "src"
"""
    create_file(os.path.join(args.package_name, 'pyproject.toml'), pyproject_content)

    # Create README.md file
    create_file(os.path.join(args.package_name, 'README.md'), f'# {args.package_name}\n')

    # Create LICENSE file
    create_file(os.path.join(args.package_name, 'LICENSE'), 'MIT License\n')

    # Create requirements.txt file
    create_file(os.path.join(args.package_name, 'requirements.txt'))

    print(f"Package {args.package_name} structure has been set up.")

# Parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Set up a Python package structure.')
    parser.add_argument('package_name', type=str, help='The name of the package to set up')
    parser.add_argument('--version', type=str, default='0.0.1', help='The version of the package')
    parser.add_argument('--description', type=str, default='A small example package', help='The description of the package')
    parser.add_argument('--author', type=str, default='Example Author', help='The author of the package')
    parser.add_argument('--author_email', type=str, default='author@example.com', help='The email of the author')
    parser.add_argument('--keywords', type=str, default='', help='The keywords of the package')
    parser.add_argument('--homepage', type=str, default='https://github.com/YOUR_USERNAME/YOUR_REPOSITORY', help='The homepage URL of the package')
    parser.add_argument('--bug_tracker', type=str, default='https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/issues', help='The bug tracker URL of the package')
    return parser.parse_args()

def main():
    args = parse_arguments()
    setup_package(args)

if __name__ == "__main__":
    main()
