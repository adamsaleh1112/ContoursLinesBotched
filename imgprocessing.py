import cv2
import numpy as np

def processed(img, maskx, masky, maskw, maskh):

    # PROCESSING
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # converts image to grayscale
    blur = cv2.blur(gray, (3, 3)) # blurs / smoothens image
    edges = cv2.Canny(blur, 50, 150, apertureSize=3) # apply acnny edge detection to image which makes edges of objects stand out

    # MASK VARIABLES
    x = maskx # mask x, y, w, h
    y = masky
    w = maskw
    h = maskh
    mask = np.zeros(edges.shape[:2], np.uint8)
    mask[y:y + h, x:x + w] = 255
    maskimg = cv2.bitwise_and(edges, edges, mask=mask)

    return maskimg

# PROGRAMMING WORKS CITED

# Grayscale (Line 7): https://www.geeksforgeeks.org/python-grayscaling-of-images-using-opencv/
# Blur (Line 8): https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html
# Canny (Line 9): https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html
# Masking (Lines 12-18): https://stackoverflow.com/questions/11492214/opencv-via-python-is-there-a-fast-way-to-zero-pixels-outside-a-set-of-rectangle