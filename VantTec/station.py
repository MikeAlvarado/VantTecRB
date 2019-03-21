import threading
from communications.Xbee.comunicacion import xbee
from mission_data import MissionStationData
from communications.Xbee.publisher import publisher

class StationXbThread(threading.Thread):
    '''Class to access xbee data from station'''
    def __init__(self, thread_id, name, station_xb):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.station_xb = station_xb

    def run(self):
        publisher(self.station_xb)

def main_station():
    main_data = MissionStationData(xbee())
    # thread_drone = DroneThread(1, "DroneComm", main_data)
    # thread_check = DroneCheker(2, "Drone Check", main_data.dock_num, main_data.map_data)
    thread_station = StationXbThread(3, "Station", main_data.station_xb)

    #thread_drone.start()
    #thread_check.start()
    thread_station.start()

    #thread_drone.join()
    #thread_check.join()
    thread_station.join()


main_station()
