import threading
# Add your imports here, if any
from utils.brick import BP, Motor, EV3ColorSensor, wait_ready_sensors, TouchSensor, reset_brick, EV3UltrasonicSensor
from time import sleep
import time
import wallfollowing

flags = { "flag1" : True, "flag2": True}

flags_lock = threading.Lock()


DELAY = 0.1
cs_data = "floor_yellow_results.csv"

# complete this based on your hardware setup

 # Input True to see what the robot is trying to initialize! False to be silent.

BP.reset_all()

DPS = 0
SLEEP_MOTOR = 3
SLEEP_US = 0.3
DELAY = 0.1
cs_data = "test_results.csv"
 
# sensors and motors

wall_us = EV3UltrasonicSensor(2)
touch_sensor = TouchSensor(3)
color_left = EV3ColorSensor(1)
left_motor = Motor("C")
right_motor = Motor("B")


wait_ready_sensors(True)

# Returns the mean of three values

def mean(first, second, third):
    return ((first + second + third) / 3)

# Robot moves forward while turning left

def move_left_arc(dps, sleep_motor):
    print("left arc")
    rt = threading.Thread(target = move_right_forward, args = (dps, sleep_motor))
    lt = threading.Thread(target = move_left_forward, args = ((dps-5), sleep_motor))
    rt.start()
    lt.start()

# left wheel of the robot moves at [dps] speed for [sleep_motor] seconds

def move_left_forward(dps, sleep_motor):
    print("left")
    left_motor.set_power(-dps)  
    sleep(sleep_motor)
    left_motor.set_power(0)
    #BP.reset_all()
 
 # right wheel of the robot moves at [dps] speed for [sleep_motor] seconds
 
def move_right_forward(dps, sleep_motor):
    print("right")
    right_motor.set_power(-dps)
    sleep(sleep_motor)
    right_motor.set_power(0)
    #BP.reset_all()

# Use threads to move the robot forward

def move_forward(d, s): # to avoid setting dps for a fixed amount of time,
                        # move each wheel in a separate thread 
    rf = threading.Thread(target = move_right_forward, args = (d, s))
    lf = threading.Thread(target = move_left_forward, args = (d, s))
    rf.start()
    lf.start()

# Use threads to turn the robot right

def turn_right(d, s): # to avoid setting dps for a fixed amount of time,
                        # move each wheel in a separate thread 
    rt = threading.Thread(target = move_right_forward, args = (d, s))
    lt = threading.Thread(target = move_left_forward, args = (-d, s))
    rt.start()
    lt.start()

# def new_move_forward(dps, sleep_motor):
#     for i in range(sleep_motor):
#         left_motor.set_power(dps)
#         right_motor.set_power(dps)
#         sleep(i)
#     BP.reset_all()

# Stop moving by setting power 0 (without threads)
    
def stop_moving(sleep_motor):
    left_motor.set_dps(0)
    right_motor.set_dps(0)
    sleep(sleep_motor)
    
# def get_distance_to_block(SLEEP_US):
#     for i in range(20):
#         print("block:", block_ultrasonic.get_value())
#         sleep(SLEEP_US)
# 
# 
# def get_distance_to_wall(SLEEP_US):
#     for i in range(20):
#         print("wall", wall_ultrasonic.get_value())
#         sleep(SLEEP_US)


#!/usr/bin/env python3

#Normalized Block Color Ranges from the collected data

#Blue: R[0.0, 0.25] G[0.0, 0.4] B[0.5238, 1.0]

#Yellow: R[0.460, 0.549] G[0.333, 0.4385] B[0.0701, 0.1746]

#Red: R[0.48275, 0.6521] G[0.0434, 0.2333] B[0.2083, 0.4137]

#Green: R[0.1538, 0.375] G[0.40625, 0.6842] B[0.0, 0.28125]


##This decision tree decides the color of floor based on some basic data analysis
def classify_color(r, g, b):
    #if (0.48<r<0.53 and 0.15<g<0.35 and 0.1<b<0.14)
     #   return "border bt red and green"
    if 0.41<r<0.5625 and 0.2258<g<0.44 and b<0.2564:
        return "border"
    if r <= 0.418:
        if g <= 0.4:
            return "blue"
        else:
            return "green"
    else:
        if g <= 0.283:
        #if g <= 0.41:
            return "red"
        #else:
        #    return "yellow"

def normalize(r, g, b):
#     print(r, g, b)
    r_norm = r/(r+g+b)
    g_norm = g/(r+g+b)
    b_norm = b/(r+g+b)

    return(r_norm, g_norm, b_norm)


#this runs similarly to the color collection program, but instead of printing the RGB values
#That is collects, it prints what it thinks the color of the floor is
#it only returns a value("blue") when it detects blue
def left_continuous_color_sensor_collection():
    counter = 0
    
    #These variables hold the three values that will be averaged in order to calculate the "current color guess"
    first = (0, 0, 1)
    second = (0, 0, 1)
    third = (0, 0, 1)

    while counter < 600:
        counter += 1
        color_data = color_left.get_rgb()
#         print(color_data)
        if color_data[0] is not None:
            normalized_tuple = normalize(color_data[0], color_data[1], color_data[2])
            

            ##this uses the most recent collection and updates first, second and third
            third = second
            second = first
            first = normalized_tuple

            newR = mean(first[0], second[0], third[0])
            newG = mean(first[1], second[1], third[1])
            newB = mean(first[2], second[2], third[2])

            decision = classify_color(normalized_tuple[0], normalized_tuple[1], normalized_tuple[2])
#             print(normalized_tuple)
            print(decision)
            if decision == "blue":
                return decision
#             else: pass
        sleep(0.1)

#this runs similarly to the color collection program, but instead of printing the RGB values
#That is collects, it prints what it thinks the color of the floor is
#it only returns a value("green") when it detects green
def left_green_continuous_color_sensor_collection():
    counter = 0
    
    #These variables hold the three values that will be averaged in order to calculate the "current color guess"
    first = (0, 0, 1)
    second = (0, 0, 1)
    third = (0, 0, 1)

    while counter < 600:
        counter += 1
        color_data = color_left.get_rgb()
#         print(color_data)
        if color_data[0] is not None:
            normalized_tuple = normalize(color_data[0], color_data[1], color_data[2])
            

            ##this uses the most recent collection and updates first, second and third
            third = second
            second = first
            first = normalized_tuple

            newR = mean(first[0], second[0], third[0])
            newG = mean(first[1], second[1], third[1])
            newB = mean(first[2], second[2], third[2])

            decision = classify_color(normalized_tuple[0], normalized_tuple[1], normalized_tuple[2])
#             print(normalized_tuple)
            print(decision)
            if decision == "green":
                
                return decision
#             else: pass
        sleep(0.1)
#this runs similarly to the color collection program, but instead of printing the RGB values
#That is collects, it prints what it thinks the color of the floor is
# def center_continuous_color_sensor_collection():
#     counter = 0
#     
#     #These variables hold the three values that will be averaged in order to calculate the "current color guess"
#     first = (0, 0, 1)
#     second = (0, 0, 1)
#     third = (0, 0, 1)
# 
#     while counter < 600:
#         counter += 1
#         color_data = color_center.get_rgb()
# #         print(color_data)
#         if color_data[0] is not None:
#             normalized_tuple = normalize(color_data[0], color_data[1], color_data[2])
#             
# 
#             ##this uses the most recent collection and updates first, second and third
#             third = second
#             second = first
#             first = normalized_tuple
# 
#             newR = mean(first[0], second[0], third[0])
#             newG = mean(first[1], second[1], third[1])
#             newB = mean(first[2], second[2], third[2])
# 
#             decision = classify_color(normalized_tuple[0], normalized_tuple[1], normalized_tuple[2])
# #             print(normalized_tuple)
# #             print(decision)
#             if decision == "blue":
#                 return decision
# #             else: pass
#         sleep(0.1)
# 
# def constant_color_sensor_collection():
#     counter = 0
#     
#     #These variables hold the three values that will be averaged in order to calculate the "current color guess"
#     first = (0, 0, 1)
#     second = (0, 0, 1)
#     third = (0, 0, 1)
# 
#     while counter < 600:
#         counter += 1
#         color_data = color.get_rgb()
#         print(color_data)
#         if color_data[0] is not None:
#             normalized_tuple = normalize(color_data[0], color_data[1], color_data[2])
#             
# 
#             ##this uses the most recent collection and updates first, second and third
#             third = second
#             second = first
#             first = normalized_tuple
# 
#             newR = mean(first[0], second[0], third[0])
#             newG = mean(first[1], second[1], third[1])
#             newB = mean(first[2], second[2], third[2])
# 
#             decision = classify_color(normalized_tuple[0], normalized_tuple[1], normalized_tuple[2])
#             print(normalized_tuple)
#             print(decision)
#             return decision
# #             else: pass
#         sleep(0.1)

# not used                
# def choose_direction():
#     right_counter = 0
#     left_counter = 0
#     turn_right(-20,15)
#     while right_counter <= 25:
#         detection = constant_color_sensor_collection()
#         if detection == "green":
#             stop_moving(0.5)
#             turn_right(20,15)
#             sleep(0.3*right_counter)
#             stop_moving(0.5)
#             break
#         sleep(0.3)
#         right_counter += 1
#     turn_right(20,15)
#     while left_counter <= 25:
#         detection = constant_color_sensor_collection()
#         if detection == "green":
#             stop_moving(0.5)
#             turn_right(-20,15)
#             sleep(0.3*left_counter)
#             stop_moving(0.5)
#             break
#         sleep(0.3)
#         left_counter += 1
#     if right_counter >= left_counter:
#         direction = 1
#     else: direction = -1
#     return direction


# this function is part of a iterative function.
# it 
def around_water(detection_l):
    detection_l = left_continuous_color_sensor_collection()  # It starts detecting the color of the floor until it detects blue,
    if detection_l == "blue":
        stop_moving(1)
        turn_right(-15,15) # turns right
        sleep(0.3)         # the sleep is to put a slight delay until the color sensor starts detecting again
        detection_l = left_green_continuous_color_sensor_collection() # starts detecting for green while turning
        if detection_l == "green": # when it detects green, stop and move forward and left
            stop_moving(1)
            move_left_arc(30,15)
            sleep(0.3)   # the same function will be called right after in order to stop the robot when detecting blue.

            
        



    

def main_function():
    
    wall_distance = 4

    print("hi")
    sleep(4)
    #move_forward(30,15)
    wallthread = threading.Thread(target = wallfollowing.wallfollowing_f, args = (100, wall_distance))
    colorthread = threading.Thread(target = wallfollowing.left_continuous_color_sensor_collection, args = ())
    wallthread.start()
    colorthread.start()
#     with flags_lock:
#         flags["flag1"] = True
    detections_l = []
    for i in range(20):
        detections_l.append("")
    for i in range(len(detections_l)):
        around_water(detections_l[i])
        actual_distance = wall_us.get_value()
#         if abs(wall_distance - actual_distance) <= 3:
#             break
#     wallthread.join()
        


    
    
    

main_function()


# move_forward(40,1)
# stop_moving(0.5)

