from PyPDF2.merger import PdfFileMerger
from PyPDF2.pdf import PdfFileReader
from zipfile import ZipFile
import copy
import os
import tempfile


class ZipMergeFile(object):
    
    def __init__(self, actual_path, symbolic_path, is_parent=False):
        self.actual_path = actual_path
        self.symbolic_path = symbolic_path.lower()
        self.is_parent = is_parent
        self.has_parent = False

    @property
    def ext(self):
        _, ext = os.path.split(self.actual_path)
        return ext
        
        
class ZipMerge(object):
    
    def __init__(self, pdf_consolidator, zip_file_consolidator):
        self._pdf_consolidator = pdf_consolidator
        self._zip_file_consolidator = zip_file_consolidator
    
    @classmethod
    def run(cls, zip_merge_files):
        files = copy.deepcopy(zip_merge_files)
        parents = [p for p in files if p.is_parent]
        parents = cls._sort_by_longest_to_shortest(parents) #depth first
        for parent in parents:
            kids = cls._find_children(parent, files)
            parent = cls._consolidate(parent, kids)
            files = cls._pop_kids(files, kids)
        return [f for f in files if not f.has_parent]

    @classmethod
    def _sort_by_longest_to_shortest(cls, zip_merge_files):
        return sorted(zip_merge_files, key=lambda x : len(x.symbolic_path), reverse=True)
            
    @classmethod
    def _find_children(cls, parent, zip_merge_files):
        return [f for f in zip_merge_files if f.symbolic_path.startswith(parent.symbolic_path) and f.symbolic_path != parent.symbolic_path]
            
    @classmethod
    def _consolidate(cls, parent, kids):
        m = {'pdf': PDFConsolidator, 'zip': ZipFileConsolidator}
        c = m.get(parent.ext, ZipFileConsolidator)()
        return c.consolidate(parent, kids)
        
    @classmethod
    def _pop_kids(cls, kids, files):
        return list(set(files) - set(kids))
    

class PDFConsolidator(object):
    
    def __init__(self, pdf_file_merger_class=PdfFileMerger, pdf_file_reader_class=PdfFileReader):
        self._pdf_file_merger_class = pdf_file_merger_class
        self._pdf_file_reader_class = pdf_file_reader_class
    
    @classmethod
    def consolidate(cls, parent, kids):
        parent.actual_path = parent.actual_path or tempfile.TemporaryFile(mode='w')
        kids = sorted(kids, key=lambda x : x.symbolic_path)
        if os.path.exists(parent.actual_path):
            os.remove(parent.actual_path)        
        merger = cls._pdf_file_merger_class()
        for f in kids:
            isinstance(f, ZipMergeFile)
            merger.append(cls._pdf_file_reader_class(f.actual_path))
            f.has_parent = True
        merger.write(parent.actual_path)
        return parent
    
        
class ZipFileConsolidator(object):
    
    def __init__(self, zip_file_class=ZipFile, temp_file_class=tempfile.TemporaryFile):
        self._zip_file_class = zip_file_class
        self._temp_file_class = temp_file_class
    
    @classmethod
    def consolidate(cls, parent, kids):
        parent.actual_path = parent.actual_path or cls._temp_file_class(mode='w')
        kids = sorted(kids, key=lambda x : x.symbolic_path)
        if os.path.exists(parent.actual_path):
            os.remove(parent.actual_path)
        zipper = cls._zip_file_class(parent.actual_path, "w")
        for f in kids:
            zipper.write(filename=f.actual_path, arcname=parent.actual_path, compress_type=None)
            f.has_parent = True
        return parent


class ZipMergeInputValidator(object):
    supported_types = ['zip', 'pdf']
    
    @classmethod
    def validate(cls, zip_merge_files):
        errors = []
        errors.append(cls._check_parent_file_types_are_supported(zip_merge_files))
        errors.append(cls._check_pdf_children(zip_merge_files))
        errors = [e for e in errors if e]
        if errors:
            print(errors)
            return False        

    @classmethod
    def _check_parent_file_types_are_supported(cls, zip_merge_files):
        for f in [f for f in zip_merge_files if f.is_parent]:
            if f.ext not in cls.supported_types:
                return 'ZipMergeInputValidator - unsupported file type: {0}'.format(f.actual_path)
        return ''

    @classmethod
    def _check_pdf_children(cls, zip_merge_files):
        for f in [f for f in zip_merge_files if f.is_parent and f.ext == 'pdf']:
            kids = cls._find_children(f, zip_merge_files)
            kids = [f for f in kids if f.ext != 'pdf']
            if kids:
                return 'ZipMergeInputValidator - Cannot merge non-pdfs with pdf'
        return ''
            
    @classmethod
    def _find_children(cls, parent, zip_merge_files):
        return [f for f in zip_merge_files if f.symbolic_path.startswith(parent.symbolic_path) and f.symbolic_path != parent.symbolic_path]    
        
        
        