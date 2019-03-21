import cv2
import numpy as np
#import pytesseract
import argparse
import os

from matplotlib import pyplot as plt
from glob import glob
from PIL import Image




def analyze(image,number_template,xc,yc,xy_c):

	#Display current ROI to be analized
	img_roi = image.copy()

	#preprocessinfg before Object Character Recognition
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray,(5,5),0)
	gray = cv2.threshold(gray, 50, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

	#Display processed ROI
	gray = cv2.medianBlur(gray, 3)



	#Write the grayscale image to disk as a temporary file
    #Load the image as a PIL/Pillow image, make a mosaic and apply OCR, and then delete the temporary file
	filename = "{}.png".format(os.getpid())
	cv2.imwrite(filename, gray)
	fn = filename
	images_names = [fn] * 4
	images = map(Image.open, images_names)
	os.remove(filename)
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

	filename = 'test.jpg'

	#Run OCR
	text = pytesseract.image_to_string(Image.open(filename),config="--psm 10")
	os.remove(filename)

	#If did not detect anything return False
	if not text:
		return xy_c
	#If detected some character, corroborate if it is a number in the range 1,2,3
	#print number_template
	if( text[0].isdigit() and int(text[0]) <= 3 ):#and number_template == text[0]):
		cv2.imshow('DETECTED ROI BEFORE IMAGE PROCESSING AND OCR..',img_roi)
		cv2.imshow('DETECTED ROI READY TO OCR...',gray)
		if(int(text[0]) == 1  and number_template == text[0]):
			xy_c[0] = [1,xc,yc]
		elif (int(text[0]) == 2 and number_template == text[0] ):
			xy_c[1] =  [2,xc,yc]
		elif (int(text[0]) == 3 and number_template == text[0]):
			xy_c[2] =  [3,xc,yc]

		return xy_c
	return xy_c





#Lista para guardar coordenadas de todos los templates matches que se hagan en una imagen.
rois = []

#Recorrer todas las imagenes de los docks y numeros. Folder con todos las fotos de los docks.
for fn in glob('test_images/*.png'):

	img = cv2.imread(fn,0)
	img2 = img.copy()
	detected = cv2.imread(fn,1)
	rgb = detected.copy()

	#Hacer template matching con todas las templates guardadas(training set)
	for fn in glob('templates/*.png'):
		#print fn[-8]
		template = cv2.imread(fn,0)
		w, h = template.shape[::-1]
		method = eval('cv2.TM_CCOEFF_NORMED')

		# Apply template Matching
		res = cv2.matchTemplate(img,template,method)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

		# If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
		if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
			top_left = min_loc
		else:
			top_left = max_loc
		bottom_right = (top_left[0] + w, top_left[1] + h)

		roi = (top_left,bottom_right,fn[-8])
		rois.append(roi)
		cv2.rectangle(img,top_left, bottom_right, 255, 2)
		cv2.imshow('ALL TEMPLATE MATCHES',img)


	#Detectar en cada roi si es un numero o no, si lo es  imprimir  el numero
	xy_c = [[0,0,0],[0,0,0],[0,0,0]]
	for coords in rois:

		top_left = coords[0]
		bottom_right = coords[1]
		number_template =  coords[2]
		x = top_left[0]
		y = top_left[1]
		w = bottom_right[0] - x
		h = bottom_right[1] - y
		xc = x + int(w /2)
		yc = y + int(h /2)
		cropped_image = rgb[y:y+h, x:x+w]


		result = analyze(cropped_image,number_template,xc,yc,xy_c)
		xy_c =  result


		'''
		if(result is False or result is None):
			continue
		else:
			if(int(result) == num_to_detect):
				print("NUMBER DETECTED:	" + str(result ))
				cv2.rectangle(detected,top_left, bottom_right, 100, 2)
				rois=[]
				#call get_distances con identificador 'N', definir parametros para los carteles.
				break
		'''

	#centers detected
	print ("X & Y Coordinates for DOCKS 1, 2, 3")

	for index,i in enumerate(result):
		print('Dock : ' + str((index+1)) +  ' ' + str(i[1:]))
	result =[]

	cv2.imshow('ROI DETECTED',detected)

	if(result is False or result is None):
		print('NUMBER ' + str(num_to_detect) + ' NOT FOUND IN THIS IMAGE')

	cv2.waitKey(0)
	rois = []
