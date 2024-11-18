#!/usr/bin/env python3

"""
This test is used to collect data from the color sensor.
It must be run on the robot.
"""

# Add your imports here, if any
from utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor, reset_brick
from time import sleep

DELAY = 0.1
cs_data = "ugreen.csv"

# complete this based on your hardware setup
COLOR_SENSOR = EV3ColorSensor(2)



wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.



def continuous_color_sensor_collection():
    counter = 0
    output_file = open(cs_data, "w")
    while counter < 200:
        counter += 1
        color_data = COLOR_SENSOR.get_rgb()
        if color_data is not None:
            r = color_data[0]
            g = color_data[1]
            b = color_data[2]
            print(color_data)
            output_file.write(f"{r}, {g}, {b}\n")
        sleep(0.1)
    output_file.close()
    reset_brick()
    exit()
                



if __name__ == "__main__":
    continuous_color_sensor_collection()
