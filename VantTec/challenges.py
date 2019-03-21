'''
Code to hold the main logic for the challenge
'''
import http.client
import json

IP_ADDR = 'http://ec2-54-89-60-172.compute-1.amazonaws.com:8080'
START_RUN = 'run/start/'
END_RUN = 'run/end/'
COURSE = 'courseA/'
TEAM_CODE = 'VTEC'

# Coords order of courses: Speed challenge, Automated docking, Find the path, Follow the leader
GPS_NAVIGATION_A = [[10, 10], [10, 10], [10, 10], [10, 10]]
GPS_NAVIGATION_B = [[10, 10], [10, 10], [10, 10], [10, 10]]
GPS_NAVIGATION_C = [[10, 10], [10, 10], [10, 10], [10, 10]]

def speed_challenge():
    '''Function to execute speed challenge'''
    pass

def automated_docking():
    '''Function to execute speed automated docking'''
    pass

def find_the_path():
    '''Function to execute find the path'''
    pass

def follow_the_leader():
    '''Function to execute follow the leader'''
    pass

def autonomus_nav():
    '''Function to execute autonomus nav'''
    pass

def gps_nav_to_sc():
    '''Navigate to speed challenge coords'''
    pass

def gps_nav_to_ac():
    '''Navigate to automated docking'''
    pass

def gps_nav_to_fp():
    '''Navigate to find the path coords'''
    pass

def gps_nav_to_fl():
    '''Navigate to follow the leader'''
    pass

def start_run_server():
    '''Funciont to ask for permission to start a run'''
    # Call server to start course
    conn = http.client.HTTPConnection(IP_ADDR)
    headers = {'Content-type': 'application/json'}
    foo = {'text': 'Hello HTTP #1 **cool**, and #1!'}
    json_data = json.dumps(foo)
    #conn.request('POST', START_RUN + COURSE + TEAM_CODE, json_data, headers)
    conn.request('POST', '/testCourse1', json_data, headers)

    response = conn.get_response()
    print(response.read().decode())
    return True

def main():
    '''Main program'''
    # Ask server to start run
    # start = False
    # while not start:
    #     start = start_run_server()

    pass

main()
