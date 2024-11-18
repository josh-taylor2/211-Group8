#!/usr/bin/env python3

"""
This test is used to collect data from the color sensor.
It must be run on the robot.
"""

def mean(int1, int2, int3):
    return ((int1+int2+int3)/3)

# Add your imports here, if any
from utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor, reset_brick
from time import sleep

DELAY = 0.1
cs_data = "floor_yellow_results.csv"

# complete this based on your hardware setup
COLOR_SENSOR = EV3ColorSensor(2)
TOUCH_SENSOR = TouchSensor(1)



wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.

#These variables hold the three values that will be averaged in order to calculate the "current color guess"
first = []
second = [0, 0, 0]
third = [0, 0, 0]


##This decision tree decides the color of floor based on some basic data analysis
def classify_color(r, g, b):

    if r>= 15 and g >= 12 and b <=7:
        return 4
    
    elif r >= 10 and g <= 9 and b<= 6:
        return 1
    
    elif g >= 10 and r <= 10 and b <= 6:
        return 3
    elif b >=4 and r <= 5 and g <=5:
        return 2
    else:
        return 0


#this runs similarly to the color collection program, but instead of printing the RGB values
#That is collects, it prints what it thinks the color of the floor is
def continuous_color_sensor_collection():
    counter = 0


    while counter < 600:
        counter += 1
        color_data = COLOR_SENSOR.get_rgb()
        if color_data is not None:

            r = color_data[0]
            g = color_data[1]
            b = color_data[2]

            ##this uses the most recent collection and updates first, second and third
            first = [r, g, b]
            second = [first[0], first[1], first[2]]
            third = [second[0], second[1], second[2]]

            newR = mean(first[0], second[0], third[0])
            newG = mean(first[1], second[1], third[1])
            newB = mean(first[2], second[2], third[2])

            decision = classify_color(newR, newG, newB)

            print(decision)
        sleep(0.1)
    reset_brick()
    exit()
                



if __name__ == "__main__":
    continuous_color_sensor_collection()


    