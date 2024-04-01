print("encrypted pdf")
#pip install PyPDF2
from PyPDF4 import PdfFileWriter, PdfFileReader

#pdf write instance
writer = PdfFileWriter()

#file that you want to encrypt
file = "/Users/adrianorastean/Downloads/Doc1.pdf"

#pdf reader instance
reader = PdfFileReader(file)

#get all pdf pages
for page in range (reader.numPages):
    writer.addPage(reader.getPage(page))

#encrypt pdf with password
writer.encrypt('Absorin27')

#create new file with name as encrypted_file
#and write the pdf page into it

with open(f'/Users/adrianorastean/Downloads/Doc1.pdf', 'wb') as file:
    writer.write(file)
    file.close()
    print('File Encrypted')