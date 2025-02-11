import os
import unittest
from hjimi_pdf_processor import PDFProcessor

class TestPDFProcessor(unittest.TestCase):
    def setUp(self):
        """
        测试前的准备工作
        创建测试用的 PDF 文件
        """
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_file = os.path.join(self.test_dir, "test.pdf")
        self.merged_file = os.path.join(self.test_dir, "merged.pdf")
        self.test_files = [
            os.path.join(self.test_dir, "test1.pdf"),
            os.path.join(self.test_dir, "test2.pdf")
        ]

    def test_sanitize_filename(self):
        """测试文件名清理功能"""
        test_cases = [
            ("file:1.pdf", "file_1.pdf"),
            ("test*.pdf", "test_.pdf"),
            ("doc/test.pdf", "doc_test.pdf"),
            ('test"file.pdf', "test_file.pdf"),
            ("test<>file.pdf", "test__file.pdf")
        ]
        
        for input_name, expected in test_cases:
            result = PDFProcessor.sanitize_filename(input_name)
            self.assertEqual(result, expected)

    def test_get_pdf_page_count(self):
        """测试获取 PDF 页数功能"""
        # 需要确保测试文件存在
        if os.path.exists(self.test_file):
            page_count = PDFProcessor.get_pdf_page_count(self.test_file)
            self.assertIsNotNone(page_count)
            self.assertIsInstance(page_count, int)
        else:
            self.skipTest("测试 PDF 文件不存在")

    def test_split_pdf_by_size(self):
        """测试按大小分割 PDF"""
        if os.path.exists(self.test_file):
            PDFProcessor.split_pdf_by_size(self.test_file, 100)
            # 检查是否生成了分割后的文件
            base_name = self.test_file.replace('.pdf', '')
            split_file = f"{base_name}_part_0.pdf"
            self.assertTrue(os.path.exists(split_file))
            # 清理测试文件
            if os.path.exists(split_file):
                os.remove(split_file)
        else:
            self.skipTest("测试 PDF 文件不存在")

    def test_split_pdf_by_pages(self):
        """测试按页数分割 PDF"""
        if os.path.exists(self.test_file):
            PDFProcessor.split_pdf_by_pages(self.test_file, 1)
            # 检查是否生成了分割后的文件
            base_name = self.test_file.replace('.pdf', '')
            split_file = f"{base_name}_part_1.pdf"
            self.assertTrue(os.path.exists(split_file))
            # 清理测试文件
            if os.path.exists(split_file):
                os.remove(split_file)
        else:
            self.skipTest("测试 PDF 文件不存在")

    def test_merge_pdfs(self):
        """测试合并 PDF"""
        # 检查是否有测试文件可用
        test_files_exist = all(os.path.exists(f) for f in self.test_files)
        if test_files_exist:
            PDFProcessor.merge_pdfs(self.test_files, self.merged_file)
            self.assertTrue(os.path.exists(self.merged_file))
            # 清理合并后的文件
            if os.path.exists(self.merged_file):
                os.remove(self.merged_file)
        else:
            self.skipTest("测试 PDF 文件不存在")

    def tearDown(self):
        """
        测试后的清理工作
        删除测试过程中生成的文件
        """
        files_to_clean = [
            self.merged_file,
            *[f"{self.test_file.replace('.pdf', '')}_part_{i}.pdf" 
              for i in range(5)]  # 清理可能的分割文件
        ]
        
        for file in files_to_clean:
            if os.path.exists(file):
                os.remove(file)

if __name__ == '__main__':
    unittest.main() 