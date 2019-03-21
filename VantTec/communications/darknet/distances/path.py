"""	
	OVER-ALL METHODS DESCRIPTIONS.
	Color detection.- Kmeans clustering algorithm.
	Distances to objects.- Triangle Similarity for Object/Marker to Camera Distance.
	Angles to objects.- Using camera calibration, fundamental matrix, aspect ratio and FOV 78 d
"""

# import the necessary packages

import random
import os
import  sys
import cv2
import numpy as np
from PIL import Image
import math
from glob import glob
from datetime  import datetime
from skimage import io, color,exposure
from skimage.color import rgb2lab,deltaE_cie76
from matplotlib import pyplot as plt

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
"""
	KNOWN_DISTANCE -- initialize the known distance from the camera to the object(bouy,inches)

	KNOWN_WIDTH    -- initialize the known object width, which in this case is 15.35 for the competitions bouy.
					  	https://www.boatfendersdirect.co.uk/products/75-a2-polyform-buoy-20-x-16.html

	FOCAL_VIEW     -- the field of vision of the camera, derived from the diagonal FOV 78 degrees and an aspect ratio of 16:9 : 70.42 degrees. 
		
					  	https://stackoverflow.com/questions/25088543/estimate-visible-bounds-of-webcam-using-diagonal-fov?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
					  	http://vrguy.blogspot.com/2013/04/converting-diagonal-field-of-view-and.html

    WIDTH_DIM      --   Dimensions of video frame
						800 x 600

	
"""


#BOUYS (INCHES)
KNOWN_DISTANCE_B = 64.0   #unknown    173 cm  68.11024 inch
KNOWN_WIDTH_B =    8.5 #inches width of contest's bouys  pix =102
FOCAL_LENGHT_B =   768.0    #(PIX_WIDTH_B * KNOWN_DISTANCE_B) / KNOWN_WIDTH_B   109pix          return  KNOWN_WIDTH_B, FOCAL_LENGHT_B, width_b)   (C_WIDTH*C_FL)/PIX_WIDTH

#POSTS(INCHES)
KNOWN_DISTANCE_P = 74.8    #unknown  
KNOWN_WIDTH_P = 55.0    #unknown  
FOCAL_LENGHT_P = 627.29    #(PIX_WIDTH_P * KNOWN_DISTANCE_P) / KNOWN_WIDTH_P

FOCAL_VIEW =  78.0
WIDTH_DIM  =  800.0
HEIGTH_DIM =  600.0

ANGLE_PER_PIXEL = 78/math.sqrt(WIDTH_DIM**2 + HEIGTH_DIM**2) 
#check for values'integrity. return 1 if length of params is the expected.
def receive(values):	
	if len(values) == 5:
        	return True

# bouy 1 post 0 [id, xc,yc,w,h]
# performs calculation on each region of interest found on the image (bouys and posts). 
# param: rois -- list of lists with description values for each roi [id, xc,yc,w,h]
# return -- distances, angles, dominant color for each roi.

def get_rois_data(rois, challenge = 'autonomus_navigation'):

	#if is empty, return
	if not rois:
		return False
	rowLength = len(rois)
	#create output list of lists
	colLength = 3
	output = [[[0] for i in range(colLength)] for i in range(rowLength)]

	#iterate through all of the rois row by row.
	#args [id, xc,w,yc,h]
	for i in range(len(rois)):

	   #buoys  xc w yc h
		if(rois[i][0]) == 1:
		  #distances(meters)
			width_b = int(rois[i][2]) 
			#print(width_b)
			#get inches to the object 
			inches = distance2camera(KNOWN_WIDTH_B, FOCAL_LENGHT_B, width_b)
			#convert inches to meters
			meters_b = inches * .0254 
			#difference of pixels from center
			difference = int(WIDTH_DIM/2) - (rois[i][1])
		  #compute angles
			#if difference is 0, angle must be 0
			if difference == 0:
				angle_b = 0
			#if difference is negative, angle must be negative
			elif difference < 0:
				angle_b = ANGLE_PER_PIXEL * abs(difference)
			#if difference is negative, angle must be positive
			elif difference > 0:
				angle_b = -(ANGLE_PER_PIXEL * difference)
		  #degrees to radians
			angle_b = angle_b * 0.0174533
			y = meters_b
			h = abs(y / math.cos(angle_b))
			x = math.sin(abs(angle_b)) * h
		  #modify x's sign depending on angle sign
			if angle_b == 0:
				x = 0
			elif angle_b < 0:
				if x > 0: 	
					x = -x
			elif angle_b > 0:
				x = abs(x)
			#form tuple alex quizo absolutos
			coords = (x,y,h)
			#change back to degreees
			angle_b = angle_b / 0.0174533
			angle_b = -angle_b 
			#setting the result
			output[i][0] = coords
			output[i][1] = angle_b
			output[i][2] = 'dontcare'#getColor(rois[i][1],rois[i][3],rois[i][2],rois[i][4])  
		#posts
		else:
		  #distances(meters)
			width_p = int(rois[i][2]) 
			#get inches to the object 
			inches = distance2camera(KNOWN_WIDTH_P, FOCAL_LENGHT_P, width_p)
			#convert inches to meters
			meters_p = inches * .0254 
		  #compute angles
		  	#if difference is 0, angle must be 0
			difference = int(WIDTH_DIM/2) - (rois[i][1])
			#if difference is 0, angle must be 0
			if difference == 0:
				angle_p = 0
		    #if difference is negative, angle must be negative
			elif difference < 0:
				angle_p = ANGLE_PER_PIXEL * abs(difference)
			#if difference is positive, angle must be positive
			elif difference > 0:
				angle_p = -(ANGLE_PER_PIXEL * difference)
			#degrees to radians
			angle_p = angle_p * 0.0174533
			y = meters_p
			h = abs(y / math.cos(angle_p))
			x = math.sin(abs(angle_p)) * h
			#modify x's sign depending on angle sign
			if angle_p == 0:
				x = 0
			elif angle_p < 0:
				if x > 0: 	
					x = -x
			elif angle_p > 0:
				x = abs(x)
			#form tuple
			coords = (x,y,h)

			#change back to degreees
			angle_p = angle_p / 0.0174533
			angle_p = -angle_p
	
			#setting the result
			output[i][0] = coords
			output[i][1] = angle_p
			colorofpost = getColor(rois[i][1],rois[i][3],rois[i][2],rois[i][4])  
			output[i][2] = colorofpost 
	
	#print("____Datos____")
	#print(output)

	if(challenge == 'autonomus_navigation'):
		return autonomus_navigation(output)
	return output


#Compute and return the distance from the marker to the camera
def distance2camera(C_WIDTH,C_FL,PIX_WIDTH):
	#print('KNOWN WIDTH: ' + str(C_WIDTH))
	#print('FOCAL LENGTH: ' + str(C_FL))
	#print('PIX_WIDTH: ' + str(PIX_WIDTH))
	return (C_WIDTH*C_FL)/PIX_WIDTH


#Compute and return the angle from the camera perspecive
def angle2camera(x1,y1,x2,y2):
	#get center pixel of roi
	pixel = (x1+(x2-x1))/2 
	preangle = int((pixel*FOCAL_VIEW)/WIDTH_DIM)
	return int(0 - ((FOCAL_VIEW/2) - preangle))

#print ROI's parameters.
def prints(rois):
	for row in rois:
   		for val in row:
        		print(('{:4}'.format(val)))

 
#K-MEANS CLUSTERING
class Cluster(object):

	def __init__(self):
		self.pixels = []
		self.centroid = None

	def addPoint(self, pixel):
		self.pixels.append(pixel)

	def setNewCentroid(self):

		R = [colour[0] for colour in self.pixels]
		G = [colour[1] for colour in self.pixels]
		B = [colour[2] for colour in self.pixels]
		if( len(R) != 0 and len(G) != 0 and len(B) != 0):
			R = sum(R) / len(R)
			G = sum(G) / len(G)
			B = sum(B) / len(B)

		self.centroid = (R, G, B)
		self.pixels = []

		return self.centroid


class Kmeans(object):

    def __init__(self, k=3, max_iterations=2, min_distance=5.0, size=200):
        self.k = k
        self.max_iterations = max_iterations
        self.min_distance = min_distance
        self.size = (size, size)

    def run(self, image):
        self.image = image
        self.image.thumbnail(self.size)
        self.pixels = np.array(image.getdata(), dtype=np.uint8)
        self.pixels = self.pixels.tolist()
        print(self.pixels)
        self.clusters = [None for i in range(self.k)]
        self.oldClusters = None
       
        randomPixels = random.sample(self.pixels, self.k)
        print(type(randomPixels))
        for idx in range(self.k):
            self.clusters[idx] = Cluster()
            self.clusters[idx].centroid = randomPixels[idx]

        iterations = 0

        while self.shouldExit(iterations) is False:

            self.oldClusters = [cluster.centroid for cluster in self.clusters]

            #print(iterations)

            for pixel in self.pixels:
                self.assignClusters(pixel)

            for cluster in self.clusters:
                cluster.setNewCentroid()

            iterations += 1


        return [cluster.centroid for cluster in self.clusters]

    def assignClusters(self, pixel):
        shortest = float('Inf')
        for cluster in self.clusters:
            distance = self.calcDistance(cluster.centroid, pixel)
            if distance < shortest:
                shortest = distance
                nearest = cluster

        nearest.addPoint(pixel)

    def calcDistance(self, a, b):

        result = np.sqrt(sum((np.array(a) - np.array(b)) ** 2))
        return result

    def shouldExit(self, iterations):

        if self.oldClusters is None:
            return False

        for idx in range(self.k):
            dist = self.calcDistance(
                np.array(self.clusters[idx].centroid),
                np.array(self.oldClusters[idx]))
            
            if dist < self.min_distance:
                return True

        if iterations <= self.max_iterations:
            return False

        return True

    def showCentroidColours(self):

        for cluster in self.clusters:
            image = Image.new("RGB", (200, 200), cluster.centroid)

    def showClustering(self):

        localPixels = [None] * len(self.image.getdata())

        for idx, pixel in enumerate(self.pixels):
                shortest = float('Inf')
                for cluster in self.clusters:
                    distance = self.calcDistance(cluster.centroid, pixel)
                    if distance < shortest:
                        shortest = distance
                        nearest = cluster

                localPixels[idx] = nearest.centroid

        w, h = self.image.size
        localPixels = np.asarray(localPixels)\
            .astype('uint8')\
            .reshape((h, w, 3))

        colourMap = Image.fromarray(localPixels)

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


def getColor(xc,yc,w,h):

	width = w	
	heigth = h
	shift_w = int((width/2))
	shift_h =  int((heigth/2))
	left =  int(xc - shift_w)
	right = int(xc + shift_w)
	upper = int(yc - shift_h)
	lower = int(yc + shift_h)
	
	filename = "filename.png"
	original = cv2.imread(filename,1)

	if original is not None:
		crop_img = original[upper:lower, left:right]
		image = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
		if image is not None:
			image = image.reshape((image.shape[0] * image.shape[1], 3))
			clt = KMeans(n_clusters = 1)
			clt.fit(image)
			result = clt.cluster_centers_
			result = result[0]
			if(result[0] > result[1]):
				return 'r'
			else:
				return 'g'
	return 'no color'

def autonomus_navigation(data):
	posts_distances_y = []
	posts_distances_x = []
	posts_angles = []
	if data is not None:
		for rois in data:
			if rois[2] == 'r' or rois[2]  == 'g':
				dists = rois[0]
				posts_distances_y.append(dists[1])
				posts_distances_x.append(dists[0])
				posts_angles.append(rois[1])

		points = zip(posts_distances_y,posts_distances_x,posts_angles)
		sorted_points = sorted(points)

		new_ys = [point[0] for point in sorted_points]
		new_xs = [point[1] for point in sorted_points]
		new_angs = [point[2] for point in sorted_points]
		print('SORTED LISTS OBJECTS Y, X , ANGLES...')
		print(new_ys)
		print(new_xs)
		print(new_angs)
		if len(new_ys) >=2:
			middle = min(new_xs[0],new_xs[1]) + abs(new_xs[0] - new_xs[1])/2
			angle_tomiddle = min(new_angs[0],new_angs[1]) + abs(new_angs[0] - new_angs[1])/2
			return  (middle,angle_tomiddle)
	return 'not found pair of posts'

		