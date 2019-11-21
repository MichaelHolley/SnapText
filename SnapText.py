# image-manipulation
import cv2
import numpy as np
from pytesseract import image_to_string
from PIL import ImageGrab

# image-save
import os
from datetime import datetime

# GUI
from tkinter import *
from tkinter import filedialog

image = None


class Rectangle:

    def __init__(self, x_=0, y_=0, w_=0, h_=0):
        self.x = x_
        self.y = y_
        self.w = w_
        self.h = h_

    def get_leftUpper(self):
        x, y = self.x, self.y  # Standard-Fall
        if self.w < 0:
            x = self.x + self.w
        if self.h < 0:
            y = self.y + self.h
        return (x, y)

    def get_rightLower(self):
        x, y = self.x + self.w, self.y + self.h  # Standard-Fall
        if self.w < 0:
            x = self.x
        if self.h < 0:
            y = self.y
        return (x, y)

    def get_width(self):
        return self.w

    def get_height(self):
        return self.h


def screenshot():
    close_window()
    global image
    image = ImageGrab.grab()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


def select_image():
    global image
    filePath = filedialog.askopenfilename(initialdir="C:\\", title="Select input-file",
                                          filetypes=(("input-file", "*.png *.jpg *.jpeg"), ("all files", "*.*")))
    print("Selected image: \t" + filePath)
    image = cv2.imread(filePath)
    close_window()


def close_window():
    window.destroy()


window = Tk()
window.title("SnapText OCR")
frame = Frame(window)
window.geometry("100x100")
window.resizable(0, 0)
frame.pack()
imageGrabButton = Button(frame, text="Screenshot", command=screenshot, width=10).grid(row=0, column=0)
takenImageButton = Button(frame, text="Select Image", command=select_image, width=10).grid(row=1, column=0)
closeButton = Button(frame, text="Close", command=sys.exit, width=10).grid(row=3, column=0)
window.mainloop()


roi = Rectangle()
isPressed = False


def selectRegion(event, x, y, flags, param):
    global roi, isPressed  # Access to variable

    # Left-Mouse-Button -> Pressed
    if event == cv2.EVENT_LBUTTONDOWN:
        roi.x = x
        roi.y = y
        isPressed = True

    # Left-Mouse-Button -> Released
    if event == cv2.EVENT_LBUTTONUP:
        isPressed = False

    # Left-Mouse-Button -> Hold
    if isPressed:
        roi.w = x - roi.x
        roi.h = y - roi.y

def copyToClipboard(text):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(text)
    r.destroy()

cv2.namedWindow('Screenshot')
cv2.setMouseCallback('Screenshot', selectRegion)

while True:
    image_copy = np.array(image)
    cv2.rectangle(image_copy, roi.get_leftUpper(), roi.get_rightLower(), (0, 255, 0))
    cv2.imshow('Screenshot', image_copy)

    key = cv2.waitKey(1) & 0xFF  # wait one second
    if key == 115:  # S-Key
        x1, y1 = roi.get_leftUpper()
        x2, y2 = roi.get_rightLower()

        image_region = image[y1:y2, x1:x2]

        cv2.destroyWindow('Screenshot')
        cv2.imshow('Screenshot Region', image_region)

        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # Project-Root
        snap_dirPath = ROOT_DIR + "/SnapHistory/"
        if not os.path.exists(snap_dirPath):
            os.makedirs(snap_dirPath)

        cv2.imwrite(ROOT_DIR + "/SnapHistory/" + datetime.now().strftime("%Y-%d-%m_%H-%M-%S") + ".png",
                    image_region)

        textInImage = image_to_string(image_region)
        copyToClipboard(textInImage)
        print(textInImage)
        break;
    if key == 27:  # ESC-Key -> Stop
        break

cv2.waitKey(0)
cv2.destroyAllWindows()

'''
        This is a teststring
        just try it with me instead of code
        Maybe this will work better
        Come on
        This has to work properly
        
        IT IS POSSIBLE THAT CAPS WILL DO BETTER
        
        you have to try numbers too 1 2 3 4 5 6 7 8 9
'''
