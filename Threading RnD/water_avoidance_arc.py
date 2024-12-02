import threading
# Add your imports here, if any
from utils.brick import BP, Motor, EV3ColorSensor, wait_ready_sensors, TouchSensor, reset_brick, EV3UltrasonicSensor
from time import sleep
import time
import wallfollowing

flags_high = { "water_avoid_mode" : False, "navigation_mode" : False }
flags_low = { "grass": False, "water" : True, "parallel" : False, "hitting_wall": False }

flags_lock1 = threading.Lock()
flags_lock2 = threading.Lock()


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

block_us = EV3UltrasonicSensor(4)
wall_us = EV3UltrasonicSensor(2)
touch_sensor = TouchSensor(3)
color_left = EV3ColorSensor(1)
left_motor = Motor("C")
right_motor = Motor("D")


wait_ready_sensors(True)

# Returns the mean of three values

def mean(first, second, third):
    return ((first + second + third) / 3)

# Robot moves forward while turning left

def move_left_arc(dps, sleep_motor):
    print("left arc")
    distance_list = [255,255,255]
    i = 0
    j = 3
    while i < sleep_motor:
        distance = wall_us.get_value()
        distance_list.append(distance)
        mean_distance = (distance_list[j] + distance_list[j-1] + distance_list[j-2])/3
        print(distance)
        print(mean_distance)
        left_motor.set_power(-(dps-5))
        right_motor.set_power(-dps)
        with flags_lock2:
            if flags_low["water"]:
                print(flags_low["water"])
                left_motor.set_power(0)
                right_motor.set_power(0)
                return None
            if flags_low["parallel"]:
                print(flags_low["parallel"])
                left_motor.set_power(0)
                right_motor.set_power(0)
                return "parallel"
        if mean_distance <= 7.5:
            print("too close to the wall")
            left_motor.set_power(20)
            right_motor.set_power(18)
            sleep(1)
            left_motor.set_power(0)
            right_motor.set_power(0)
            with flags_lock2:
                flags_low["hitting_wall"] = True
                return None
        if touch_sensor.is_pressed():
            print("too close to the wall")
            left_motor.set_power(20)
            right_motor.set_power(18)
            sleep(1)
            left_motor.set_power(0)
            right_motor.set_power(0)
            with flags_lock2:
                flags_low["hitting_wall"] = True
                return None
        print("touch sensor: " + str(touch_sensor.is_pressed()))
        print("still going")
        i += 0.1
        j += 1
        sleep(0.1)
    left_motor.set_power(0)
    right_motor.set_power(0)
    
    
#     rt = threading.Thread(target = move_right_forward, args = (dps, sleep_motor))
#     lt = threading.Thread(target = move_left_forward, args = ((dps-5), sleep_motor))
#     rt.start()
#     lt.start()

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

def move_forward(dps, sleep_motor): # to avoid setting dps for a fixed amount of time,
                        # move each wheel in a separate thread 
    print("move_forward")
    i = 0
    while i < sleep_motor:
        left_motor.set_power(-(dps+2))
        right_motor.set_power(-dps)
        i += 0.1
        sleep(0.1)
    left_motor.set_power(0)
    right_motor.set_power(0) 

# Use threads to turn the robot right

def turn_right(dps, sleep_motor):
    
    distance_list = [255,255,255]
    print("turn_right")
    with flags_lock1:
        if flags_high["water_avoid_mode"]:
            print("water_avoid_mode")
            i = 0
            j = 3
            while i < sleep_motor:
                distance = wall_us.get_value()
                distance_list.append(distance)
                mean_distance = (distance_list[j] + distance_list[j-1] + distance_list[j-2])/3
                print(distance)
                print(mean_distance)
                left_motor.set_power(-dps)
                right_motor.set_power(dps)
                with flags_lock2:
                    if flags_low["grass"]:
                        print(flags_low["grass"])
                        left_motor.set_power(0)
                        right_motor.set_power(0)
                        return None
                    if flags_low["parallel"]:
                        print(flags_low["parallel"])
                        left_motor.set_power(0)
                        right_motor.set_power(0)
                        return None
                print("still going")
                if mean_distance <= 7.5:
                    print("too close to the wall")
                    left_motor.set_power(20)
                    right_motor.set_power(18)
                    sleep(1)
                    left_motor.set_power(0)
                    right_motor.set_power(0)
                    with flags_lock2:
                        flags_low["hitting_wall"] = True
                        return None
                if touch_sensor.is_pressed():
                    print("too close to the wall")
                    left_motor.set_power(20)
                    right_motor.set_power(18)
                    sleep(1)
                    left_motor.set_power(0)
                    right_motor.set_power(0)
                    with flags_lock2:
                        flags_low["hitting_wall"] = True
                        return None
                print("touch sensor: " + str(touch_sensor.is_pressed()))
                i += 0.1
                j += 1
                sleep(0.1)
            left_motor.set_power(0)
            right_motor.set_power(0)
        if flags_high["navigation_mode"]:
            print("navigation_mode")
            i = 0
            while i < sleep_motor:
                left_motor.set_power(-dps)
                right_motor.set_power(dps)
                i += 0.1
                sleep(0.1)
            left_motor.set_power(0)
            right_motor.set_power(0)
    

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
        if g <= 0.36:
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
#             print(decision)
            if decision == "blue":
                with flags_lock2:
                    flags_low["water"] = True
                    flags_low["grass"] = False
                return decision
            with flags_lock2:
                if flags_low["parallel"] == True:
                    return None
                if flags_low["hitting_wall"] == True:
                    return None
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
            print(normalized_tuple)
            print(decision)
            if decision == "green":
                with flags_lock2:
                    flags_low["grass"] = True
                    flags_low["water"] = False
                return decision
            with flags_lock2:
                if flags_low["parallel"] == True:
                    return None
                if flags_low["hitting_wall"] == True:
                    return None
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

            
        
def collect_data():
    BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    
    while True:
        Encoder_left_motor = BP.get_motor_encoder(BP.PORT_C)
        Encoder_right_motor = BP.get_motor_encoder(BP.PORT_D)
        print("left_motor: " + str(Encoder_left_motor))
        print("right_motor: " + str(Encoder_right_motor))
        
        with flags_lock2:
            if flags_low["hitting_wall"]:
                print("stop data")
                return None
        
        if abs(Encoder_left_motor) >= 20 and abs(Encoder_right_motor) >= 20:
            if abs(Encoder_left_motor - Encoder_right_motor) <= 3:
                with flags_lock2:
                    flags_low["parallel"] = True
                    return None
        
        sleep(0.1)
    


    

def main_function():
    
    avg_wall_distance = []
    for i in range(6):
        wall_distance = wall_us.get_value()
        print(wall_distance)
        avg_wall_distance.append(wall_distance)
        sleep(0.1)
    
    avg = (avg_wall_distance[3] + avg_wall_distance[4] + avg_wall_distance[5])/3
    print(avg)

    print("hi")
    sleep(4)
    #move_forward(30,15)
    wallthread = threading.Thread(target = wallfollowing.wallfollowing_f, args = (100, avg))
    colorthread = threading.Thread(target = wallfollowing.left_continuous_color_sensor_collection, args = ())
    datathread = threading.Thread(target = collect_data, args = ())
    wallthread.start()
    colorthread.start()
    
    wallthread.join()
    colorthread.join()
    flags_high["water_avoid_mode"] = True
    
    datathread.start()
    
#     with flags_lock:
#         flags["flag1"] = True

    for i in range(20):
        arc_thread = threading.Thread(target = turn_right, args = (22,15))
#         sleep(0.1)
        color_thread = threading.Thread(target = left_green_continuous_color_sensor_collection, args = ())
        arc_thread.start()
        color_thread.start()
        arc_thread.join()
        color_thread.join()
        
        arc_thread = threading.Thread(target = move_left_arc, args = (22,15))
#         sleep(0.1)
        color_thread = threading.Thread(target = left_continuous_color_sensor_collection, args = ())
        arc_thread.start()
        color_thread.start()
        arc_thread.join()
        color_thread.join()
        
     
        
        with flags_lock2:
            if flags_low["parallel"]:
                print("done!")
                break
                
            if flags_low["hitting_wall"]:
                print("don't wannt hit the wall!")
                break
            
    datathread.join()
    with flags_lock2:
        
        if flags_low["parallel"]:
            print("done!")
            left_motor.set_power(0)
            right_motor.set_power(0)
            print("end")
            
            avg_distance = []
            for i in range(6):
                distance = wall_us.get_value()
                print(distance)
                avg_distance.append(distance)
                sleep(0.1)
            
            avg = (avg_distance[3] + avg_distance[4] + avg_distance[5])/3
            print(avg)
            wallthread_1 = threading.Thread(target = wallfollowing.wallfollowing_f, args = (100, avg))
            wallthread_1.start()
                
        elif flags_low["hitting_wall"]:
            print("don't wannt hit the wall!")
            left_motor.set_power(0)
            right_motor.set_power(0)
            print("end")
            
            left_motor.set_power(20)
            right_motor.set_power(18)
            sleep(0.8)
            wallthread_1 = threading.Thread(target = wallfollowing.wallfollowing_f, args = (100, 3))
            wallthread_1.start()
            
        
#     for i in range(len(detections)):
#         around_water(detections[i])
#         print(flags)
#         with flags_lock:
#             if flags["parallel"] == True:
#                 stop_moving(1)
#                 print("now parallel")
#                 break
#             elif flags["parallel"] == False:
#                 continue
#     print("End")

#         actual_distance = wall_us.get_value()
        
#         if abs(wall_distance - actual_distance) <= 3:
#             break
#     wallthread.join()
        


    
    
    

main_function()
# while True:
#     print(touch_sensor.is_pressed())
#     sleep(0.1)

# arc_thread = threading.Thread(target = move_left_arc, args = (30,15))
# color_thread = threading.Thread(target = left_continuous_color_sensor_collection, args = ())
# 
# arc_thread.start()
# color_thread.start()
# datathread = threading.Thread(target = collect_data, args = ())
# datathread.start()





# move_forward(40,1)
# stop_moving(0.5)

