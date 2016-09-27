from src.zipmerge import ZipMerge, ZipMergeFile
import os


def scenario_1__simple_zip_with_subdirs():
    zm = ZipMerge()
    dest_path = "./test_pdfs/scenario_1.zip"
    if os.path.exists(dest_path):
        os.remove(dest_path)
    files = [("./test_pdfs/a.pdf", dest_path),
             ("./test_pdfs/b.pdf", dest_path),
             ("./test_pdfs/c.pdf", dest_path),
             ("./test_pdfs/d", dest_path)]
    _ = zm.run(files)
    result = os.path.exists(dest_path) == True
    print("\r\n\t\tWORKED!" if result else "\r\n\t\tFAILED!")
    
    
def scenario_2__simple_merge():
    zm = ZipMerge()
    root_dir = './test_pdfs/'
    dest_path = "./test_pdfs/scenario_2.pdf"
    if os.path.exists(dest_path):
        os.remove(dest_path)
    files = [("./test_pdfs/a.pdf", dest_path),
             ("./test_pdfs/b.pdf", dest_path),
             ("./test_pdfs/c.pdf", dest_path)]
    _ = zm.run(files)
    result = os.path.exists(dest_path) == True
    print("\r\n\t\tWORKED!" if result else "\r\n\t\tFAILED!")    


def scenario_3__pdf_merge_then_zip_with_subdirs():
    zm = ZipMerge()
    root_dir = './test_pdfs/'
    dest_path1 = "./test_pdfs/scenario_3.pdf"
    dest_path2 = "./test_pdfs/scenario_3.zip"
    if os.path.exists(dest_path1):
        os.remove(dest_path1)
    if os.path.exists(dest_path2):
        os.remove(dest_path2)
    files1 = [("./test_pdfs/a.pdf", dest_path1),
             ("./test_pdfs/b.pdf", dest_path1),
             ("./test_pdfs/c.pdf", dest_path1)]
    files2 = [(dest_path1, dest_path2),
             ("./test_pdfs/a.pdf", dest_path2),
             ("./test_pdfs/b.pdf", dest_path2),
             ("./test_pdfs/c.pdf", dest_path2),
             ("./test_pdfs/d", dest_path2)]
    _ = zm.run(files1)
    _ = zm.run(files2)
    result = os.path.exists(dest_path1) == True and os.path.exists(dest_path2) == True 
    print("\r\n\t\tWORKED!" if result else "\r\n\t\tFAILED!")   



if __name__ == '__main__':
    scenario_1__simple_zip_with_subdirs()
    scenario_2__simple_merge()
    scenario_3__pdf_merge_then_zip_with_subdirs()


