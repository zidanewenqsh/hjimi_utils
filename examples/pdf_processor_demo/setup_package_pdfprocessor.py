#!/usr/bin/env python
#! -*- coding: utf-8 -*-
"""
This script sets up the package structure for a PDF processing package.

Usage:
    python setup_package_pdfprocessor.py

The package will include PDF processing utilities such as:
- PDF splitting by size, pages, or bookmarks
- PDF merging
- PDF page counting
"""
import os
from hjimi_tools import PackageSetup

def setup_pdf_processor():
    # 设置包的基本信息并创建包结构
    package_setup = PackageSetup(
        package_name="pdf_processor",
        version="0.1.0",
        description="A utility package for PDF processing, including splitting, merging, and page counting",
        author="wenquanshan",
        author_email="wenquanshan@sximi.com",
        homepage="https://github.com/zidanewenqsh/pdf_processor",
        bug_tracker="https://github.com/zidanewenqsh/pdf_processor/issues",
        # requirements=["PyPDF2>=3.0.0"]  # 添加依赖包
    )
    
    # 使用 PackageSetup 创建基本包结构
    package_setup.setup_package()

if __name__ == "__main__":
    setup_pdf_processor()
