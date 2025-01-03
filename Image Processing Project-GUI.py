import cv2
import pytesseract
import numpy as np
import imutils
import re
from pathlib import Path
from tkinter import filedialog, Button, Tk, Label,PhotoImage,Frame
from PIL import ImageTk, Image
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preProcess(img):
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #greyscale
    blur = cv2.blur(gray_image,(2,2)) #blurring
    inverted = 256- 1 - blur #inverting
    return inverted

def getContours(img):
    edged = cv2.Canny(img, 30, 200) #Edge detection
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #Find contours 
    contours = imutils.grab_contours(keypoints) #Grab contours 
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10] #Sort contours
    
    #Looping over our contours to find the best possible approximate contour of 10 contours
    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break
    return location

def getplate(img,location):
    mask = np.zeros(img.shape, np.uint8) #create blank image with same dimensions as the original image
    new_image = cv2.drawContours(mask, [location], 0,255, -1) #Draw contours on the mask image
    new_image = cv2.bitwise_and(img, img, mask=mask) #Take bitwise AND between the original image and mask image
    (x,y) = np.where(mask==255) #Find the co-ordinates of the four corners of the document
    (x1, y1) = (np.min(x), np.min(y)) #Find the top left corner
    (x2, y2) = (np.max(x), np.max(y)) #Find the bottom right corner
    cropped_image = img[x1:x2+1, y1:y2+1] #Crop the image using the co-ordinates
    return cropped_image

def readplate(img):
    preProcessed_img=preProcess(img)
    contours=getContours(preProcessed_img)
    try:
        plate=getplate(preProcessed_img,contours)
        data = pytesseract.image_to_string(plate, lang='eng', config='--oem 3 --psm 7 tessedit_char_whitelist=-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        #specifying pystesseract configure
        #--oem 3 => Using default engine
        #--psm 7 => Treating the image as a single text line.
        #tessedit_char_whitelist=-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ => Specifying characters to recognize
        data=re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', data)
        #cleaning text using regular expressions to increase accuracy
        return data
    except:
        return "No plate detected"        

def upload_image():
    file_path = filedialog.askopenfilename()
    
    if file_path:
        img = cv2.imread(file_path)
        root.geometry("700x500")
        frame = Frame(root, width=600, height=400)
        frame.pack()
        frame.place(anchor='center', relx=0.5, rely=0.5)

        image_display=Image.open(file_path)
        image_display = image_display.resize((400, 300), Image.Resampling.LANCZOS)
        photo_image = ImageTk.PhotoImage(image_display)

        image_label = Label(frame, image=photo_image)
        # Create an object of tkinter ImageTk
        image_label.image = photo_image 
        image_label.pack(expand=1, fill='none')
        text=readplate(cv2.imread(file_path))
        plate_number_label.config(text=f"Plate Number: {text.strip()}")


root = Tk()
root.title('License Plate Recognition')
root.configure(bg="#2C3E50")
root.minsize(300,100)
  

button_style = {
    "bg": "#E74C3C", 
    "fg": "white",  
    "font": ("Helvetica", 12), 
    "relief": "raised",  
    "bd": 5,  
    "width": 20  
}

upload_button = Button(root, text="Upload Image", command=upload_image, **button_style)
upload_button.pack(pady=30)  

plate_number_label = Label(root, text="Plate Number: ", bg="#2C3E50", fg="#ECF0F1", font=("Helvetica", 14))
plate_number_label.pack(pady=30,side='bottom')

root.mainloop()




