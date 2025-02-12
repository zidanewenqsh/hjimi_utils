# HJIMI PDF 处理器

PDF 处理器是一个功能强大的 PDF 文件处理工具包，提供多种 PDF 文件操作功能。

## 主要功能

1. PDF 文件拆分
   - 按文件大小拆分
   - 按页数拆分
   - 按书签拆分（支持一级书签）

2. PDF 文件合并
   - 支持多个 PDF 文件合并
   - 保持原始页面内容和格式
   - 错误处理和日志记录

3. PDF 文件信息
   - 获取总页数
   - 文件名规范化

## 特性

- 易于使用：提供直观的静态方法接口
- 灵活配置：支持自定义拆分大小和页数
- 错误处理：全面的异常处理和错误消息
- 文件安全：自动清理临时文件

## 系统要求

- Python 3.8 或更高版本
- PyPDF2 3.0.0 或更高版本

## 安装

```bash
pip install hjimi-pdf-processor
```

## 导入

```python
from hjimi_pdf_processor import PDFProcessor
```

## 使用示例

### 1. 获取 PDF 页数
```python
# 获取单个文件页数
page_count = PDFProcessor.get_pdf_page_count("文档.pdf")
print(f"PDF 页数：{page_count}")

# 获取多个文件页数
pdf_files = ["文档1.pdf", "文档2.pdf", "文档3.pdf"]
for file in pdf_files:
    count = PDFProcessor.get_pdf_page_count(file)
    print(f"{file} 页数：{count}")
```

### 2. 拆分 PDF 文件

```python
# 按页数拆分
PDFProcessor.split_pdf_by_pages("大文档.pdf", pages_per_split=10)

# 按文件大小拆分（单位：KB）
PDFProcessor.split_pdf_by_size("大文档.pdf", max_size_kb=1024)

# 按书签拆分
PDFProcessor.split_pdf_by_bookmarks("书籍.pdf")
```

### 3. 合并 PDF 文件

```python
# 合并多个 PDF 文件
pdf_files = ["第一章.pdf", "第二章.pdf", "第三章.pdf"]
PDFProcessor.merge_pdfs(pdf_files, "合并文档.pdf")
```

## 使用场景

1. 文件拆分
   - 拆分大型 PDF 文件以便于传输
   - 按章节拆分教材或文档（书签）
   - 按固定页数拆分文档以便打印

2. 文件合并
   - 合并多个扫描文档
   - 合并报告或文章章节
   - 将多个 PDF 文件整合成单个文档

3. 文件处理
   - 批量获取 PDF 文件信息
   - 规范化 PDF 文件名
   - 控制 PDF 文件大小

## API 文档

### PDFProcessor 类方法

#### 1. sanitize_filename(filename: str) -> str
清理文件名中的非法字符。
- **参数**：
  - filename：原始文件名
- **返回值**：清理后的合法文件名
- **用途**：处理包含特殊字符的文件名，将非法字符替换为下划线

#### 2. get_pdf_page_count(file_path: str) -> int
获取 PDF 文件的总页数。
- **参数**：
  - file_path：PDF 文件路径
- **返回值**：PDF 总页数，出错时返回 None
- **异常处理**：捕获并打印文件读取错误

#### 3. split_pdf_by_size(input_file: str, max_size_kb: int) -> None
按大小拆分 PDF 文件。
- **参数**：
  - input_file：输入 PDF 文件路径
  - max_size_kb：每个拆分文件的最大大小（KB）
- **输出格式**：`原文件名_部分序号.pdf`
- **特性**：自动清理临时文件，显示实时进度

#### 4. split_pdf_by_pages(input_file: str, pages_per_split: int) -> None
按页数拆分 PDF 文件。
- **参数**：
  - input_file：输入 PDF 文件路径
  - pages_per_split：每个拆分文件的页数
- **输出格式**：`原文件名_部分序号.pdf`
- **特性**：显示拆分进度和页面范围

#### 5. split_pdf_by_bookmarks(input_file: str) -> None
按一级书签拆分 PDF 文件。
- **参数**：
  - input_file：输入 PDF 文件路径
- **输出格式**：`原文件名_部分序号_书签名.pdf`
- **限制**：仅支持一级书签拆分
- **特性**：自动处理书签名中的非法字符

#### 6. merge_pdfs(pdf_files: List[str], output_path: str) -> None
合并多个 PDF 文件。
- **参数**：
  - pdf_files：PDF 文件路径列表
  - output_path：输出文件路径
- **特性**：
  - 保持原始页面内容和格式
  - 单个文件失败不影响整体合并
  - 详细的错误日志记录

## 注意事项

1. 文件操作
   - 确保足够的磁盘空间
   - 保留原始文件备份
   - 注意文件名冲突

2. 性能考虑
   - 大文件处理可能需要较长时间
   - 建议先用小文件测试
   - 监控内存使用情况

3. 限制
   - 不支持加密的 PDF 文件
   - 仅支持一级书签拆分
   - 某些特殊 PDF 格式可能不兼容

## 许可证

MIT 许可证

## 联系方式

- 作者：wenquanshan
- 邮箱：wenquanshan@sximi.com
- 项目主页：https://github.com/zidanewenqsh/pdf_processor
- 问题追踪：https://github.com/zidanewenqsh/pdf_processor/issues

## 贡献指南

我们欢迎问题报告和功能建议。要贡献代码，请：

1. Fork 仓库
2. 创建功能分支
3. 提交更改
4. 确保所有测试通过
5. 提交拉取请求

## 更新日志

### v0.1.2
- 修复包结构和导入路径
- 重命名源目录以匹配包名
- 更新项目配置以正确命名包

### v0.1.1
- 修复文档中的包导入语句
- 更新包名为 hjimi_pdf_processor
- 改进文档结构

### v0.1.0
- 初始版本发布
- 实现基本的 PDF 拆分和合并功能
- 添加文件信息获取功能
