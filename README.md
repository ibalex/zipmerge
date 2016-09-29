# ZipMerge Project

A small wrapper to the libraries ZipFile & PyPDF2.  It provides an api allowing one can pass in a list of tuples in the form of ('source file path', 'destination file path').  If the destination file is a pdf but then the source file must also be pdf.  However, if the destination file is a zip then the source files can be a directory, zip, or virtually any file type.  The return value will be a list of the new files that were created... There should be a new file created for each unique destination path in the list of tuples.

Example:

	zipfile = "\\users\\jschmow\\desktop\\foobar.zip"
	files = [('\\users\\jschmow\\desktop\\hello.pdf', zipfile),
			 ('\\users\\jschmow\\desktop\\world.png', zipfile),
			 ('\\users\\jschmow\\desktop\\other_files', zipfile)]
	zipmerge = ZipMerge()
	results = zipmerge.run(files)
	
	print(results)   #prints "\\users\\jschmow\\desktop\\foobar.zip"