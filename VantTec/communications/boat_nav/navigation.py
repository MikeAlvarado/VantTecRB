
'''
    @name       	navigation.py
    @desc 			Navigation file. integration of boat movement 
    @author 		Marcopolo Gil Melchor marcogil93@gmail.com
    @created_at 	2017-11-28 
    @updated_at 	2018-06-22
    @updated_by     Julio Aguilar, Gerardo Berni, Alejandro González
    @dependecies	python3
'''

'''
    Required python libraries 
'''
#Basic libraries
import time
import math
import random
import datetime

'''
    Required our project libraries 
''' 
from .motors import Motors

class Navigation:
    def __init__(self, imu):
        self.frame = None
        self.stopNavigation = False
        self.imu = imu
        self.motors = Motors()

    def navigate(self, destiny, lat, lon):
        print('--------entra-------')
        lastOrientationDegree = 0
        turn_degrees_needed   = 0
        turn_degrees_accum    = 0
        distance = destiny['distance']
        orientationDegree = destiny['degree']
        
        #clean angle
        self.imu.get_delta_theta()
        #print("delta theta: ", self.imu.get_delta_theta)

        #Condition distance more than 2 meters. 
        while distance > 2 and not self.stopNavigation:
            print("coords: ", self.imu.get_gps_coords())
            
            if lastOrientationDegree != orientationDegree:
                turn_degrees_needed = orientationDegree
                turn_degrees_accum  = 0

                #clean angle
                self.imu.get_delta_theta()
                lastOrientationDegree = orientationDegree

            #If same direction, keep route
            imu_angle = self.imu.get_delta_theta()['z']%360

            if imu_angle > 180:
                imu_angle = imu_angle - 360
            
            #print("grados imu: ", imu_angle)

            #threshold
            if math.fabs(imu_angle) > 1:
                turn_degrees_accum += imu_angle

            #print("grados acc: ", turn_degrees_accum)
            turn_degrees_needed = (orientationDegree + turn_degrees_accum)%360

            if turn_degrees_needed > 180 : 
                turn_degrees_needed = turn_degrees_needed - 360
            elif  turn_degrees_needed < -180:
                turn_degrees_needed = turn_degrees_needed + 360
            
            print("grados a voltear: ", turn_degrees_needed)

            if math.fabs(turn_degrees_needed) < 10: 
                print("Tengo un margen menor a 10 grados")
                velocity = 50
                self.motors.move(velocity, velocity)

            else:
                #girar
                if turn_degrees_needed > 0:
                    print("Going to move left")
                    self.motors.move(25, -25)
                else:
                    print("Going to move right")
                    self.motors.move(-25, 25)
            #ir derecho
            #recorrer 2 metros
            destiny = self.imu.get_degrees_and_distance_to_gps_coords(lat, lon)
            #time.sleep()
        self.motors.move(0,0)

    def visnavigate(self, pdistance, pdegree):
        lastOrientationDegree = 0
        turn_degrees_needed   = 0
        turn_degrees_accum    = 0
        distance = pdistance
        orientationDegree = pdegree
        #clean angle
        self.imu.get_delta_theta()
        #print("delta theta: ", self.imu.get_delta_theta)

        #Condition distance more than 4 meters. 
        while distance > 5 and not self.stopNavigation:
            print("coords: ", self.imu.get_gps_coords())
            
            if lastOrientationDegree != orientationDegree:
                turn_degrees_needed = orientationDegree
                turn_degrees_accum  = 0

                #clean angle
                self.imu.get_delta_theta()
                lastOrientationDegree = orientationDegree

            #If same direction, keep route
            imu_angle = self.imu.get_delta_theta()['z']%360

            if imu_angle > 180:
                imu_angle = imu_angle - 360
            
            #print("grados imu: ", imu_angle)

            #threshold
            if math.fabs(imu_angle) > 1:
                turn_degrees_accum += imu_angle

            #print("grados acc: ", turn_degrees_accum)
            turn_degrees_needed = (orientationDegree + turn_degrees_accum)%360

            if turn_degrees_needed > 180 : 
                turn_degrees_needed = turn_degrees_needed - 360
            elif  turn_degrees_needed < -180:
                turn_degrees_needed = turn_degrees_needed + 360
            
            print("grados a voltear: ", turn_degrees_needed)

            if math.fabs(turn_degrees_needed) < 15: 
                print("Tengo un margen menor a 15 grados")
                velocity = 50
                self.motors.move(velocity, velocity)

            else:
                #girar
                if turn_degrees_needed > 0:
                    #print("Going to move left")
                    self.motors.move(30, -30)
                else: 
                    #print("Going to move right")
                    self.motors.move(-30, 30)
            #ir derecho
            #recorrer 2 metros           
            #time.sleep(1)
        
        while distance < 5:
            waypoint = self.imu.get_pos_from_vision(pdistance, pdegree)
            waypoint_x = waypoint['real_x']
            waypoint_y = waypoint['real_y']
            gate_gps = self.imu.get_obstacle_gps_coords(0, 0, waypoint_x, waypoint_y)
            lat = gate_gps['latitude']
            lon = gate_gps['longitud']
            destiny = self.imu.get_degrees_and_distance_to_gps_coords(lat, lon)
            self.navigate(destiny,lat,lon)
            
        self.motors.move(50,50)
        time.sleep(5)
        self.motors.move(0,0)

    def visnavigate2(self, pdistance, pdegree):
        lastOrientationDegree = 0
        turn_degrees_needed   = 0
        turn_degrees_accum    = 0
        distance = pdistance
        orientationDegree = pdegree
        #clean angle
        self.imu.get_delta_theta()
        #print("delta theta: ", self.imu.get_delta_theta)

        #Condition distance more than 5 meters. 
        while distance > 3 and not self.stopNavigation:
            print("coords: ", self.imu.get_gps_coords())
            
            if lastOrientationDegree != orientationDegree:
                turn_degrees_needed = orientationDegree
                turn_degrees_accum  = 0

                #clean angle
                self.imu.get_delta_theta()
                lastOrientationDegree = orientationDegree

            #If same direction, keep route
            imu_angle = self.imu.get_delta_theta()['z']%360

            if imu_angle > 180:
                imu_angle = imu_angle - 360
            
            #print("grados imu: ", imu_angle)

            #threshold
            if math.fabs(imu_angle) > 1:
                turn_degrees_accum += imu_angle

            #print("grados acc: ", turn_degrees_accum)
            turn_degrees_needed = (orientationDegree + turn_degrees_accum)%360

            if turn_degrees_needed > 180 : 
                turn_degrees_needed = turn_degrees_needed - 360
            elif  turn_degrees_needed < -180:
                turn_degrees_needed = turn_degrees_needed + 360
            
            print("grados a voltear: ", turn_degrees_needed)

            if math.fabs(turn_degrees_needed) < 15: 
                print("Tengo un margen menor a 15 grados")
                velocity = 50
                self.motors.move(velocity, velocity)

            else:
                #girar
                if turn_degrees_needed > 0:
                    #print("Going to move left")
                    self.motors.move(30, -30)
                else: 
                    #print("Going to move right")
                    self.motors.move(-30, 30)
            #ir derecho
            #recorrer 2 metros           
            #time.sleep(1)       

        self.motors.move(50,50)
        time.sleep(5)
        self.motors.move(0,0)

    def search(self):
        print('Searching')
        self.motors.move(30,-30)

    def visgpsnavigate(self, pdistance, pdegree):
         
        distance = pdistance
         
        while distance > 2:
            waypoint = self.imu.get_pos_from_vision(pdistance, pdegree)
            waypoint_x = waypoint['real_x']
            waypoint_y = waypoint['real_y']
            gate_gps = self.imu.get_obstacle_gps_coords(0, 0, waypoint_x, waypoint_y)
            lat = gate_gps['latitude']
            lon = gate_gps['longitud']
            destiny = self.imu.get_degrees_and_distance_to_gps_coords(lat, lon)
            self.navigate(destiny,lat,lon)
             
        self.motors.move(50,50)
        time.sleep(5)
        self.motors.move(0,0)
