import os

class ZipMergeFileAccessException(Exception): pass

class DependencyManager(object):
    ''' This class is not really needed but made it convenient for 
        mocking in the unit test... by indirectly using dependencies 
        thru this class and injecting it to other classes, mocking 
        the dependencies becomes easy.  patching is another option,
        but I think it would have made the unit test ugly.'''
    
    def get_pdf_file_merger(self, fpath):
        if os.path.exists(fpath):
            raise ZipMergeFileAccessException("Cannot overwrite/append to existing pdf file: '{0}'".format(fpath))
        from PyPDF2.merger import PdfFileMerger
        return PdfFileMerger()
    
    def get_pdf_file_reader(self, fpath):
        from PyPDF2.pdf import PdfFileReader
        return PdfFileReader(open(fpath, 'rb'))
    
    def get_zip_file(self, fpath, mode):
        if os.path.exists(fpath):
            raise ZipMergeFileAccessException("Cannot overwrite/append to existing zip file: '{0}'".format(fpath))
        from zipfile import ZipFile
        return ZipFile(fpath, mode)
    
    def get_copyfile_func(self):
        from shutil import copyfile
        return copyfile
    
    def upsert_parent_directory(self, fpath):
        d, _ = os.path.split(fpath)
        if not os.path.exists(d):
            os.makedirs(d)
            
    def os_path_exists(self, path):
        return os.path.exists(path)
            
    def log(self, msg):
        print(msg)
    
    

class ZipMergeFile(object):
    def __init__(self, source_path, dest_path):
        self.source_path = source_path
        self.dest_path = dest_path.lower()

    @property
    def dest_ext(self):
        _, ext = os.path.splitext(self.dest_path)
        return ext
    
    @property
    def name(self):
        _, fname = os.path.split(self.source_path.replace('\\', '/'))
        return fname
        
                
        
class ZipMerge(object):
    
    def __init__(self, dependency_manager=None):
        self.dependency_manager = dependency_manager or DependencyManager()
        self.consolidators = {'.pdf': PDFConsolidator, '.zip': ZipConsolidator}
    
    def run(self, file_mappings):
        '''
        :param file_mappings: list of tuples like ('/file/path/fname.txt', 'archive/path/fname.txt')
        :return: A list of file paths for the new files
        '''
        zip_merge_files = [ZipMergeFile(t[0], t[1]) for t in file_mappings]
        self._verify_source_files(zip_merge_files)
        pdfs = [f for f in zip_merge_files if f.dest_ext == '.pdf']
        zips = [f for f in zip_merge_files if f.dest_ext == '.zip']
        new_files = PDFConsolidator(self.dependency_manager).consolidate(pdfs, new_files=[])
        new_files = ZipConsolidator(self.dependency_manager).consolidate(zips, new_files)
        return new_files
    
    def _verify_source_files(self, zip_merge_files):
        for o in zip_merge_files:
            if not self.dependency_manager.os_path_exists(o.source_path):
                raise ZipMergeFileAccessException("Unable to locate file: '{0}'".format(o.source_path))
        
            

class ZipMergeFileHasher(object):
    @classmethod
    def hash(cls, zip_merge_files):
        dest_hash = {}
        for f in zip_merge_files:
            if f.dest_path not in dest_hash:
                dest_hash[f.dest_path] = []
            dest_hash[f.dest_path].append(f)
        return dest_hash


class IFileConsolidator(object):
    def __init__(self, dependency_manager):
        self.dependency_manager = dependency_manager
        
    def consolidate(self, zip_merge_file):
        raise NotImplementedError
    
    
    
class PDFConsolidator(IFileConsolidator):
    def __init__(self, dependency_manager):
        super(PDFConsolidator, self).__init__(dependency_manager)
    
    def consolidate(self, zip_merge_files, new_files):
        hashed = ZipMergeFileHasher.hash(zip_merge_files)
        for dest_path, files in hashed.items():
            self.dependency_manager.upsert_parent_directory(dest_path)
            merger = self.dependency_manager.get_pdf_file_merger(dest_path)
            for o in files:
                merger.append(self.dependency_manager.get_pdf_file_reader(o.source_path), import_bookmarks=False)
            merger.write(dest_path)
            new_files.append(dest_path)
        return new_files
    
    
    
class ZipConsolidator(IFileConsolidator):
    def __init__(self, dependency_manager):
        super(ZipConsolidator, self).__init__(dependency_manager)
    
    def consolidate(self, zip_merge_files, new_files):
        hashed = ZipMergeFileHasher.hash(zip_merge_files)
        for dest_path, files in hashed.items():
            self.dependency_manager.upsert_parent_directory(dest_path)
            zipper = self.dependency_manager.get_zip_file(dest_path, "a")
            files = sorted(files, key=lambda f: len(f.dest_path))
            self._zip_dirs(zipper, files)
            self._zip_files(zipper, files)
            zipper.close()
            new_files.append(dest_path)
        return new_files
    
    def _zip_files(self, zipper, zip_merge_files):
        files = [o for o in zip_merge_files if not os.path.isdir(o.source_path)]
        for o in files:
            zipper.write(filename=o.source_path, arcname=o.name, compress_type=None)
        
    def _zip_dirs(self, zipper, zip_merge_files):
        files = [o for o in zip_merge_files if os.path.isdir(o.source_path)]
        for o in files:
            for root, _, files in os.walk(o.source_path):
                for fname in files:
                    fpath = os.path.join(root, fname)
                    parent, _ = os.path.split(o.source_path)
                    rel_dir = root[len(parent):]
                    arcname = os.path.join(rel_dir, fname)
                    zipper.write(filename=fpath, arcname=arcname, compress_type=None)
        

        
