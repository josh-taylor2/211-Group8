from utils.brick import wait_ready_sensors, EV3UltrasonicSensor, TouchSensor, EV3ColorSensor, Motor, BP
import math
import time
from time import sleep
import threading
# import block_detection


board_length = 122

BP.reset_all()


block_us = EV3UltrasonicSensor(4)
wall_us = EV3UltrasonicSensor(2)
touch_sensor = TouchSensor(3)
color_sensor = EV3ColorSensor(1)
left_motor = Motor('C')
right_motor = Motor('D')
color_motor = Motor('A')
gate = Motor('B')

wait_ready_sensors()

wall_counter = 0
block_counter = 0

global flags
flags = { "no_water" : True, "no_blocks": True}
global flags_lock
flags_lock = threading.Lock()

block_lock = threading.Lock()
collecting = False

def move_right_forward(dps, t):
    right_motor.set_power(-dps)
    time.sleep(t)
    right_motor.set_power(0)

def move_left_forward(dps, t):
    left_motor.set_power(-dps - 4)
    time.sleep(t)
    left_motor.set_power(0)

def move_forward(dps, t):
    rt = threading.Thread(target = move_right_forward, args = (dps, t))
    lt = threading.Thread(target = move_left_forward, args = (dps, t))
    rt.start()
    lt.start()

def is_it_poop(tuple):
    R, G, B = tuple[0], tuple[1], tuple[2]
    
    block = 0
    
    if B <= 6.5:
        if G <=17.5:
            return "floor"
        else:
            block = 1
    else:
        if G <= 4.5:
            if B <= 10.5:
                return "floor"
            else:
                    block = 1
        else:
            if G <= 5.5:
                if R <= 4.5:
                    return "floor"
                else:
                    block = 1
                    
    if (R/(R+G+B)) <= 0.438:
        return "person/seat"
    else:
        return "trash"

def stop_wheels():
    left_motor.set_dps(0)
    right_motor.set_dps(0)

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
        with block_lock:
            if not collecting:
                pass
            else:
                stop_wheels()
                break
        with flags_lock:
            #if flags["no_water"] and flags["no blocks"]:
            if flags["no_water"]:
                print("no blocks is true")
                pass
#             if flags["no_blocks"]:
#                 pass
            else:
                print("no blocks is false")
                break
#         with data_lock:
#             if not collecting:
#                 pass
#             else:
#                 break
        cur_time = time.time()
        actual_distance = wall_us.get_value()
        print("actual distance", actual_distance)
        
        if touch_sensor.is_pressed():
            print("Hit the wall")
            left_motor.set_power(18)
            right_motor.set_power(18)
            sleep(1)
            
            left_motor.set_power(18)
            right_motor.set_power(-18)
            sleep(1.3)
        
        #if the distance from the wall is within 2 cm of the desired distance, the robot will continue moving forward
        if abs(actual_distance - distance_from_wall) <= 1:
            left_motor.set_power(-18)
            right_motor.set_power(-18)
            sleep(0.1)
            
        # If the distance from the wall is too large, the robot will adjust itself to move closer to the wall
        if actual_distance - distance_from_wall > 0:
            if touch_sensor.is_pressed():
                print("Hit the wall")
                left_motor.set_power(18)
                right_motor.set_power(18)
                sleep(1)
                
                left_motor.set_power(18)
                right_motor.set_power(-18)
                sleep(1.3)
            else:
                left_motor.set_power(-18)
                right_motor.set_power(-12)
                sleep(0.5)
                
                left_motor.set_power(-12)
                right_motor.set_power(-18)
                sleep(0.05)
            
        # If the distance from the wall is too small, the robot will adjust itself to move away from the wall
        elif actual_distance - distance_from_wall < 0:
            left_motor.set_power(-12)
            right_motor.set_power(-18)
            sleep(0.1)         

            
    left_motor.set_power(0)
    right_motor.set_power(0)

    
def classify_color(r, g, b):
    #if (0.48<r<0.53 and 0.18<g<0.35 and 0.1<b<0.14)
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
#     BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C))
#     BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_D))
#     BrickPi.MotorEnable[PORT_C] = 1
#     BrickPi.MotorEnable[PORT_D] = 1
#     left_motor.reset_encoder()
#     right_motor.reset_encoder()
    

    counter = 0
    
    #These variables hold the three values that will be averaged in order to calculate the "current color guess"
    first = (0, 0, 1)
    second = (0, 0, 1)
    third = (0, 0, 1)

    while counter < 6000:
            
#         Encoder_left_motor = BP.get_motor_encoder(BP.PORT_C)
#         Encoder_right_motor = BP.get_motor_encoder(BP.PORT_D)
#     #     Encoder_right_motor = BrickPi.Encoder[PORT_D]
#         
#         print("left_motor: " + str(Encoder_left_motor))
#         print("right_motor: " + str(Encoder_right_motor))        
            
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
                    flags["no_water"] = False
                return decision
#             else: pass
        sleep(0.1)
    with flags_lock:
        flags["no_water"] = True 

def stop_moving(sleep_motor):
    left_motor.set_dps(0)
    right_motor.set_dps(0)
    sleep(sleep_motor)

def classify_color():
    # yellow 86, 75, 8
    #wait_ready_sensors(True)
    rgb = color_sensor.get_rgb()
    
    print(rgb)
    if (20 < rgb[0] < 30 and 20 < rgb[1] < 30 and 0 < rgb[2] < 10):
        return "trash" # yellow
    elif (10 < rgb[0] < 30 and 10 < rgb[1] < 20 and 18 < rgb[2] < 40):
        return "person/seat" # purple
    elif (65 < rgb[0] < 95 and 5 < rgb[1] < 35 and 0 < rgb[2] < 30):
        return "trash" # orange
    elif (0 < rgb[0] < 18 and 20 < rgb[1] < 52 and 0 < rgb[2] < 25):
        return "person/seat" # green
    return "fail"

def collect_trash():
    #time.sleep(0.02)
    #block_color = single_color_collection()
    
    #if block_color == 'yellow':
    print("gate open")
    gate.set_power(-20)
    time.sleep(1)
    left_motor.set_power(-22)
    right_motor.set_power(-20)
    time.sleep(1)
    gate.set_power(20)
    time.sleep(0.4)

    #BP.reset_all()
    return True

def avoid_block():
    print("moving to avoid block")
    
    left_motor.set_power(18)
    right_motor.set_power(18)
    sleep(1)
    
    left_motor.set_power(0)
    right_motor.set_power(0)
    sleep(0.2)
    
    left_motor.set_power(-18)
    right_motor.set_power(18)
    sleep(1.3)
    
    left_motor.set_power(-20)
    right_motor.set_power(-18)
    sleep(2)
    
    left_motor.set_power(-8)
    right_motor.set_power(-20)
    sleep(1.2)
    
    left_motor.set_power(-18)
    right_motor.set_power(-20)
    sleep(1)
    
    
    
def rotate_colorsensor_motor_by_degree(degree):
    color_motor.reset_encoder()
    target_angle = degree
    current_angle = 0
    while abs(current_angle) < abs(target_angle):
        step = 5 if target_angle > 0 else -5
        current_angle += step
        if abs(current_angle) > abs(target_angle):
            current_angle = target_angle
            
        color_motor.set_position(current_angle)
        time.sleep(0.2)
        
        print(f"Current Angle: {current_angle}")
        
    #BP.reset_all()
    return current_angle

def check_cubes_within_range():
    step = 5
    sleep_time = 0.4
    max_angle = 180
    
    color_motor.reset_encoder()
    current_angle = 0
    direction = 1
    
    while True:
#         detected_color = color_sensor.get_color() #replace with actual color detection algorithm
        #print(color_sensor.get_rgb())
        rgb = color_sensor.get_rgb()
        detected_color = is_it_poop(rgb)
        print("detected_color", detected_color)
        #detected_color = classify_color()
        if detected_color == "trash":
            print("Target color detected. Stopping motor.")
            

            return True, current_angle, detected_color
        
        elif detected_color == "person/seat":
            print("Person/Seat detected")

            return True, current_angle, detected_color
        
        current_angle += step * direction
        
        if current_angle > max_angle:
            direction = -1
            current_angle = max_angle
            
        elif current_angle < 0:
            current_angle = 0
            print("Motor return to forward limit.")
            
            #BP.reset_all()
            return False, current_angle, detected_color
        
        
        print(current_angle)
        color_motor.set_position(current_angle)
        time.sleep(sleep_time)

def ccollect_cubes_within_range():
    if_detected, cs_angle, detected_color  = check_cubes_within_range();
    if if_detected:
        if detected_color == "trash":
            print(f"reset color_sensor:{cs_angle}")
            rotate_colorsensor_motor_by_degree(-cs_angle)
            print("moving color sensor")
            if cs_angle > 55:
                collect_trash()
            else:
                right_motor.set_power(-20)
                time.sleep(0.5)
                collect_trash()
        else:
            rotate_colorsensor_motor_by_degree(-cs_angle)
            avoid_block()
            print(detected_color)
            print("done in check")
    else:
        print("no block detected")

    time.sleep(1)

def collect_cubes_within_range():
    global block_lock
    global collecting
    #time.sleep(3)
    while True:
        with block_lock:
            print(collecting)
            if collecting:
                if_detected, cs_angle, detected_color  = check_cubes_within_range();
                
                #block detected
                if if_detected:
                    if detected_color == "trash":
                        print(f"reset color_sensor:{cs_angle}")
                        rotate_colorsensor_motor_by_degree(-cs_angle)
                        print("moving color sensor")
                        if cs_angle > 55:
                            collect_trash()
                        else:
                            right_motor.set_power(-20)
                            time.sleep(0.5)
                            collect_trash()
                    else: # person/seat -> avoid block
                        rotate_colorsensor_motor_by_degree(-cs_angle)
                        avoid_block()
                        print(detected_color)
                        print("done in check")
                        with block_lock:
                            collecting = False
                else:
                    print("no block detected")
                    with block_lock:
                        collecting = False
                with block_lock:
                    collecting = False
                time.sleep(1)

def check_for_blocks():
    #collecting = False
    global block_lock
    global collecting
    while not collecting:
        #time.sleep(4)
        print("repeating while\n\n\n")
        time.sleep(1)
        distance = block_us.get_value()
        print(distance)
        if distance < 13:
            stop_wheels()
            with block_lock:
                 collecting = True
                 print("check for blocks", collecting)
            print("less than 13, analyzing")
            ccollect_cubes_within_range()
            with block_lock:
                collecting = False
            

#                 stop_wheels()
#                 collect_cubes_within_range()
#             
            #with data_lock:
            #with flags_lock:
             #   flags["no_blocks"] = False
            #collect_cubes_within_range()
            print("done in check\n\n\n\n\n\n")
            #reset_brick()
        else:
            with block_lock:
                print("check for blocks", collecting)
        time.sleep(0.1)
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
avg_wall_distance = []
for i in range(6):
    wall_distance = wall_us.get_value()
    print(wall_distance)
    avg_wall_distance.append(wall_distance)
    sleep(0.1)

avg = (avg_wall_distance[3] + avg_wall_distance[4] + avg_wall_distance[5])/3
print(avg)
    
t1 = threading.Thread(target=check_for_blocks)
#t2 = threading.Thread(target=collect_cubes_within_range)
t4 = threading.Thread(target = wallfollowing_f, args = (100, avg))
t3 = threading.Thread(target=move_forward, args=(15,10))

#
wait_ready_sensors(True)
#BP.reset_all()
#hi
t1.start()
#BP.reset_all()
#t2.start()
t3.start()


    

    
            




    





 



        
    




