import time
from digi.xbee.devices import XBeeDevice
import json
from ..boat_nav.gpsNavigation import GPSNavigation
from ..darknet.caller import main_caller

def subscriber(xbee, imu):
    '''Esto es para el bote, el bote envia a la estacion cada 500ms'''
    #****************************************************************************************#
    # Replace with the serial port where your local module is connected to.
    PORT = "/dev/ttyUSB1"
    # Replace with the baud rate of your local module.
    BAUD_RATE = 9600
    REMOTE_NODE_ID = "vtecstation" #El nodo con el que se quiere comunicar.
    #****************************************************************************************#

    print(" +-------------------------------------------------+")
    print(" |                       Bote                      |")
    print(" +-------------------------------------------------+\n")
    device = XBeeDevice(PORT, BAUD_RATE)
    gps_navigation = GPSNavigation(imu)

    try:
        device.open()
        device.flush_queues()

        print("Waiting conversation...\n")
        while True:
            xbee_message = device.read_data()
            if xbee_message is not None:
                #Imprime el json para prueba
                jmessage = json.loads(bytes(xbee_message.data).decode()) 
                print(jmessage)

                # Set current coords
                coords = imu.get_gps_coords()
                lat = coords['latitude']
                lon = coords['longitud']
                xbee.set_latlong(lat,lon)
                # Set target coords
                
                if jmessage['action'] == '2':
                    xbee.set_target(float(jmessage['target_lat']),float(jmessage['target_lon']))
                    gps_navigation.update_nav(xbee.target_lat, xbee.target_lon) # Waypoint
                elif jmessage['action'] == '3':
                    # Until there is a resutl
                    res = 'not found pair of posts'
                    while res == 'not found pair of posts' or res is None:
                        res = main_caller('autonomus_navigation')
                        gps_navigation.navigation.search()

                    gps_navigation.auto_nav(res[0], res[1]) # Waypoint Carlos

                    res = 'not found pair of posts'
                    while res == 'not found pair of posts' or res is None:
                        res = main_caller('autonomus_navigation')
                        gps_navigation.navigation.search()

                    gps_navigation.auto_nav(res[0], res[1]) # Waypoint Carlos

                elif jmessage['action'] == '4':
                    # Until there is a resutl
                    res = 'not found pair of posts' or res is None:
                    while res == 'not found pair of posts':
                        res = main_caller('autonomus_navigation')
                        gps_navigation.navigation.search()

                    gps_navigation.auto_nav2(res[0], res[1]) # Waypoint Carlos

                    res = 'not found pair of posts'
                    while res == 'not found pair of posts' or res is None:
                        res = main_caller('autonomus_navigation')
                        gps_navigation.navigation.search()

                    gps_navigation.auto_nav2(res[0], res[1]) # Waypoint Carlos

                elif jmessage['action'] == '5':
                    # Until there is a resutl
                    res = 'not found pair of posts'
                    while res == 'not found pair of posts':
                        res = main_caller('autonomus_navigation')
                        gps_navigation.navigation.search()

                    gps_navigation.auto_nav(res[0], res[1]) # Waypoint Carlos

                    res = 'not found pair of posts'
                    while res == 'not found pair of posts':
                        res = main_caller('autonomus_navigation')
                        gps_navigation.navigation.search()

                    gps_navigation.auto_nav(res[0], res[1]) # Waypoint Carlos


                xbee_network = device.get_network()
                remote_device = xbee_network.discover_device(REMOTE_NODE_ID) #Aqui debe enviarlo al servidor
                device.send_data(remote_device, xbee.send())

    finally:
        if device is not None and device.is_open():
            device.close()
