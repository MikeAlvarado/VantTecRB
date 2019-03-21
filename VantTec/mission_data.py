'''
Module with class that holds all variables and data for the mission
'''

class MissionStationData:
    '''Class to handle global varaibles easily'''
    def __init__(self, station_xb):
        self.dock_num = 0
        self.map_data = {
            'height': 0,
            'width': 0,
            'obstacles': [], #tuple array
            'boat_x': 0,
            'boat_y': 0,
            'can_x': 0,
            'can_y': 0,
        },
        self.received_dock_img = False
        self.station_xb = station_xb

class MissionBoatData:
    '''Class to handle global varaibles easily'''
    def __init__(self, boat_xb):
        self.dock_num = 0
        self.map_data = {
            'height': 0,
            'width': 0,
            'obstacles': [], #tuple array
            'boat_x': 0,
            'boat_y': 0,
            'can_x': 0,
            'can_y': 0,
        },
        self.received_dock_img = False
        self.boat_xb = boat_xb
        self.exit_nav = False
