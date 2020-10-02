# SnapText
This is a OCR -Tool for screenshots made with OpenCV, Python and Pillow, which is ment to recognize text in images for use with Application, Websites and Images where you are unable to copy the text by selecting it.

## Required libs:
- Pytesseract
- PIL
- Numpy
- OpenCV
- tkinter

## How to use
1. Execute and use the Application-GUI to do a screenshot or select an image
2. Select ROI and press S-Key to select
3. Press any key to stop the program
4. Copy text from the console

## Known Issues
- With multiple Screens/Monitors connected, it will only capture the "main" screen
- the text in the ROI has to be big enough to undergo OCR => Necessary to zoom in manually
