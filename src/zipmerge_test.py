from src.zipmerge import ZipMerge, ZipMergeFile
from mock import Mock, call
import unittest


class TestZipMerge(unittest.TestCase):
    
    def setUp(self):
        self.zipmerge = ZipMerge()
        self.pdf_file_merger_mock = Mock()
        self.pdf_file_reader_mock = Mock()
        self.zip_file_mock = Mock()
        self.temp_file_mock = Mock()
        dependancy_mgr_mock = Mock()
        dependancy_mgr_mock.get_pdf_file_merger.return_value = self.pdf_file_merger_mock 
        dependancy_mgr_mock.get_pdf_file_reader.return_value = self.pdf_file_reader_mock
        dependancy_mgr_mock.get_zip_file.return_value = self.zip_file_mock
        dependancy_mgr_mock.get_temporary_file.return_value = self.temp_file_mock
        dependancy_mgr_mock.os_remove_if_exists = lambda x : None
        self.zipmerge = ZipMerge(dependancy_mgr_mock)
        
    
    def test_simple_pdf_merge(self):       
        # This use case merges 3 pdf's into a single new pdf that didn't exist before (it also leaves the seprate pdf's untouched)
        files = [ZipMergeFile('\\fake\\file\\path1\\merged.pdf', 'merged.pdf', is_parent=True),
                 ZipMergeFile('\\fake\\file\\path1\\a.pdf', 'merged.pdf/a.pdf', is_parent=False),
                 ZipMergeFile('\\fake\\file\\path2\\b.pdf', 'merged.pdf/b.pdf', is_parent=False),
                 ZipMergeFile('\\fake\\file\\path2\\c.pdf', 'merged.pdf/c.pdf', is_parent=False)]
        results = self.zipmerge.run(files)
        actual = results[0]
        expected = files[0]
        self.assertEqual=(actual, expected)
        
        # Below I verify the behavior and usage of the PdfFileMerger & PdfFileReader API's
        # Typically I avoid testing my implementation but we can't test the real API's so this is a consolation 
        self.assertEquals(self.pdf_file_merger_mock.append.call_count, len([f for f in files if not f.is_parent]))
        new_file = files[0].source_path
        self.pdf_file_merger_mock.write.assert_called_once_with(new_file)


    def test_simple_zip_merge(self):
        files = [ZipMergeFile('\\fake\\file\\path1\\merged.zip', 'merged.zip', is_parent=True),
        ZipMergeFile('\\fake\\file\\path1\\a.zip', 'merged.zip/a.zip', is_parent=False),
        ZipMergeFile('\\fake\\file\\path2\\b.zip', 'merged.zip/b.zip', is_parent=False),
        ZipMergeFile('\\fake\\file\\path2\\c.zip', 'merged.zip/c.zip', is_parent=False)]
        results = self.zipmerge.run(files)
        actual = results[0]
        expected = files[0]
        self.assertEqual=(actual, expected)

        # Reluctantly testing behavior again
        self.assertEquals(self.zip_file_mock.write.call_count, len([f for f in files if not f.is_parent]))
        calls = [call(arcname=files[1].name, compress_type=None, filename=files[1].source_path),
                 call(arcname=files[2].name, compress_type=None, filename=files[2].source_path),
                 call(arcname=files[3].name, compress_type=None, filename=files[3].source_path)]
        self.zip_file_mock.write.assert_has_calls(calls)
        
     
#     def test_simple_pdf_merge_and_zip_merge(self):
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