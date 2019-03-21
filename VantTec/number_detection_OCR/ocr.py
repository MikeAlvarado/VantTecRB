# USAGE
# python ocr.py --image images/example_01.png 
# python ocr.py --image images/example_02.png  --preprocess blur

# import the necessary packages
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import numpy as np

'''
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
	help="type of preprocessing to be done")
args = vars(ap.parse_args())
'''
# load the example image and convert it to grayscale
image = cv2.imread('image.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cv2.imshow("Image", gray)

# check to see if we should apply thresholding to preprocess the
# image

gray = cv2.threshold(gray, 0, 255,
cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# make a check to see if median blurring should be done to remove
# noise
#gray = cv2.medianBlur(gray, 3)
kernel = np.ones((3,3),np.uint8)
gray = cv2.erode(gray,kernel,iterations = 1)
cv2.imshow("Imagwe", gray)

# write the grayscale image to disk as a temporary file so we can
# apply OCR to it
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)

# load the image as a PIL/Pillow image, apply OCR, and then delete
# the temporary file

cv2.waitKey(0)



fn = 'fff.png' #filename
images_names = [fn] * 4
#print images_names
images = map(Image.open, images_names) 
widths, heights = images[0].size

total_width = widths * 4
max_height = heights

new_im = Image.new('RGB', (total_width, max_height))

x_offset = 0
count = 4

for im in images:
  new_im.paste(im, (x_offset,0))
  x_offset += im.size[0]

new_im.save('test.jpg')
new_im.show()
filename = 'test.jpg'


text = pytesseract.image_to_string(Image.open(filename),config="--psm 10")
os.remove(filename)
print(text[0])

# show the output images
# cv2.imshow("Image", image)

cv2.waitKey(0)
