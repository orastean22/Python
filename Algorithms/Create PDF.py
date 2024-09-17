# Use python to create an PDF file
# pip install reportlab
# Version V0.1
# Author: AdrianO
# Update 17.09.2024


from reportlab.pdfgen import canvas

# Create a new PDF file
pdf_file = canvas.Canvas("AdrianO.pdf")

# Add text to the pdf file
pdf_file.drawString(72,720,"Hello Word")
pdf_file.drawString(72,700,"Free pdf document")
pdf_file.drawString(72,680,"Like | Share")
pdf_file.drawString(72,660,"Subscribe")
pdf_file.drawString(72,640,"clcoding.com")
pdf_file.drawString(72,620,"Thank you")

# Save the PDF file
pdf_file.save()


