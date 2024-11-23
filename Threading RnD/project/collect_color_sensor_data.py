#!/usr/bin/env python3

"""
This test is used to collect data from the color sensor.
It must be run on the robot.
"""

# Add your imports here, if any
from utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor, reset_brick
from time import sleep

DELAY = 0.3
cs_data = "../data_analysis/color_sensor_test_blue.csv"

# complete this based on your hardware setup
COLOR_SENSOR = EV3ColorSensor(2)
TOUCH_SENSOR = TouchSensor(1)



wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.


def collect_color_sensor_data():
    counter = 0
    "Collect color sensor data."
    while counter < 30:
        output_file = open(COLOR_SENSOR_DATA_FILE, "a")
        while not TOUCH_SENSOR.is_pressed():
            pass
        if TOUCH_SENSOR.is_pressed():
            #print("pressed")
            counter += 1
            color_data = COLOR_SENSOR.get_rgb()
            if color_data is not None:
                print(color_data)
                output_file.write(f"{color_data}\n")
            sleep(1)


    print("Done collecting CS color samples")
    output_file.close()
    reset_brick() # Turn off everything on the brick's hardware, and reset it
    exit()
    
def continuous_color_sensor_collection():
    counter = 0
    output_file = open(cs_data, "w")
    while counter < 60:
        counter += 1
        color_data = COLOR_SENSOR.get_rgb()
        if color_data is not None:
            print(color_data)
            output_file.write(f"{color_data}\n")
        sleep(0.1)
    output_file.close()
    reset_brick()
    exit()
                



if __name__ == "__main__":
    continuous_color_sensor_collection()
