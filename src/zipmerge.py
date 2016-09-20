import os
class ImportManager(object):
    ''' This class is not really needed but made it convenient for mocking in 
        the unittest (I didn't like patch for this)... Otherwise, I would have 
        just initialize the types from external libraries where they are used '''
    
    def get_pdf_file_merger(self):
        from PyPDF2.merger import PdfFileMerger
        return PdfFileMerger()
    
    def get_pdf_file_reader(self, fpath):
        from PyPDF2.pdf import PdfFileReader
        return PdfFileReader(fpath)
    
    def get_zip_file(self, fpath, mode):
        from zipfile import ZipFile
        return ZipFile(fpath, mode)
    
    def get_temporary_file(self):
        from tempfile import TemporaryFile
        return TemporaryFile(mode='w')
    
    

class ZipMergeFile(object):
    
    def __init__(self, actual_path, symbolic_path, is_parent=False):
        self.actual_path = actual_path
        self.symbolic_path = symbolic_path.lower()
        self.is_parent = is_parent
        self.has_parent = False

    @property
    def ext(self):
        _, ext = os.path.splitext(self.actual_path)
        return ext
        
        
class ZipMerge(object):
    
    def __init__(self, import_manager=None):
        self.import_manager = import_manager or ImportManager()
    
    
    def run(self, zip_merge_files):
        files = zip_merge_files
        parents = [p for p in files if p.is_parent]
        parents = self._sort_by_longest_to_shortest(parents) #depth first
        for parent in parents:
            kids = self.find_children(parent, files)
            parent = self._consolidate(parent, kids)
            files = self._pop_kids(kids, files)
        return [f for f in files if not f.has_parent]

    def _sort_by_longest_to_shortest(self, zip_merge_files):
        return sorted(zip_merge_files, key=lambda x : len(x.symbolic_path), reverse=True)
            
    def find_children(self, parent, zip_merge_files):
        results = []
        for f in zip_merge_files:
            if f.symbolic_path.startswith(parent.symbolic_path) and f.symbolic_path != parent.symbolic_path:
                results.append(f)
        return results
            
    def _consolidate(self, parent, kids):
        m = {'.pdf': PDFConsolidator, '.zip': ZipFileConsolidator}
        c = m.get(parent.ext, ZipFileConsolidator)(self.import_manager)
        return c.consolidate(parent, kids)
        
    def _pop_kids(self, kids, files):
        return list(set(files) - set(kids))
    

class PDFConsolidator(object):
    
    def __init__(self, import_manager):
        self.import_manager = import_manager
    
    def consolidate(self, parent, kids):
        parent.actual_path = parent.actual_path or self.import_manager().get_temporary_file()
        kids = sorted(kids, key=lambda x : x.symbolic_path)
        if os.path.exists(parent.actual_path):
            os.remove(parent.actual_path)        
        merger = self.import_manager.get_pdf_file_merger()
        for f in kids:
            isinstance(f, ZipMergeFile)
            merger.append(self.import_manager.get_pdf_file_reader(f.actual_path))
            f.has_parent = True
        merger.write(parent.actual_path)
        return parent
    
        
class ZipFileConsolidator(object):
    
    def __init__(self, import_manager):
        self.import_manager = import_manager
    
    def consolidate(self, parent, kids):
        parent.actual_path = parent.actual_path or self.import_manager().get_temporary_file()
        kids = sorted(kids, key=lambda x : x.symbolic_path)
        if os.path.exists(parent.actual_path):
            os.remove(parent.actual_path)
        zipper = self.import_manager.get_zip_file(parent.actual_path, "w")
        for f in kids:
            _, fname = os.path.split(f.actual_path)
            zipper.write(filename=f.actual_path, arcname=fname, compress_type=None)
            f.has_parent = True
        return parent


class ZipMergeInputValidator(object):
    supported_types = ['zip', 'pdf']
    
    def validate(self, zip_merge_files):
        errors = []
        errors.append(self._check_parent_file_types_are_supported(zip_merge_files))
        errors.append(self._check_pdf_children(zip_merge_files))
        errors = [e for e in errors if e]
        if errors:
            print(errors)
            return False        

    def _check_parent_file_types_are_supported(self, zip_merge_files):
        for f in [f for f in zip_merge_files if f.is_parent]:
            if f.ext not in self.supported_types:
                return 'ZipMergeInputValidator - unsupported file type: {0}'.format(f.actual_path)
        return ''

    def _check_pdf_children(self, zip_merge_files):
        for f in [f for f in zip_merge_files if f.is_parent and f.ext == 'pdf']:
            kids = ZipMerge.find_children(f, zip_merge_files)
            kids = [f for f in kids if f.ext != 'pdf']
            if kids:
                return 'ZipMergeInputValidator - Cannot merge non-pdfs with pdf'
        return ''
            
        
        