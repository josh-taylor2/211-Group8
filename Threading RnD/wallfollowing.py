from utils.brick import wait_ready_sensors, EV3UltrasonicSensor, TouchSensor, EV3ColorSensor, Motor, BP
import math
import time
from time import sleep
import threading

board_length = 122

BP.reset_all()


wall_us = EV3UltrasonicSensor(2)
touch_sensor = TouchSensor(3)
color_sensor = EV3ColorSensor(1)
left_motor = Motor('C')
right_motor = Motor('B')

wait_ready_sensors()

wall_counter = 0
block_counter = 0

flags = { "flag1" : True, "flag2": True}

flags_lock = threading.Lock()


def mean(first, second, third):
    return ((first + second + third) / 3)

# Keeping the robot at a given distance from the wall
def wallfollowing_f(run_time, distance_from_wall):
    # If the distance from the wall is too small, the robot will move away from the wall
    actual_distance = wall_us.get_value()
    print(actual_distance)
    init_time = time.time()
    cur_time = time.time()
    print(cur_time - init_time)
    while (actual_distance != None or wall_us.get_value() <= 80) and (cur_time - init_time) <= run_time:
        with flags_lock:
            if flags["flag1"]:
                pass
            else:
                break
        cur_time = time.time()
        actual_distance = wall_us.get_value()
        print(actual_distance)
        
        if touch_sensor.is_pressed():
            print("Hit the wall")
            left_motor.set_power(40)
            right_motor.set_power(40)
            sleep(0.5)
            
            left_motor.set_power(20)
            right_motor.set_power(-20)
            sleep(1.3)
        
        #if the distance from the wall is within 2 cm of the desired distance, the robot will continue moving forward
        if abs(actual_distance - distance_from_wall) <= 1:
            left_motor.set_power(-40)
            right_motor.set_power(-40)
            sleep(0.1)
            
        # If the distance from the wall is too large, the robot will adjust itself to move closer to the wall
        if actual_distance - distance_from_wall > 0:
            if touch_sensor.is_pressed():
                print("Hit the wall")
                left_motor.set_power(20)
                right_motor.set_power(20)
                sleep(0.5)
                
                left_motor.set_power(20)
                right_motor.set_power(-20)
                sleep(1.3)
            else:
                left_motor.set_power(-40)
                right_motor.set_power(-35)
                sleep(0.5)
                
                left_motor.set_power(-35)
                right_motor.set_power(-40)
                sleep(0.05)
            
        # If the distance from the wall is too small, the robot will adjust itself to move away from the wall
        elif actual_distance - distance_from_wall < 0:
            left_motor.set_power(-35)
            right_motor.set_power(-40)
            sleep(0.1)
            

            
            
    
    left_motor.set_power(0)
    right_motor.set_power(0)

    
    
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

def normalize(r, g, b):
    print(r, g, b)
    r_norm = r/(r+g+b)
    g_norm = g/(r+g+b)
    b_norm = b/(r+g+b)

    return(r_norm, g_norm, b_norm)

def single_color_collection():

    color_data = color_sensor.get_rgb()
    print(color_data)
    if color_data is not None:
        normalized_tuple = normalize(color_data[0], color_data[1], color_data[2])
        decision = classify_color(normalized_tuple[0], normalized_tuple[1], normalized_tuple[2])
        print(normalized_tuple)
        print(decision)

#     reset_brick()
    return decision

def left_continuous_color_sensor_collection():
    counter = 0
    
    #These variables hold the three values that will be averaged in order to calculate the "current color guess"
    first = (0, 0, 1)
    second = (0, 0, 1)
    third = (0, 0, 1)

    while counter < 600:
        counter += 1
        color_data = color_sensor.get_rgb()
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
                with flags_lock:
                    flags["flag1"] = False
                return decision
#             else: pass
        sleep(0.1)

def stop_moving(sleep_motor):
    left_motor.set_dps(0)
    right_motor.set_dps(0)
    sleep(sleep_motor)
    
# Testing
# wallthread = threading.Thread(target = wallfollowing_f, args = (100,2.5))
# colorthread = threading.Thread(target = left_continuous_color_sensor_collection, args = ())
# 
# colorthread.start()
# wallthread.start()


# wallfollowing_f(100,2.5)
# i = 1
# while True:
#     if touch_sensor.is_pressed():
#         print("Touch" + i )
#         





    

    
            




    





 



        
    



