#!/usr/bin/env python
#! -*- coding: utf-8 -*-
"""
This script sets up the package structure for an OpenAI demo package.

Usage:
    python setup_package_openai.py

The package will include OpenAI integration utilities such as:
- AI conversation management
- Chat history handling
- Multiple session support
- Various output format support
"""
import os
from hjimi_tools import PackageSetup

def setup_openai_demo():
    # Set up package basic information and create package structure
    package_setup = PackageSetup(
        package_name="hjimi_openai",
        version="0.1.0",
        description="A demo package for OpenAI integration with conversation management and multiple output formats",
        author="wenquanshan",
        author_email="wenquanshan@sximi.com",
        homepage="https://github.com/zidanewenqsh/openai_demo",
        bug_tracker="https://github.com/zidanewenqsh/openai_demo/issues",
        requirements=[
            "langchain-openai>=0.0.3",
            "langchain-core>=0.1.4",
            "langchain-community>=0.0.6",
            "langchain>=0.1.0"
        ]
    )
    
    # Create basic package structure using PackageSetup
    package_setup.setup_package()

if __name__ == "__main__":
    setup_openai_demo()
