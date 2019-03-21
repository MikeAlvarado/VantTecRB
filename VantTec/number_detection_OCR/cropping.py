"""
Kmeans clustering algorithm for colour detection in images

Initialise a kmeans object and then use the run() method.
Several debugging methods are available which can help to
show you the results of the algorithm.
"""

import Image
import random
import os
import pygame, sys
import cv2
import numpy as np
from PIL import Image
from glob import glob
from datetime  import datetime
from skimage import io, color,exposure
from skimage.color import rgb2lab,deltaE_cie76
from matplotlib import pyplot as plt

pygame.init()


def displayImage(screen, px, topleft, prior):

	# ensure that the rect always has positive width, height
	x, y = topleft
	width =  pygame.mouse.get_pos()[0] - topleft[0]
	height = pygame.mouse.get_pos()[1] - topleft[1]
	if width < 0:
		x += width
		width = abs(width)
	if height < 0:
		y += height
		height = abs(height)

	# eliminate redundant drawing cycles (when mouse isn't moving)
	current = x, y, width, height
	if not (width and height):
		return current
	if current == prior:
		return current

	# draw transparent box and blit it onto canvas
	screen.blit(px, px.get_rect())
	im = pygame.Surface((width, height))
	im.fill((128, 128, 128))
	pygame.draw.rect(im, (32, 32, 32), im.get_rect(), 1)
	im.set_alpha(128)
	screen.blit(im, (x, y))
	pygame.display.flip()

	# return current box extents
	return (x, y, width, height)



def setup(path):
    px = pygame.image.load(path)
    screen = pygame.display.set_mode( px.get_rect()[2:] )
    screen.blit(px, px.get_rect())
    pygame.display.flip()
    return screen, px


def mainLoop(screen, px):

 
	topleft = bottomright = prior = None
	n=0
	while n!=1:

		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONUP:
				if not topleft:
				    topleft = event.pos
				else:
				    bottomright = event.pos
				    n=1
				if topleft:
					prior = displayImage(screen, px, topleft, prior)
	return ( topleft + bottomright )




def ROI(fn):

	input_loc = fn
	screen, px = setup(input_loc)
	left, upper, right, lower = mainLoop(screen, px)

	#ROI Ensure output rect always has positive width, height
	if right < left:
		left, right = right, left
	if lower < upper:
		lower, upper = upper, lower

	im = Image.open(input_loc)
	return left,upper,right,lower


def main():

	cont = 0
	original = cv2.imread("templates11.png")
	cv2.imshow('drawing',original) 
	z = cv2.waitKey(0)
	

	if z == 99: 

		cv2.destroyWindow('drawing')
		left,upper,right,lower = ROI("templates11.png")
		#Crop ROI 
		image_obj = Image.open("templates11.png")
		coords = (left,upper,right,lower)
		cropped_image = image_obj.crop(coords)
		cropped_image.save( "image" +str(cont) +".png")
		cont+=1
		
		

if __name__ == "__main__":
	main()
