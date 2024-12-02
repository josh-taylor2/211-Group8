import threading
# Add your imports here, if any
from utils.brick import BP, Motor, EV3ColorSensor, wait_ready_sensors, TouchSensor, reset_brick, EV3UltrasonicSensor
from time import sleep
import time
import wallfollowing

# set "water_avoid_mode" or "navigation_mode" for movement functions using flag lock
flags_high = { "water_avoid_mode" : False, "navigation_mode" : False }

# communicate between threads in case of encountering water, grass, and wall while avoidng water
# using anoter set of flag lock
flags_low = { "grass": False, "water" : True, "parallel" : False, "hitting_wall": False }


# we use separate locks to avoid nesting them inside one thread
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


# One of main movement function during water avoidance
# The robot moves forward in a left arc until it detects water again.
# It ends the thread and breaks water avoidance loop whenever:
# 1. the robot becomes parallel again(motor encoder)
# 2. the robot is withint 7.5 cm to the wall (US sensor)
# 3. the touch sensor is pressed by the wall (touch sensor)

def move_left_arc(dps, sleep_motor):
    print("left arc")
    distance_list = [255,255,255] # distance list defined for condition #2
    i = 0                         
    j = 3                         # iterating variable for distance list
    while i < sleep_motor:

        # for every iteration, measure the distance to the wall and append it to distance list
        distance = wall_us.get_value()
        distance_list.append(distance)
        mean_distance = (distance_list[j] + distance_list[j-1] + distance_list[j-2])/3  # get the mean of the last three measurments
        print(distance)
        print(mean_distance)

        # for every iteration, move forward in a left arc
        left_motor.set_power(-(dps-5))
        right_motor.set_power(-dps)

        # communication FROM other threads
        with flags_lock2:
            # if left_continuous_color_sensor_collection() detects "blue", stop and end thread
            if flags_low["water"]:
                print(flags_low["water"])
                left_motor.set_power(0)
                right_motor.set_power(0)
                return None
            # if collect_data() indicates "parallel", stop and end thread
            if flags_low["parallel"]:
                print(flags_low["parallel"])
                left_motor.set_power(0)
                right_motor.set_power(0)
                return "parallel"
        
        # communication TO other threads
        # if the mean distance to the wall is less than 7.5, or the touch sensor is pressed, 
        # back up and end thread
        # The reason we are not using 'if or' is because it bugs with 'or' statements for some reason.
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

        i += 0.1    # iterate the while loop
        j += 1      # the next distance will be appended in the next index in distance list
        sleep(0.1)

    # when the while loop is broken, stop the robot
    left_motor.set_power(0)
    right_motor.set_power(0)
    



# One of main movement function during water avoidance
# The robot turns right until it detects grass again.
# has two modes: "water avoidane" and "navigation(normal)". But maybe we won't need them?
# It ends the thread and breaks water avoidance loop whenever:
# 1. the robot becomes parallel again(motor encoder)
# 2. the robot is withint 7.5 cm to the wall (US sensor)
# 3. the touch sensor is pressed by the wall (touch sensor)

def turn_right(dps, sleep_motor):
    
    distance_list = [255,255,255]   # distance list defined
    print("turn_right")

    # "water_avoid_mode" activated
    with flags_lock1:
        if flags_high["water_avoid_mode"]:
            print("water_avoid_mode")
            i = 0
            j = 3
            while i < sleep_motor:

                # measure distance from the wall every iteration
                distance = wall_us.get_value()
                distance_list.append(distance)
                mean_distance = (distance_list[j] + distance_list[j-1] + distance_list[j-2])/3
                print(distance)
                print(mean_distance)

                # turn right every iteration
                left_motor.set_power(-dps)
                right_motor.set_power(dps)

                # communication FROM other threads
                with flags_lock2:
                    # if left_green_continuous_color_sensor_collection() detects "green", stop and end thread
                    if flags_low["grass"]:
                        print(flags_low["grass"])
                        left_motor.set_power(0)
                        right_motor.set_power(0)
                        return None
                    # if collect_data() indicates "parallel", stop and end thread
                    if flags_low["parallel"]:
                        print(flags_low["parallel"])
                        left_motor.set_power(0)
                        right_motor.set_power(0)
                        return None
                    
                # communication TO other threads
                # if the mean distance to the wall is less than 7.5, or the touch sensor is pressed, 
                # back up and end thread
                # The reason we are not using 'if or' is because it bugs with 'or' statements for some reason.
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
            
            # when the while loop breaks, stop the robot
            left_motor.set_power(0)
            right_motor.set_power(0)
        
        # when "navigation_mode", just turn for the given time
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


# This function is threaded simultaneously with move_left_arc() thread.
# It detects the color of the floor every 0.1 second
# It ends the thread when:
# 1. it detects blue => changes the flag of water and green and end thread
# 2. when the robot is parallel
# 3. when the robot is wihtin 7.5 cm to the wall or hits the wall

def left_continuous_color_sensor_collection():
    counter = 0

    #These variables hold the three values that will be averaged in order to calculate the "current color guess"
    first = (0, 0, 1)
    second = (0, 0, 1)
    third = (0, 0, 1)

    while counter < 600:
        counter += 1
        color_data = color_left.get_rgb() # take color sensor value every iteration

        # all the color stuff
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

            # communication TO other threads
            # when the sensor detects blue, it sets "water" flag to True and "grass" flag to False
            # => ends move_left_arc() thread and allows turn_right() thread to run
            if decision == "blue":
                with flags_lock2:
                    flags_low["water"] = True
                    flags_low["grass"] = False
                return decision
            
            # communication FROM other threads
            # when collect_data() or move_left_arc() sets "parallel" flag or "hitting_wall" flag to True, end thread
            with flags_lock2:
                if flags_low["parallel"] == True:
                    return None
                if flags_low["hitting_wall"] == True:
                    return None

        sleep(0.1)


# This function is threaded simultaneously with turn_right() thread.
# It detects the color of the floor every 0.1 second
# It ends the thread when:
# 1. it detects green => changes the flag of water and green and end thread
# 2. when the robot is parallel
# 3. when the robot is wihtin 7.5 cm to the wall or hits the wall

def left_green_continuous_color_sensor_collection():
    counter = 0
    
    #These variables hold the three values that will be averaged in order to calculate the "current color guess"
    first = (0, 0, 1)
    second = (0, 0, 1)
    third = (0, 0, 1)

    while counter < 600:
        counter += 1
        color_data = color_left.get_rgb()  # take color sensor value every iteration

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

            # communication TO other threads
            # when the sensor detects blue, it sets "water" flag to False and "grass" flag to True
            # => ends turn_right() thread and allows move_left_arc() thread to run
            if decision == "green":
                with flags_lock2:
                    flags_low["grass"] = True
                    flags_low["water"] = False
                return decision
            
            # communication FROM other threads
            # when collect_data() or move_left_arc() sets "parallel" flag or "hitting_wall" flag to True, end thread
            with flags_lock2:
                if flags_low["parallel"] == True:
                    return None
                if flags_low["hitting_wall"] == True:
                    return None

        sleep(0.1)


# This function collects the motor encoder data every 0.1 second.
# It will be called as a thread as soon as the robot detects water for the first time.
# It will stop all water avoidance threads whem the robot becomes parallel to the wall again  
        
def collect_data():

    # reset motor encoder values to zero
    BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))
    BP.offset_motor_encoder(BP.PORT_D, BP.get_motor_encoder(BP.PORT_D))
    
    # collect motor encoder value every 0.1 second
    while True:
        Encoder_left_motor = BP.get_motor_encoder(BP.PORT_C)
        Encoder_right_motor = BP.get_motor_encoder(BP.PORT_D)
        print("left_motor: " + str(Encoder_left_motor))
        print("right_motor: " + str(Encoder_right_motor))
        
        # communication FROM other threads
        # if the robot is within 7.5 cm to the wall or hits the wall, end thread
        with flags_lock2:
            if flags_low["hitting_wall"]:
                print("stop data")
                return None
        
        # communication TO other threads
        # if the left and right motor encoder values are equal again(means the robot is parallel),
        # change "parallel" flag to True and end thread
        # => stop move_left_arc(), turn_right(), and both colour threads

        if abs(Encoder_left_motor) >= 20 and abs(Encoder_right_motor) >= 20:
            if abs(Encoder_left_motor - Encoder_right_motor) <= 3:
                with flags_lock2:
                    flags_low["parallel"] = True
                    return None
        
        sleep(0.1)
    


    

def main_function():
    
    # measure wall_US values to set them as the initial wall follower distance
    avg_wall_distance = []

    # get six wall_US values
    for i in range(6):
        wall_distance = wall_us.get_value()
        print(wall_distance)
        avg_wall_distance.append(wall_distance)
        sleep(0.1)
    
    # take the average of the last three values
    avg = (avg_wall_distance[3] + avg_wall_distance[4] + avg_wall_distance[5])/3
    print(avg)

    print("hi")

    # start the wallfollower thread and water detection thread from wallfollowing.py file
    wallthread = threading.Thread(target = wallfollowing.wallfollowing_f, args = (100, avg))
    colorthread = threading.Thread(target = wallfollowing.left_continuous_color_sensor_collection, args = ())
    wallthread.start()
    colorthread.start()
    
    # wait until those two threads are finished
    wallthread.join()
    colorthread.join()

    # enable the water avoidance mode
    flags_high["water_avoid_mode"] = True
    
    # start the collect_data() thread as soon as wallfollowing threads are done
    datathread = threading.Thread(target = collect_data, args = ())
    datathread.start()

    # water avoidance loop
    # iterate the water avoidance functions 20 times maximum
    for i in range(20):
        
        # the robot is already detecting blue
        # turn_right() thread and left_green...() thread
        # => turn right until it detects grass
        arc_thread = threading.Thread(target = turn_right, args = (22,15))
        color_thread = threading.Thread(target = left_green_continuous_color_sensor_collection, args = ())
        arc_thread.start()
        color_thread.start()
        # wait until the threads are done
        arc_thread.join()
        color_thread.join()
        
        # now the robot is detecting green away from water
        # move_left_arc() thread and left_continuous...() thread
        # => move forward in a left arc until it detects water again
        arc_thread = threading.Thread(target = move_left_arc, args = (22,15))
        color_thread = threading.Thread(target = left_continuous_color_sensor_collection, args = ())
        arc_thread.start()
        color_thread.start()
        # wait until the threads are done
        arc_thread.join()
        color_thread.join()
        
     
        # the above threads all end when
        # - the robot is parallel to the wall again or
        # - the robot is within 7.5 cm to the wall or hits the wall
        # then just exit the water avoidance loop
        with flags_lock2:
            if flags_low["parallel"]:
                print("done!")
                break
                
            if flags_low["hitting_wall"]:
                print("don't wannt hit the wall!")
                break

    # different action depending on the robots state
    # if it's parallel to the wall => measure distance to the wall and wall follow at that distance
    # if it's too close to the wall => wall follow at 3 cm
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
            
            wallthread_1 = threading.Thread(target = wallfollowing.wallfollowing_f, args = (100, 3))
            wallthread_1.start()
            
        
        


    
    
    

main_function()

## Testing ##
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

