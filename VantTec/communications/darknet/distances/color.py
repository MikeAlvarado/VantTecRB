# USAGE
# python color_kmeans.py --image images/jp.png --clusters 3

# import the necessary packages
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import argparse
import utils
import cv2
import numpy as np



def getColor(xc,yc,w,h):

	width = w	
	heigth = h
	shift_w = int((width/2))
	shift_h =  int((heigth/2))
	left =  int(xc - shift_w)
	right = int(xc + shift_w)
	upper = int(yc - shift_h)
	lower = int(yc + shift_h)
	
	original = cv2.imread('filename.png',1)
	crop_img = original[upper:lower, left:right]
	cv2.imshow('cropp',crop_img)
	cv2.waitKey(0)
	image = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
	image = image.reshape((image.shape[0] * image.shape[1], 3))
	clt = KMeans(n_clusters = 3)
	clt.fit(image)
	result = clt.cluster_centers_


getColor(325,209,30,41)
