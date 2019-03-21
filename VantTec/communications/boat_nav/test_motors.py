from motors import Motors
import serial
import time
def kill_me():
    ser = serial.Serial('/dev/ttyACM0', 115200)
    val = '%B,1600,1600%'.encode()
    #val2 = '%B,1500,1500%'
    #print('value: ', val)
    #val2 = val2.encode()
    time.sleep(10)
    ser.write(val)
    #ser.write(val2)
    ser.close()

def test_m():
    motors = Motors()
    motors.move_thrusters(1530,1470)
    time.sleep(5)
    motors.move_thrusters(1500, 1500)

#kill_me()
test_m()
