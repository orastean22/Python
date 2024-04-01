print("decrypted pdf")
from PyPDF4 import PdfFileWriter, PdfFileReader

#pdf write instance
writer = PdfFileWriter()

#file that you want to decrypt
file = "/Users/adrianorastean/Downloads/Doc1.pdf"

#pdf reader instance
reader = PdfFileReader(file)
if reader.isEncrypted:
    #decrypt pdf with password
    reader.decrypt('Absorin27')
    #get all pdf pages
    for page in range (reader.numPages):
        writer.addPage(reader.getPage(page))
    #create new file with name as encrypted_files   
    #and write the pdf pages into it
    with open(f'/Users/adrianorastean/Downloads/Doc1.pdf', 'wb') as file:
        writer.write(file)
        file.close()
    print('File Decrypted')
else:
    print('File has no encryption')