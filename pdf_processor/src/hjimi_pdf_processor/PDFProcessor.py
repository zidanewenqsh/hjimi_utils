import os
import re
from PyPDF2 import PdfReader, PdfWriter

class PDFProcessor:
    """
    PDF 文件处理工具类，提供 PDF 的分割、合并、读取等功能
    """
    
    @staticmethod
    def sanitize_filename(filename):
        """
        清理文件名中的非法字符
        :param filename: 原始文件名
        :return: 清理后的文件名
        """
        illegal_characters = r'[\/:*?"<>|]'
        return re.sub(illegal_characters, "_", filename)

    @staticmethod
    def get_pdf_page_count(file_path):
        """
        获取 PDF 文件的总页数
        :param file_path: PDF 文件路径
        :return: 总页数
        """
        try:
            reader = PdfReader(file_path)
            return len(reader.pages)
        except Exception as e:
            print(f"读取 PDF 文件时出错: {e}")
            return None

    @staticmethod
    def split_pdf_by_size(input_file, max_size_kb):
        """
        按文件大小拆分 PDF
        :param input_file: 输入 PDF 文件路径
        :param max_size_kb: 每个拆分文件的最大大小（KB）
        """
        reader = PdfReader(input_file)
        writer = PdfWriter()
        part_number = 0
        current_size = 0

        for page_num, page in enumerate(reader.pages):
            writer.add_page(page)
            
            temp_file = f"temp_part_{part_number}.pdf"
            with open(temp_file, "wb") as temp_pdf:
                writer.write(temp_pdf)
            
            current_size = os.path.getsize(temp_file) / 1024
            if current_size > max_size_kb:
                output_file = f"{input_file.replace('.pdf', '')}_part_{part_number}.pdf"
                with open(output_file, "wb") as output_pdf:
                    writer.write(output_pdf)
                print(f"生成文件: {output_file}，大小: {current_size:.2f} KB")

                writer = PdfWriter()
                part_number += 1

        if writer.pages:
            output_file = f"{input_file.replace('.pdf', '')}_part_{part_number}.pdf"
            with open(output_file, "wb") as output_pdf:
                writer.write(output_pdf)
            print(f"生成文件: {output_file}")

        if os.path.exists(temp_file):
            os.remove(temp_file)
        print("PDF 按大小拆分完成！")

    @staticmethod
    def split_pdf_by_pages(input_file, pages_per_split):
        """
        按指定页数拆分 PDF 文件
        :param input_file: 输入 PDF 文件路径
        :param pages_per_split: 每个文件包含的页数
        """
        reader = PdfReader(input_file)
        total_pages = len(reader.pages)
        print(f"总页数: {total_pages}")
        
        base_name = input_file.replace('.pdf', '')
        
        for start_page in range(0, total_pages, pages_per_split):
            writer = PdfWriter()
            end_page = min(start_page + pages_per_split, total_pages)
            
            for page_num in range(start_page, end_page):
                writer.add_page(reader.pages[page_num])
            
            output_file = f"{base_name}_part_{start_page // pages_per_split + 1}.pdf"
            with open(output_file, "wb") as output_pdf:
                writer.write(output_pdf)
            print(f"生成文件: {output_file}，包含页数: {start_page + 1} - {end_page}")
        
        print("PDF 拆分完成！")

    @staticmethod
    def split_pdf_by_bookmarks(input_file):
        """
        按书签拆分 PDF 文件（仅处理主书签）
        :param input_file: 输入 PDF 文件路径
        """
        reader = PdfReader(input_file)
        bookmarks = reader.outline
        
        if not bookmarks:
            print("此 PDF 文件没有书签，无法按书签拆分。")
            return
        
        main_bookmarks = [bookmark for bookmark in bookmarks if not isinstance(bookmark, list)]
        print(f"发现一级书签数量: {len(main_bookmarks)}")
        
        for i, bookmark in enumerate(main_bookmarks):
            start_page = reader.get_destination_page_number(bookmark)
            end_page = (reader.get_destination_page_number(main_bookmarks[i + 1]) 
                       if i + 1 < len(main_bookmarks) else len(reader.pages))
            
            writer = PdfWriter()
            for page_num in range(start_page, end_page):
                writer.add_page(reader.pages[page_num])
            
            safe_title = PDFProcessor.sanitize_filename(bookmark.title)
            output_file = f"{input_file.replace('.pdf', '')}_part_{i+1}_{safe_title}.pdf"
            
            with open(output_file, "wb") as output_pdf:
                writer.write(output_pdf)
            
            print(f"生成文件: {output_file}，包含页数: {start_page + 1} - {end_page}")
        
        print("PDF 按书签拆分完成！")

    @staticmethod
    def merge_pdfs(pdf_files, output_path):
        """
        合并多个 PDF 文件为一个 PDF 文件
        :param pdf_files: 待合并的 PDF 文件路径列表
        :param output_path: 合并后 PDF 文件的保存路径
        """
        try:
            writer = PdfWriter()

            for file in pdf_files:
                try:
                    reader = PdfReader(file)
                    for page in reader.pages:
                        writer.add_page(page)
                    print(f"成功合并: {file}")
                except Exception as e:
                    print(f"读取文件 {file} 时出错: {e}")
            
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
            
            print(f"合并完成！合并文件已保存为: {output_path}")

        except Exception as e:
            print(f"合并过程中发生错误: {e}")


# 使用示例
if __name__ == "__main__":
    # 获取页数示例
    pdf_files = ["1729_ftp.pdf", "9422_ftp.pdf", "9436_ftp.pdf"]
    for file in pdf_files:
        page_count = PDFProcessor.get_pdf_page_count(file)
        if page_count is not None:
            print(f"{file} 的总页数是: {page_count}")
    
    # 合并 PDF 示例
    PDFProcessor.merge_pdfs(pdf_files, "merged.pdf")
    
    # 按页数拆分示例
    PDFProcessor.split_pdf_by_pages("merged_page.pdf", pages_per_split=3)
    
    # 按大小拆分示例
    PDFProcessor.split_pdf_by_size("merged_size.pdf", max_size_kb=256)
    
    # # 按书签拆分示例
    PDFProcessor.split_pdf_by_bookmarks("merged_withbookmarks.pdf") 