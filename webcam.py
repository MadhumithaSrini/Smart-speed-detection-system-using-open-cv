from PIL import Image
from firebase import firebase
import pytesseract
import argparse
import cv2
import time
import os
import numpy as np

firebase = firebase.FirebaseApplication('https://pyocr-464c8.firebaseio.com/')
SECRET_KEY = 'gi2m28GsAeA2FPEdYJpAN4MAeM1qAUMZMlboifeQ'


cap= cv2.VideoCapture(0)
count=0

while(count<=100):
    ret,image=cap.read()
                               #if it's an external web cam , image=cv2.flip(image,-1)
    cv2.imshow('image',image)
    count+=1
    cv2.waitKey(50) & 0xff
    cv2.imwrite("images/test.png", image)                   #it can also be directly given with the name in which image should be stored.Not necessarily foldername/image name....refer note
cap.release()
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,                   #--image : The path to the image we’re sending through the OCR system.
	help="image")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
	help="type of preprocessing to be done")
args = vars(ap.parse_args())

# load the example image and convert it to grayscale
test = cv2.imread(args["image"])
gray = cv2.cvtColor(test, cv2.COLOR_BGR2GRAY)

cv2.imshow("Image", gray)

# check to see if we should apply thresholding to preprocess the
# image
if args["preprocess"] == "thresh":
	gray = cv2.threshold(gray, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# make a check to see if median blurring should be done to remove
# noise
elif args["preprocess"] == "blur":
	gray = cv2.medianBlur(gray, 3)

# write the grayscale image to disk as a temporary file so we can
# apply OCR to it
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)

# load the image as a PIL/Pillow image, apply OCR, and then delete
# the temporary file
mytext = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)
print(mytext)
firebase.put("vehicle", "id", mytext)
print("done")
time.sleep(5)

# show the output images
# cv2.imshow("Image", image)
cv2.imshow("Output", gray)
cv2.waitKey(0)


