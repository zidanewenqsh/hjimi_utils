# HJIMI PDF Processor

PDF Processor is a powerful PDF file processing toolkit that provides various PDF file manipulation functions.

## Main Features

1. PDF File Splitting
   - Split by file size
   - Split by page count
   - Split by bookmarks (supports first-level bookmarks)

2. PDF File Merging
   - Support merging multiple PDF files
   - Maintain original page content and format
   - Error handling and logging

3. PDF File Information
   - Get total page count
   - Filename normalization

## Features

- Easy to use: Provides intuitive static method interfaces
- Flexible configuration: Supports custom split sizes and page counts
- Error handling: Comprehensive exception handling and error messages
- File safety: Automatic temporary file cleanup

## Requirements

- Python 3.8 or higher
- PyPDF2 3.0.0 or higher

## Installation

```bash
pip install hjimi-pdf-processor
```

## Import

```python
from hjimi_pdf_processor import PDFProcessor
```

## Usage Examples

### 1. Get PDF Page Count
```python
# Get single file page count
page_count = PDFProcessor.get_pdf_page_count("document.pdf")
print(f"PDF pages: {page_count}")

# Get multiple file page counts
pdf_files = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
for file in pdf_files:
    count = PDFProcessor.get_pdf_page_count(file)
    print(f"{file} pages: {count}")
```

### 2. Split PDF Files

```python
# Split by page count
PDFProcessor.split_pdf_by_pages("large_doc.pdf", pages_per_split=10)

# Split by file size (in KB)
PDFProcessor.split_pdf_by_size("large_doc.pdf", max_size_kb=1024)

# Split by bookmarks
PDFProcessor.split_pdf_by_bookmarks("book.pdf")
```

### 3. Merge PDF Files

```python
# Merge multiple PDF files
pdf_files = ["chapter1.pdf", "chapter2.pdf", "chapter3.pdf"]
PDFProcessor.merge_pdfs(pdf_files, "merged_document.pdf")
```

## Use Cases

1. File Splitting
   - Split large PDF files for easier transmission
   - Split textbooks or documents by chapters (bookmarks)
   - Split documents by fixed page count for printing

2. File Merging
   - Merge multiple scanned documents
   - Combine report or article sections
   - Integrate multiple PDF files into a single document

3. File Processing
   - Batch retrieve PDF file information
   - Normalize PDF filenames
   - Control PDF file sizes

## API Documentation

### PDFProcessor Class Methods

#### 1. sanitize_filename(filename: str) -> str
Cleans illegal characters from filenames.
- **Parameters**:
  - filename: Original filename
- **Returns**: Cleaned legal filename
- **Usage**: Handles filenames containing special characters, replacing illegal characters with underscores

#### 2. get_pdf_page_count(file_path: str) -> int
Gets the total page count of a PDF file.
- **Parameters**:
  - file_path: PDF file path
- **Returns**: Total PDF pages, None if error occurs
- **Exception Handling**: Catches and prints file reading errors

#### 3. split_pdf_by_size(input_file: str, max_size_kb: int) -> None
Splits PDF file by size.
- **Parameters**:
  - input_file: Input PDF file path
  - max_size_kb: Maximum size for each split file (KB)
- **Output Format**: `original_filename_part_number.pdf`
- **Features**: Auto-cleans temporary files, displays real-time progress

#### 4. split_pdf_by_pages(input_file: str, pages_per_split: int) -> None
Splits PDF file by page count.
- **Parameters**:
  - input_file: Input PDF file path
  - pages_per_split: Pages per split file
- **Output Format**: `original_filename_part_number.pdf`
- **Features**: Shows split progress and page ranges

#### 5. split_pdf_by_bookmarks(input_file: str) -> None
Splits PDF file by first-level bookmarks.
- **Parameters**:
  - input_file: Input PDF file path
- **Output Format**: `original_filename_part_number_bookmark_name.pdf`
- **Limitations**: Only supports first-level bookmark splitting
- **Features**: Automatically handles illegal characters in bookmark names

#### 6. merge_pdfs(pdf_files: List[str], output_path: str) -> None
Merges multiple PDF files.
- **Parameters**:
  - pdf_files: List of PDF file paths
  - output_path: Output file path
- **Features**:
  - Maintains original page content and format
  - Single file failure doesn't affect overall merge
  - Detailed error logging

## Notes

1. File Operations
   - Ensure sufficient disk space
   - Keep original file backups
   - Be aware of filename conflicts

2. Performance Considerations
   - Large file processing may take time
   - Test with small files first
   - Monitor memory usage

3. Limitations
   - Does not support encrypted PDF files
   - Only supports first-level bookmark splitting
   - Some special PDF formats may not be compatible

## License

MIT License

## Contact

- Author: wenquanshan
- Email: wenquanshan@sximi.com
- Project Homepage: https://github.com/zidanewenqsh/pdf_processor
- Issue Tracking: https://github.com/zidanewenqsh/pdf_processor/issues

## Contributing

We welcome issue reports and feature suggestions. To contribute code:

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Ensure all tests pass
5. Submit a pull request

## Changelog

### v0.1.2
- Fixed package structure and import path
- Renamed source directory to match package name
- Updated project configuration for correct package naming

### v0.1.1
- Fixed package import statement in documentation
- Updated package name to hjimi_pdf_processor
- Improved documentation structure

### v0.1.0
- Initial release
- Implemented basic PDF splitting and merging functions
- Added file information retrieval features
