import json

class xbee(object):
    def __init__(self):
        self.challenge = 'speed'
        self.latitude = 'HDDD.DDDDDD'
        self.longitude = 'HDDD.DDDDDD'
        self.target_lat = 'HDDD.DDDDD'
        self.target_lon = 'HDDD.DDDDD'
        self.action = '1'


    def set_challenge(self, chal='N'):
    	self.challenge = chal

    def set_latlong(self, latitude, longitude):
    	self.latitude = latitude
    	self.longitude = longitude
        
    def set_target(self, lat, lon):
        self.target_lat = lat
        self.target_lon = lon
        
    def set_action(self,action):
        self.action = action
        
    def send(self):
        return json.dumps(self, default=jsonDefault)


def jsonDefault(object):
    return object.__dict__
