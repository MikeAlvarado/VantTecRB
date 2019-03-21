from communications.Xbee.comunicacion import xbee
from communications.thread_classes import BoatXbThread
from mission_data import MissionBoatData
import threading
from communications.Xbee.subscriber import subscriber
from communications.boat_nav.imu import Imu
# from communications.darknet.caller import main_caller


# class CameraThread(threading.Thread):
#     '''Class to access camera data'''
#     def __init__(self, thread_id, name):
#         threading.Thread.__init__(self)
#         self.thread_id = thread_id
#         self.name = name

#     def run(self):
#         main_caller()

class ThreadKiller(threading.Thread):
    '''Class to kill challenges'''
    def __init__(self, thread_id, name, data):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.data = data
    
    def run(self):
        while True:
            val = input('Kill?')
            if val == 'y':
                self.data.exit_nav = True
            self.data.exit_nav = False

def main_boat():
    main_data = MissionBoatData(xbee())
    thread_boat = BoatXbThread(1, "Boat", main_data.boat_xb, main_data) #subscriber
    #thread_killer = ThreadKiller(2, "Killer", main_data)

    thread_boat.start()
    #thread_killer.start()
    thread_boat.join()
    #thread_killer.join()

subscriber(xbee(), Imu())
