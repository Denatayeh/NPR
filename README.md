## Number Plate Recognition System
This project is a Number Plate Recognition System built with Python. It uses Pytesseract for optical character recognition (OCR) to detect and extract text from vehicle license plates.
The system features a GUI built with Tkinter for a user-friendly interaction.

### Features
- **Accurate**: This project achieved a 87% accuracy on the provided dataset. It was calculated using Levenshtein ratio (a measure of similarity between two strings, based on the Levenshtein distance).
- **License Plate Detection**: Automatically processes images to detect and recognize text from vehicle license plates.
- **Graphical User Interface**: Easy-to-use interface built with Tkinter for seamless interaction.
- **Optical Character Recognition (OCR)**: Leverages Pytesseract for efficient and accurate text extraction.

### Sample Run 
![Picture1](https://github.com/user-attachments/assets/b3b99f59-773a-47f7-92a9-db83f0e0a9de)

### Analysis
Some preprocessing is done to each image using cv2 and other libraries before sending the plate to tesseract to be read. Please refer to the [Analysis file](https://github.com/Denatayeh/NPR/blob/main/Image%20Processing%20Project%20-%20Analysis.ipynb) to view preprocessing in depth.
