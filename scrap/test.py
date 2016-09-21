from src.zipmerge import ZipMerge, ZipMergeFile
import os




def scenario_1__simple_zip():
    zm = ZipMerge()
    output_fpath = './test_pdfs/zipped.zip'
    files = [ZipMergeFile(output_fpath, "zipped.zip", is_parent=True),
             ZipMergeFile("./test_pdfs/a.pdf", "zipped.zip/a.pdf", is_parent=False),
             ZipMergeFile("./test_pdfs/b.pdf", "zipped.zip/b.pdf", is_parent=False),
             ZipMergeFile("./test_pdfs/c.pdf", "zipped.zip/c.pdf", is_parent=False)]
    _ = zm.run(files)
    result = os.path.exists(output_fpath) == True
    print("\r\n\t\tWORKED!" if result else "\r\n\t\tFAILED!")
    
def scenario_2__simple_merge():
    zm = ZipMerge()
    output_fpath = './test_pdfs/merged.pdf'
    files = [ZipMergeFile(output_fpath, "merged.pdf", is_parent=True),
             ZipMergeFile("./test_pdfs/a.pdf", "merged.pdf/a.pdf", is_parent=False),
             ZipMergeFile("./test_pdfs/b.pdf", "merged.pdf/b.pdf", is_parent=False),
             ZipMergeFile("./test_pdfs/c.pdf", "merged.pdf/c.pdf", is_parent=False)]
    _ = zm.run(files)
    result = os.path.exists(output_fpath) == True
    print("\r\n\t\tWORKED!" if result else "\r\n\t\tFAILED!")    


def scenario_3__pdf_merge_and_zip_multilevel():
    zm = ZipMerge()
    output_fpath = './test_pdfs/scenario_3.zip'
    files = [ZipMergeFile(output_fpath, "scenario_3.zip", is_parent=True),
             
             ZipMergeFile('',                  "scenario_3.zip/sub_1.zip", is_parent=True),
             ZipMergeFile('./test_pdfs/a.pdf', "scenario_3.zip/sub_1.zip/a.pdf"),
             ZipMergeFile('./test_pdfs/b.pdf', "scenario_3.zip/sub_1.zip/b.pdf"),
             
             ZipMergeFile('',                  "scenario_3.zip/sub_2.zip", is_parent=True),             
             ZipMergeFile('./test_pdfs/b.pdf', "scenario_3.zip/sub_2.zip/b.pdf"),
             ZipMergeFile('./test_pdfs/c.pdf', "scenario_3.zip/sub_2.zip/c.pdf"),
             
             ZipMergeFile('',                  "scenario_3.zip/sub_2.zip/c.pdf/merged_b_and_c.pdf", is_parent=True),
             ZipMergeFile('./test_pdfs/b.pdf', "scenario_3.zip/sub_2.zip/c.pdf/merged_b_and_c.pdf/b.pdf"),
             ZipMergeFile('./test_pdfs/c.pdf', "scenario_3.zip/sub_2.zip/c.pdf/merged_b_and_c.pdf/c.pdf")]
    
    _ = zm.run(files)
    result = os.path.exists(output_fpath) == True
    print("\r\n\t\tWORKED!" if result else "\r\n\t\tFAILED!")   

    
# scenario_1__simple_zip()
# scenario_2__simple_merge()
scenario_3__pdf_merge_and_zip_multilevel()