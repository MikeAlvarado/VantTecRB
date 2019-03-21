'''
	@name       	automatedDocking.py
    @desc 			Class for the Automated Docking challenge
	@author 		Alejandro Gonzalez alex_gg97@hotmail.com
	@created_at 	2018-06-06
	@dependecies	python3
'''

'''
	Required python libraries
'''
#Add python3 path
import os
import sys

#Basic libraries
import time
import math
import random
import datetime

from num_detection import xy_c
#Vision and communication libraries are missing

'''
	Required our project libraries
'''
from .motors import Motors

class AutoDock:
	def __init__(self):
		self.Display = 0 	#Display number seen by the UAV (1,2 or 3)
		self.Dock = 0		#Dock the boat has to dock on (Dock1, Dock2, Dock3)
		self.Dock1 = 0		#Horizontal pixel the Dock1 is on the camera
		self.Dock2 = 0		#Horizontal pixel the Dock2 is on the camera
		self.Dock3 = 0		#Horizontal pixel the Dock3 is on the camera
		self.Center = 400	#Horizontal pixel which is the center of the image (800 pixels)
		#Error margin of a 50 pixels
		#We need experiments to change it
		self.CenterMin = Center + 50
		self.CenterMax = Center - 50
		self.Distance = 0
		self.Hydrophone = False

	def autoDock(self, xy_c, drone_display)

		#Get Docks position x in pixels and distance in meters
		self.Dock1 = xy_c[0]
		self.Dock2 = xy_c[1]
		self.Dock3 = xy_c[2]
		self.Distance1 = 
		self.Distance2 =
		self.Distance3 =


		self.Hydrophone = True

		while self.Hydrophone = True
			if self.Dock2 < self.CenterMin and self.Dock2 > self.CenterMax and self.Distance2 > 3:
				if self.Dock2 < self.CenterMin :
					motors.move(15,0)

				elif self.Dock2 > self.CenterMax :
					motors.move(0,15)

			elif self.Dock2 < self.CenterMin and self.Dock2 > self.CenterMax and self.Distance2 < 2: 
					motors.move(-30,-30)
					#si está muy cerca y aun no acomoda la direccion, tiene que regresarse

			elif self.Dock2 > self.CenterMin and self.Dock2 < self.CenterMax and self.Distance2 > 1:
				motors.move(30,30)
				#va derecho, se reduce la distancia

			else
				motors.move(0,0)
				time.sleep(5)
				self.Hydrophone = False

		while self.Distance2 < 5 and not self.Hydrophone
			motors.move(-30, -30)

		if self.Distance >= 5 and not self.Hydrophone
			#we need to get the result coming from the phone, for now we can test giving it the number
			self.Display = drone_display

			if self.Display = 1:
				self.Dock = self.Dock1
				self.Distance = self.Distance1

			elif self.Display = 2:
				self.Dock = self.Dock2
				self.Distance = self.Distance2

			elif self.Display = 3:
				self.Dock = self.Dock3
				self.Distance = self.Distance3

			if self.Dock < self.CenterMin and self.Dock > self.CenterMax and self.Distance > 3:
				if self.Dock < self.CenterMin :
					motors.move(15,0)

				elif self.Dock > self.CenterMax :
					motors.move(0,15)

			elif self.Dock < self.CenterMin and self.Dock > self.CenterMax and self.Distance < 2: 
					motors.move(-30,-30)
					#si está muy cerca y aun no acomoda la direccion, tiene que regresarse

			elif self.Dock > self.CenterMin and self.Dock < self.CenterMax and self.Distance > 1:
					motors.move(30,30)
					#va derecho, se reduce la distancia

			else
				motors.move(0,0)
				#la distancia es menor a 1 metro, se frena y el impulso lo atraca