#!/usr/bin/env python3

#Normalized Block Color Ranges!

#Yellow: R[0.484, 0.524], G[0.417, 0.464, 0.0211, 0.08917]

#Blue: R[0.0526, 0.2307] G[0.2045, 0.3947] B[0.4883, 0.6363]

#Purple: R[0.3875, 0.7936] G[0.0615, 0.16216] B[0.09375, 0.175]

#Green: R[0.06521, 0.1724] G[0.5254, 0.7333] B[0.1777, 0.3220]


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


##This decision tree decides the color of floor based on some basic data analysis
def classify_color(r, g, b):

    if b <= 0.302:
        if b <= 0.111:
            return "yellow"
        else:
            return "orange"
    else:
        if r <= 0.247:
            return "blue"
        else:
            return "purple"
        
def normalize(r, g, b):
    r_norm = r/(r+g+b)
    g_norm = g/(r+g+b)
    b_norm = b/(r+g+b)

    return(r_norm, g_norm, b_norm)


#These variables hold the three values that will be averaged in order to calculate the "current color guess"
first = (0, 0, 0)
second = (0, 0, 0)
third = (0, 0, 0)


#this runs similarly to the color collection program, but instead of printing the RGB values
#That is collects, it prints what it thinks the color of the floor is
def continuous_color_sensor_collection():
    counter = 0


    while counter < 600:
        counter += 1
        color_data = COLOR_SENSOR.get_rgb()
        if color_data is not None:

            normalized_tuple = normalize(color_data[0], color_data[1], color_data[2])

            ##this uses the most recent collection and updates first, second and third
            third = second
            second = first
            first = normalized_tuple

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