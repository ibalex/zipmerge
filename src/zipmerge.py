import os

class DependancyManager(object):
    ''' This class is not really needed but made it convenient for 
        mocking in the unit test... by indirectly using dependencies 
        thru this class and injecting it to other classes, mocking 
        the dependencies becomes easy.  We could have used patch 
        but I think it would have made the unit test too ugly.'''
    
    def get_pdf_file_merger(self):
        from PyPDF2.merger import PdfFileMerger
        return PdfFileMerger()
    
    def get_pdf_file_reader(self, fpath):
        from PyPDF2.pdf import PdfFileReader
        return PdfFileReader(file(fpath, 'rb'))
    
    def get_zip_file(self, fpath, mode):
        from zipfile import ZipFile
        return ZipFile(fpath, mode)
    
    def get_temp_file_path(self, fname):
        import tempfile
        d = tempfile.gettempdir()
        return os.path.join(d, fname)
    
    def os_remove_if_exists(self, fpath):
        if os.path.exists(fpath): 
            os.remove(fpath)
            
    def log(self, msg):
        print(msg)
    
    

class ZipMergeFile(object):
    def __init__(self, source_path, dest_path, is_parent=False):
        self.source_path = source_path
        self.dest_path = dest_path.lower()
        self.is_parent = is_parent
        self.has_parent = False

    @property
    def ext(self):
        _, ext = os.path.splitext(self.dest_path)
        return ext
    
    @property
    def name(self):
        _, fname = os.path.split(self.dest_path)
        return fname
        
        
        
class ZipMerge(object):
    
    def __init__(self, dependancy_manager=None):
        self.dependancy_manager = dependancy_manager or DependancyManager()
    
    
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
        return sorted(zip_merge_files, key=lambda x : len(x.dest_path), reverse=True)
            
    def find_children(self, parent, zip_merge_files):
        results = []
        for f in zip_merge_files:
            if f.dest_path.startswith(parent.dest_path) and f.dest_path != parent.dest_path:
                results.append(f)
        return results
            
    def _consolidate(self, parent, kids):
        m = {'.pdf': PDFConsolidator, '.zip': ZipFileConsolidator}
        c = m.get(parent.ext, ZipFileConsolidator)(self.dependancy_manager)
        return c.consolidate(parent, kids)
        
    def _pop_kids(self, kids, files):
        return list(set(files) - set(kids))



class IFileConsolidator(object):
    def __init__(self, dependancy_manager):
        self.dependancy_manager = dependancy_manager
        
    def consolidate(self, parent, kids):
        ''' Override this method but call it at the start of the derived class' implementation '''
        parent.source_path = parent.source_path or self.dependancy_manager.get_temp_file_path(parent.name)
        kids = sorted(kids, key=lambda x : x.dest_path)
        self.dependancy_manager.os_remove_if_exists(parent.source_path)



class PDFConsolidator(IFileConsolidator):
    def __init__(self, dependancy_manager):
        super(PDFConsolidator, self).__init__(dependancy_manager)
    
    def consolidate(self, parent, kids):
        super(PDFConsolidator, self).consolidate(parent, kids)
        merger = self.dependancy_manager.get_pdf_file_merger()
        for f in kids:
            isinstance(f, ZipMergeFile)
            merger.append(self.dependancy_manager.get_pdf_file_reader(f.source_path), import_bookmarks=False)
            self.dependancy_manager.log("PDFConsolidator: merged {0}".format(f.source_path))
            f.has_parent = True
        merger.write(parent.source_path)
        return parent
    
   
        
class ZipFileConsolidator(IFileConsolidator):
    def __init__(self, dependancy_manager):
        super(ZipFileConsolidator, self).__init__(dependancy_manager)
    
    def consolidate(self, parent, kids):
        super(ZipFileConsolidator, self).consolidate(parent, kids)
        zipper = self.dependancy_manager.get_zip_file(parent.source_path, "w")
        for f in kids:
            zipper.write(filename=f.source_path, arcname=f.name, compress_type=None)
            self.dependancy_manager.log("ZipFileConsolidator: zipped {0}".format(f.source_path))
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
                return 'ZipMergeInputValidator - unsupported file type: {0}'.format(f.source_path)
        return ''

    def _check_pdf_children(self, zip_merge_files):
        for f in [f for f in zip_merge_files if f.is_parent and f.ext == 'pdf']:
            kids = ZipMerge.find_children(f, zip_merge_files)
            kids = [f for f in kids if f.ext != 'pdf']
            if kids:
                return 'ZipMergeInputValidator - Cannot merge non-pdfs with pdf'
        return ''
    
# To Do: PdfFileMerger doesn't support encrypted files... either decrypt them or make a validation check
#     def _check_for_ecrypted_pdfs(self):
            
        
        