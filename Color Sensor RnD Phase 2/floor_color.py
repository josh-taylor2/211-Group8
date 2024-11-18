#!/usr/bin/env python3

#Normalized Block Color Ranges from the collected data

#Blue: R[0.0, 0.25] G[0.0, 0.4] B[0.5238, 1.0]

#Yellow: R[0.460, 0.549] G[0.333, 0.4385] B[0.0701, 0.1746]

#Red: R[0.48275, 0.6521] G[0.0434, 0.2333] B[0.2083, 0.4137]

#Green: R[0.1538, 0.375] G[0.40625, 0.6842] B[0.0, 0.28125]


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

    if r <= 0.418:
        if g <= 0.4:
            return "blue"
        else:
            return "green"
    else:
        if g <= 0.283:
            if b < 0.28:
                return "yellow"
            return "red"
        else:

            return "yellow"
        
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