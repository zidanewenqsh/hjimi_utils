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
    src_dir = os.path.join(args.package_name, 'src')
    package_dir = os.path.join(src_dir, args.package_name)
    create_dir(package_dir)

    # Create empty __init__.py
    create_file(os.path.join(package_dir, '__init__.py'))

    # Create pyproject.toml file with dynamic content
    pyproject_content = f"""[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{args.package_name}"
version = "{args.version}"
description = "{args.description}"
readme = "README.md"
authors = [
    {{ name = "{args.author}", email = "{args.author_email}" }},
]
license = "{args.license}"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
keywords = "{args.keywords}"

[tool.setuptools]
packages = find:
    where = "src"

#[tool.setuptools]
#packages = ["{args.package_name}"]
#package_dir = {{ "": "src" }}
"""
    create_file(os.path.join(args.package_name, 'pyproject.toml'), pyproject_content)

    # Create README.md file
    create_file(os.path.join(args.package_name, 'README.md'), f'# {args.package_name}\n')

    # Create LICENSE file
    create_file(os.path.join(args.package_name, 'LICENSE'), args.license + '\n')

    # Create requirements.txt file
    create_file(os.path.join(args.package_name, 'requirements.txt'))

    print(f"Package {args.package_name} structure has been set up.")

# Parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Set up a Python package structure.')
    parser.add_argument('package_name', type=str, help='The name of the package to set up')
    parser.add_argument('--version', type=str, default='0.1.0', help='The version of the package')
    parser.add_argument('--description', type=str, default='A small example package', help='The description of the package')
    parser.add_argument('--author', type=str, default='Your Name', help='The author of the package')
    parser.add_argument('--author_email', type=str, default='', help='The email of the author')
    parser.add_argument('--license', type=str, default='MIT', help='The license of the package')
    parser.add_argument('--keywords', type=str, default='example', help='The keywords of the package')
    return parser.parse_args()

def main():
    args = parse_arguments()
    setup_package(args)

if __name__ == "__main__":
    main()
