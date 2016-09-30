# ZipMerge Project

What is this thing?
- A small wrapper to the python libraries 'ZipFile' & 'PyPDF2'
- An api allowing one to pass in a list of tuples in the form of ('source file path', 'destination file path') 
- The source files are merged or zipped with their corresponding destination files
- The return value will be a list of the new files (essentially a distinct list of the destination file paths)



Example:

	zipmerge = ZipMerge()	
	
	hello_world_pdf = '\\users\\jschmow\\desktop\\hello_world.pdf'
	foobar_zip = '\\users\\jschmow\\desktop\\foobar.zip'	
	
	files = [('\\users\\jschmow\\desktop\\hello.pdf', hello_world_pdf),
			 ('\\users\\jschmow\\desktop\\world.pdf', hello_world_pdf)]
			 
	print(zipmerge.run(files))   #prints '\\users\\jschmow\\desktop\\hello_world.pdf'

	files = [(hello_world_pdf, foobar_zip),
			 ('\\users\\jschmow\\desktop\\world.png', foobar_zip),
			 ('\\users\\jschmow\\desktop\\other_files', foobar_zip)]		
			 
	print(zipmerge.run(files))   #prints '\\users\\jschmow\\desktop\\foobar.zip'