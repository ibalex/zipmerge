from src.zipmerge import ZipMerge, ZipMergeFileAccessException
from mock import Mock, call
import unittest


class TestZipMerge(unittest.TestCase):
    
    def setUp(self):
        self.zipmerge = ZipMerge()
        self.pdf_file_merger_mock = Mock()
        self.pdf_file_reader_mock = Mock()
        self.zip_file_mock = Mock()
        self.temp_file_mock = Mock()
        self.dependency_mgr_mock = Mock()
        self.dependency_mgr_mock.get_pdf_file_merger.return_value = self.pdf_file_merger_mock 
        self.dependency_mgr_mock.get_pdf_file_reader.return_value = self.pdf_file_reader_mock
        self.dependency_mgr_mock.get_zip_file.return_value = self.zip_file_mock
        self.dependency_mgr_mock.get_temporary_file.return_value = self.temp_file_mock
        self.dependency_mgr_mock.os_remove_if_exists = lambda x : None
        self.zipmerge = ZipMerge(self.dependency_mgr_mock)
        
    
    def test_simple_pdf_merge(self):       
        # This use case merges 3 pdf's into a single new pdf that didn't exist before (it also leaves the seprate pdf's untouched)
        dest_path = "\\fake\\file\\path1\\merged.pdf"
        files = [('\\fake\\file\\path1\\a.pdf', dest_path),
                 ('\\fake\\file\\path2\\b.pdf', dest_path),
                 ('\\fake\\file\\path2\\c.pdf', dest_path)]
        actual = self.zipmerge.run(files)
        expected = [dest_path]
        self.assertEqual=(actual, expected)
        
        # Verify the usage of the PdfFileMerger & PdfFileReader API's because 
        # they are Mocks and we have no actual results to test
        self.assertEquals(self.pdf_file_merger_mock.append.call_count, len(files))
        self.pdf_file_merger_mock.write.assert_called_once_with(dest_path)


    def test_simple_zip_merge(self):
        src = '\\fake\\file\\path\\'
        fa, fb, fc = 'a.zip', 'b.zip', 'c.zip'
        s1, s2, s3 = src+fa, src+fb, src+fc
        dest_path = "\\fake\\file\\path99\\merged.zip"
        files = [(s1, dest_path), (s2, dest_path), (s3, dest_path)]
        actual = self.zipmerge.run(files)
        expected = [dest_path]
        self.assertEqual=(actual, expected)

        # Reluctantly testing behavior again
        self.assertEquals(self.zip_file_mock.write.call_count, len(files))
        calls = [call(arcname=fa, compress_type=None, filename=s1),
                 call(arcname=fb, compress_type=None, filename=s2),
                 call(arcname=fc, compress_type=None, filename=s3)]
        self.zip_file_mock.write.assert_has_calls(calls)
        
     
#     def test_simple_pdf_merge_and_zip_merge(self):
#         assert(False)
#         
#     def test_zip_files_When_one_is_directory_with_children(self):
#         assert(False)    
# 
        
    #------ negative scenarios ------#
    def test_exception_when_missing_source_file(self):
        self.dependency_mgr_mock.os_path_exists.return_value = False
        dest_path = "\\fake\\file\\path1\\merged.pdf"
        files = [('\\fake\\file\\path1\\a.pdf', dest_path),
                 ('\\fake\\file\\path2\\b.pdf', dest_path)]
        self.assertRaises(ZipMergeFileAccessException, self.zipmerge.run, files)
    
#     @patch('src.zipmerge.os.path')
#     def test_exception_when_dest_pdf_exists(self, ospath_mock):
#         ospath_mock.exists.return_value = True
#         ospath_mock.splitext.return_value = ("what", "ever")
#         ospath_mock.split.return_value = ("what", "ever")
#         self.dependency_mgr_mock.get_pdf_file_merger = DependencyManager().get_pdf_file_merger
#         dest_path = "\\fake\\file\\path1\\merged.pdf"
#         files = [ZipMergeFile('\\fake\\file\\path1\\a.pdf', dest_path),
#                  ZipMergeFile('\\fake\\file\\path2\\b.pdf', dest_path)]
#         self.assertRaises(ZipMergeFileAccessException, self.zipmerge.run, files)
#          
#     def test_exception_when_dest_zip_exists(self):
#         assert(False)
        
        
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()