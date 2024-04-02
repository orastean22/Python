import pytesseract
from PIL import Image

# Open the image
image = Image.open("/Users/adrianorastean/Downloads/SPI1.jpeg")

# Perform OCR
text = pytesseract.image_to_string(image)

# Print the extracted text
print(text)
