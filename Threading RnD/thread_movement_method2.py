import threading
# Add your imports here, if any
from utils.brick import BP, Motor, EV3ColorSensor, wait_ready_sensors, TouchSensor, reset_brick, EV3UltrasonicSensor
from time import sleep

DELAY = 0.1
cs_data = "floor_yellow_results.csv"

# complete this based on your hardware setup

#TOUCH_SENSOR = TouchSensor(1)



wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.


BP.reset_all()

DPS = 0
SLEEP_MOTOR = 3
SLEEP_US = 0.3
DELAY = 0.1
cs_data = "test_results.csv"
 

#block_ultrasonic = EV3UltrasonicSensor(1)
wall_ultrasonic = EV3UltrasonicSensor(2)
color_center = EV3ColorSensor(4)
color_left = EV3ColorSensor(1)
#wall_ultrasonic = EV3Ultrasonic Sensor(2)
left_motor = Motor("C")
right_motor = Motor("B")
#wait_ready_sensors()

def mean(first, second, third):
    return ((first + second + third) / 3)

def move_left_forward(dps, sleep_motor):
    print("left")
    left_motor.set_power(-dps)  
    sleep(sleep_motor)
    left_motor.set_power(0)
    #BP.reset_all()
    
def move_right_forward(dps, sleep_motor):
    print("right")
    right_motor.set_power(-dps)
    sleep(sleep_motor)
    right_motor.set_power(0)
    #BP.reset_all()
    
def move_forward(d, s): # to avoid setting dps for a fixed amount of time,
                        # move each wheel in a separate thread 
    rf = threading.Thread(target = move_right_forward, args = (d, s))
    lf = threading.Thread(target = move_left_forward, args = (d, s))
    rf.start()
    lf.start()

def turn_right(d, s): # to avoid setting dps for a fixed amount of time,
                        # move each wheel in a separate thread 
    rt = threading.Thread(target = move_right_forward, args = (d, s))
    lt = threading.Thread(target = move_left_forward, args = (-d, s))
    rt.start()
    lt.start()

def new_move_forward(dps, sleep_motor):
    for i in range(sleep_motor):
        left_motor.set_power(dps)
        right_motor.set_power(dps)
        sleep(i)
    BP.reset_all()
    
def stop_moving(sleep_motor):
    left_motor.set_dps(0)
    right_motor.set_dps(0)
    sleep(sleep_motor)
    
def get_distance_to_block(SLEEP_US):
    for i in range(20):
        print("block:", block_ultrasonic.get_value())
        sleep(SLEEP_US)


def get_distance_to_wall(SLEEP_US):
    for i in range(20):
        print("wall", wall_ultrasonic.get_value())
        sleep(SLEEP_US)


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
                return decision
#             else: pass
        sleep(0.1)


#this runs similarly to the color collection program, but instead of printing the RGB values
#That is collects, it prints what it thinks the color of the floor is
def center_continuous_color_sensor_collection():
    counter = 0
    
    #These variables hold the three values that will be averaged in order to calculate the "current color guess"
    first = (0, 0, 1)
    second = (0, 0, 1)
    third = (0, 0, 1)

    while counter < 600:
        counter += 1
        color_data = color_center.get_rgb()
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
                return decision
#             else: pass
        sleep(0.1)

def constant_color_sensor_collection():
    counter = 0
    
    #These variables hold the three values that will be averaged in order to calculate the "current color guess"
    first = (0, 0, 1)
    second = (0, 0, 1)
    third = (0, 0, 1)

    while counter < 600:
        counter += 1
        color_data = color.get_rgb()
        print(color_data)
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
            return decision
#             else: pass
        sleep(0.1)
                
def choose_direction():
    right_counter = 0
    left_counter = 0
    turn_right(-20,15)
    while right_counter <= 25:
        detection = constant_color_sensor_collection()
        if detection == "green":
            stop_moving(0.5)
            turn_right(20,15)
            sleep(0.3*right_counter)
            stop_moving(0.5)
            break
        sleep(0.3)
        right_counter += 1
    turn_right(20,15)
    while left_counter <= 25:
        detection = constant_color_sensor_collection()
        if detection == "green":
            stop_moving(0.5)
            turn_right(-20,15)
            sleep(0.3*left_counter)
            stop_moving(0.5)
            break
        sleep(0.3)
        left_counter += 1
    if right_counter >= left_counter:
        direction = 1
    else: direction = -1
    return direction

def around_water(detection_l, detection_c):
    detection_c = center_continuous_color_sensor_collection()
    detection_l = left_continuous_color_sensor_collection()
    print("left: " + detection_l + "center: " + detection_c)
    if detection_c or detection_l == "blue":
        stop_moving(1)
        turn_right(-20,15)
        print("detection: " + detection_l + " and " + detection_c)
    

def main_function():
    

    #t3 = threading.Thread(target = get_distance_to_block, args = (0.3,))
    #t4 = threading.Thread(target = stop_moving, args = (2,))
    #t5 = threading.Thread(target = get_distance_to_wall, args = (0.3,))
    print("hi")
    sleep(4)
    #move_forward(30,15)
    move_forward(30,15)
    detection_l0 = ""
    detection_c0 = ""
    detection_l1 = ""
    detection_c1 = ""
    detection_l2 = ""
    detection_c2 = ""
    detection_l3 = ""
    detection_c3 = ""
    detection_l4 = ""
    detection_c4 = ""
    detection_c = center_continuous_color_sensor_collection()
    detection_l = left_continuous_color_sensor_collection()
    if detection_c or detection_l == "blue":
        stop_moving(1)
        turn_right(-20,0.8)
        sleep(0.8)
        move_forward(20,1.5)
        sleep(2)
        turn_right(20,15)
        detection_c0 = center_continuous_color_sensor_collection()
        detection_l0 = left_continuous_color_sensor_collection()
        if detection_c0 or detection_l0 == "blue":
            stop_moving(1)
            turn_right(-20,0.8)
            sleep(0.8)
            move_forward(20,1.5)
            sleep(2)
            turn_right(20,15)
            detection_c1 = center_continuous_color_sensor_collection()
            detection_l1 = left_continuous_color_sensor_collection()
            if detection_c1 or detection_l1 == "blue":
                stop_moving(1)
                turn_right(-20,0.8)
                sleep(0.8)
                move_forward(20,1.5)
                sleep(2)
                turn_right(20,15)
                detection_c2 = center_continuous_color_sensor_collection()
                detection_l2 = left_continuous_color_sensor_collection()
                if detection_c2 or detection_l2 == "blue":
                    stop_moving(1)
                    turn_right(-20,0.8)
                    sleep(0.8)
                    move_forward(20,1.5)
                    sleep(2)
                    turn_right(20,15)
                detection_c3 = center_continuous_color_sensor_collection()
                detection_l3 = left_continuous_color_sensor_collection()
                if detection_c3 or detection_l3 == "blue":
                    stop_moving(1)
                    turn_right(-20,0.8)
                    sleep(0.8)
                    move_forward(20,1.5)
                    sleep(2)
                    turn_right(20,15)
            
        #     move_forward(40,0.5)
#     sleep(0.5)
#     turn_right(20,1)
#     around_water(detection_2)
#     print("still going")
#     move_forward(40,0.5)
#     sleep(0.5)
#     turn_right(20,1)
#     around_water(detection_3)
    

    
    
    
#
    
# def follow_border():
#     # If the distance from the wall is "too small, the robot will move away from the wall
#     seconds = 0
#     direction = -1
#     while seconds <= 200:
#         detection = constant_color_sensor_collection()
#         print(detection)
#         #if the distance from the wall is within 2 cm of the desired distance, the robot will continue moving forward
#         if detection != "red" or "border":
#             if direction == 1:
#                 left_motor.set_power(-15)
#                 right_motor.set_power(-20)
#                 sleep(0.5
#                 direction = -1
#             if direction == -1:
#                 left_motor.set_power(-20)
#                 right_motor.set_power(-15)
#                 sleep(0.5)
#                 direction = 1
#         # If the distance from the wall is too large, the robot will adjust itself to move closer to the wall
#         elif detection == "red" or "border":
#             left_motor.set_power(-20)
#             right_motor.set_power(-20)
#             sleep(0.5)
#         seconds += seconds
        # If the distance from the wall is too small, the robot will adjust itself to move away from the wall

#     if detection == "blue" or "red" or "border":
#         stop_moving(1)
#         turn_right(-20,15)
#         sleep(2)
#         stop_moving(5)
#         print("still going")
#         continuous_color_sensor_collection()
        
#         if detection_1 == "red":
#             stop_moving(0.5)
#             move_forward(20,15)
#             sleep(0.5)
#         continuous_color_sensor_collection()
#         if continuous_color_sensor_collection() == "red":
#             stop_moving(3)
#             turn_right(20, 15)
#             sleep(0.5)
#         continuous_color_sensor_collection()
#         if continuous_color_sensor_collection() == "red":
#             stop_moving(0.5)
#             move_forward(20,15)
#             sleep(0.5)
#         continuous_color_sensor_collection()
#         if continuous_color_sensor_collection() == "red":
#             stop_moving(0.5)
#             turn_right(20,15)
#             sleep(0.5)
        
        
    


#     t3.start()
#     t5.start()
#     time.sleep(6)
#     t4.start()
    #print("bye")
    
#print("hello world")
main_function()
#turn_right(-20,2.5)
#sleep(3)
#print(choose_direction())

#move_forward(-40,4)
#follow_border()



