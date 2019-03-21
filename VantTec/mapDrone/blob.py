# -*- coding: utf-8 -*-

import cv2
import numpy as np
import math



def map(imgname):


	#READ GRAYSCALE
	img_big_size = cv2.imread(imgname, 0)
	#READ RGB
	img_bgr_big_size = cv2.imread(imgname, 1)
	img_bgr =   cv2.resize(img_bgr_big_size, (640,480 ))
	img_ori = img_bgr.copy()
	#THRESHOLD HSV
	hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
	img_hsv = cv2.inRange(hsv, (103, 87, 0), (255, 243,203))
	edge = cv2.Canny(img_hsv, 100, 80)
	cnts = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
	m  = cv2.moments(cnts) 
	c = int(round(m['m10']/m['m00'])),int(round(m['m01']/m['m00']))
	cv2.circle(img_bgr,c,5,(255,0,0),-1)
	
	


	cv2.imshow('BLOB',img_hsv)
	cv2.imshow('ORIGINAL',img_bgr)
	cv2.imshow('EDGE',edge)
	#THRESHOLD HSV
	cv2.waitKey(0)



result = map('v.jpg')


