'''
	@name       	imu.py
    @desc 			Imu Controller.
					This file has all the necesary functions to access the imu for the
					autonomous navigation, such as position, orientation, velocity,
					acceleration, etc.
	@author 		Marcopolo Gil Melchor marcogil93@gmail.com
	@created_at 	2017-06-08 
	@updated_at 	2017-11-28 Restructuration and comments. 
	@dependecies	python3
'''

'''
	Required dependencies
'''
#Vector Nav library
from vnpy import *

#Basic libraries
import math
import time
import sys
import os
#Debug libraries
from inspect import getmembers
from pprint import pprint

#	CONSTANTS
EARTH_RADIUOS = 6371000
PORT = 	'/dev/ttyUSB0'
'''
@desc 	Init imu module connection **
@params None
@return None
'''

class Imu:
	'''Class to access imu data'''
	def __init__(self):
		self.northYaw = 0
		self.earthRadious = EARTH_RADIUOS
		self.vnSensor = VnSensor()
		self.baudRate = 115200
		self.get_port()
		self.connect()

	
	def get_port(self):
		'''
		@desc 	Get imu port **
		@params None
		@return string
		'''
		if os.path.exists(PORT):
			print("Port Found")
			return PORT
		else:
			sys.exit('IMU not found // Check if connected')


	def print_model(self):
		'''
		@desc 	Get Imu model information **
		@params None
		@return string
		'''
		return self.vnSensor.read_model_number()



	def close_(self):
		'''
		@desc Close Imu sensor
		@params None
		@return None
		'''
		self.vnSensor.disconnect()

	
	def connect(self):
		'''
		@desc Reconnect Imu
		@params None
		@return None
		'''
		self.vnSensor.connect(PORT,self.baudRate)

	def get_num_satellites(self):
		'''
		@desc 	Get  number of listening Satellites**
		@params None
		@return integer 
		'''
		#Return values of gps
		#'gps_fix', 'lla', 'ned_acc', 'ned_vel', 'num_sats', 'speed_acc', 'this', 'time', 'time_acc', 'week'
		return self.vnSensor.read_gps_solution_lla().num_sats


	def get_gps_coords(self):
		'''
		@desc 	Get averages of latitude and longitud coords after 10 tests
		@params None
		@return dynamic array
				float longitud
				float latitude
		'''
		coord_x = 0
		coord_y = 0

		#Get average coords of 10 tests
		for i in range(10):
			lla = self.vnSensor.read_gps_solution_lla()
			coord_x += lla.lla.x
			coord_y += lla.lla.y
		
		coord_x = coord_x / 10
		coord_y = coord_y / 10
		coords ={ 'latitude': coord_x , 'longitud': coord_y}

		return coords


	def get_yaw_pitch_roll(self):
		'''
		@desc 	Get  yaw pitch roll degrees
		@params None
		@return vec3f object
				float x 
				float y
				float z 
		'''
		return self.vnSensor.read_yaw_pitch_roll()


	def get_yaw_orientation(self):
		'''
		@desc 	Get  yaw degree
		@params None
		@return float degree
		'''
		degree = self.vnSensor.read_yaw_pitch_roll().x%360

		if(degree > 180):
			degree = degree - 360


		return degree


	def get_magnetic_measurments(self):
		'''
		@desc 	Get  magnetic fields measurements
		@params None
		@return vec3f object of cgs (centimetre–gram–second) units (Gaussian units)
				float x 
				float y
				float z 
		'''
		return self.vnSensor.read_magnetic_measurements()


	def get_magnetic_and_gravity_reference(self):
		'''
		@desc 	Get  magnetic fields measurements
		@params None
		@return ???
		'''
		return self.vnSensor.read_magnetic_and_gravity_reference_vectors()


	def get_imu_measurements(self):
		'''
		@desc 	Get  all imu measurments
		@params None
		@return ???
		'''
		return self.vnSensor.read_imu_measurements()


	def get_gps_acceleration_velocity(self):
		'''
		@desc 	Get acceleration and velocity vectors
		@params None
		@return dynamic array
					vec3f acceleration
					vec3f velocity
		'''
		lla = self.vnSensor.read_gps_solution_lla()

		return {
			'acceleration': lla.ned_acc,
			'velocity': lla.ned_vel
		}


	def get_angular_rates(self):
		'''
		@desc Get acceleration and velocity vectors
		@params None
		@return dynamic array
				vec3f acceleration
				vec3f velocity
		'''
		angles = self.vnSensor.read_angular_rate_measurements()

		return {
			'x': angles.x%360,
			'y': angles.y%360,
			'z': angles.z%360,
		}


	def get_acceleration(self):
		'''
		@desc Get acceleration
		@params None
		@return vec3f acceleration
		'''
		return self.vnSensor.read_acceleration_measurements()


	def get_delta_theta(self):
		'''
		@desc Get delta theta
		@params None
		@return dynamic array
					x
					y
					z
		'''
		angles = self.vnSensor.read_delta_theta_and_delta_velocity().delta_theta

		return {
			'x': angles.x%360,
			'y': angles.y%360,
			'z': angles.z%360,
		}


	def get_delta_velocity(self):
		'''
		@desc Get delta velocity
		@params None
		@return vec3f velocity
		'''
		return self.vnSensor.read_delta_theta_and_delta_velocity().delta_velocity


	def get_degrees_to_north_orientation(self):
		'''
		@desc Get needed degrees to point north
		@params None
		@return float degree
		'''
		degree = (self.get_yaw_orientation()%360) - self.northYaw

		if (degree > 180):
			degree = degree - 360


		return degree


	def get_degrees_and_distance_to_gps_coords(self, latitude2, longitud2):
		'''
		@desc get degrees and distance to gps coords
		@params goal latitude and longitud
		@return dynamic array
					float distance  meters
					float degrees 
		'''
		north = (self.get_yaw_orientation()%360) - self.northYaw

		if (north > 180):
			north = north - 360

		coords = self.get_gps_coords()
		latitude1 = coords['latitude']
		longitud1 = coords['longitud']

		#print(coords)
		#print(latitude2, longitud2)

		longitud_distance = (longitud1 - longitud2)
		y_distance = math.sin(longitud_distance) * math.cos(latitude2)
		x_distance = math.cos(latitude1) * math.sin(latitude2) - math.sin(latitude1) * math.cos(latitude2) * math.cos(longitud_distance)
		bearing = math.atan2(y_distance, x_distance)
		bearing = math.degrees(bearing) - north
		bearing = (bearing + 360) % 360

		if (bearing > 180):
			bearing = bearing - 360
		
		print("bearing: ", bearing)

		phi1 = math.radians(latitude1)
		phi2 = math.radians(latitude2)
		dphi = math.radians(latitude2 - latitude1)
		dlam = math.radians(longitud2 - longitud1)
		a = math.sin(dphi/2)*math.sin(dphi/2) + math.cos(phi1)*math.cos(phi2)* math.sin(dlam/2)*math.sin(dlam/2)
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
		distance = self.earthRadious * c
		print("distance: ", distance)

		return {
			'distance': int(distance),
			'degree': int(bearing) * -1
		}

	def get_obstacle_gps_coords(self, boat_x, boat_y, path_x, path_y):
		'''
		@desc cambio de coordenadas x y a GPS 
		@params boat_x, boat_y, path_x, path_y
		@returns latitude, longitude
		'''
		coords = self.get_gps_coords()
		latitude1 = coords['latitude']
		longitude1 = coords['longitud']

		#print(coords);
		#print(latitude2, longitud2);

		y_distance = path_y - boat_y
		x_distance = path_x - boat_x

		phi1 = math.radians(latitude1)
		phi2 = math.radians(latitude2)

		latitude2  = latitude1  + (y_distance / EARTH_RADIUOS) * (180 / math.pi)
		longitude2 = longitude1 + (x_distance / EARTH_RADIUOS) * (180 / math.pi) / math.cos(phi1 * math.pi/180)

		return {
			'latitude': latitude2,
			'longitud': longitude2
		}

	def get_pos_from_vision(self, point_distance, point_degree):

		north = (self.imu.get_yaw_orientation()%360) - self.northYaw

		if (north > 180):
			north = north - 360

		real_degree = north + point_degree
		real_radians = math.radians(real_degree)

		real_x = math.sin(abs(real_radians))*point_distance
		real_y = math.cos(abs(real_radians))*point_distance

		return {
			'real_x': real_x,
			'real_y': real_y
		}