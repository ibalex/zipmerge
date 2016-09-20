from src.zipmerge import ZipMerge, ZipMergeFile
import os




def test1():
    zm = ZipMerge()
    output_fpath = './test_pdfs/zipped.zip'
    files = [ZipMergeFile(output_fpath, "zipped.zip", is_parent=True),
             ZipMergeFile("./test_pdfs/a.pdf", "zipped.zip/a.pdf", is_parent=False),
             ZipMergeFile("./test_pdfs/b.pdf", "zipped.zip/b.pdf", is_parent=False),
             ZipMergeFile("./test_pdfs/c.pdf", "zipped.zip/c.pdf", is_parent=False)]
    _ = zm.run(files)
    result = os.path.exists(output_fpath) == True
    print("\r\n\t\tWORKED!" if result else "\r\n\t\tFAILED!")
    
    
    
    
test1()
