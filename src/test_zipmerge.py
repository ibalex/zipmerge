import unittest
from src import zipmerge
from unittest.mock import Mock
from src.zipmerge import ZipMerge, ZipFileConsolidator, PDFConsolidator,\
    ZipMergeFile


class Test(unittest.TestCase):


    def setUp(self):
        self.zip_file_class = Mock()
        self.temp_file_class = Mock()
        self.pdf_file_merger_class = Mock()
        self.pdf_file_reader_class = Mock()
        self.pdf_consolidator = PDFConsolidator(self.pdf_file_merger_class, self.pdf_file_reader_class)
        self.zip_file_consolidator = ZipFileConsolidator(self.zip_file_class, self.temp_file_class)
        self.zipmerge = ZipMerge(self.pdf_consolidator, self.zip_file_consolidator)

    def test_simple_pdf_merge(self):
        files = [ZipMergeFile('\\fake\\file\\path1\\merged.pdf', 'merged.pdf/a.pdf', is_parent=True),
                 ZipMergeFile('\\fake\\file\\path1\\a.pdf', 'merged.pdf/a.pdf', is_parent=False),
                 ZipMergeFile('\\fake\\file\\path2\\b.pdf', 'merged.pdf/b.pdf', is_parent=False),
                 ZipMergeFile('\\fake\\file\\path2\\c.pdf', 'merged.pdf/c.pdf', is_parent=False)]
        expected = files[0]
        actual = self.zipmerge.run(files)
        self.assertEquals(actual, expected)

#     def test_simple_zip_merge(self):
#         assert(False)
#     
#     def test_simple_pdf_and_zip_merge(self):
#         assert(False)
#         
#     def test_nested_pdf_merge(self):
#         assert(False)    
# 
#     def test_nested_zip_merge(self):
#         assert(False)  
#         
#     def test_nested_pdf_and_zip_merge(self):
#         assert(False)
        
        
    #------ negative scenarios ------#
#     def test_pdf_merge_with_non_pdf(self):
#         assert(False)
# 
#     def test_pdf_merge_with_nothing(self):
#         assert(False)
#         
#     def test_zip_merge_with_nothing(self):
#         assert(False)
        
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()