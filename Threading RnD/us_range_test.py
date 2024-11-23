from utils.brick import wait_ready_sensors, EV3UltrasonicSensor, EV3GyroSensor, Motor, BP
import math
import time
from time import sleep
import SLAM
import threading
BP.reset_all()
# Initialize sensors
wall_us = EV3UltrasonicSensor(3)

#wait_ready_sensors()

def get_wall_US_distance():
    for i in range(400):
        if wall_us.get_value() == None:
            z = 0
        else:  
            z = wall_us.get_value()
            
        distance = [float(z)]
        time.sleep(0.3)
        print(distance)
        
#wait_ready_sensors()
time.sleep(3.3)
print("distance:",get_wall_US_distance())