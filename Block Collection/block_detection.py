from utils import sound
from utils.brick import TouchSensor, EV3ColorSensor, EV3UltrasonicSensor, wait_ready_sensors, reset_brick, BP, Motor
import time
from time import sleep
import threading


block_us = EV3UltrasonicSensor(4)
wall_us = EV3UltrasonicSensor(2)
touch_sensor = TouchSensor(3)
color_sensor = EV3ColorSensor(1)
left_wheel = Motor("C")
right_wheel = Motor("B")
color_motor = Motor("A")
gate = Motor("D")


data_lock = threading.Lock()
condition = threading.Condition()

collecting = False
done_collecting = 1


wait_ready_sensors(True)


def stop_wheels():
    left_wheel.set_dps(0)
    right_wheel.set_dps(0)

def move_right_forward(dps, t):
    right_wheel.set_power(-dps)
    time.sleep(t)
    right_wheel.set_power(0)

def move_left_forward(dps, t):
    left_wheel.set_power(-dps)
    time.sleep(t)
    left_wheel.set_power(0)

def move_forward(dps, t):
    rt = threading.Thread(target = move_right_forward, args = (dps, t))
    lt = threading.Thread(target = move_left_forward, args = (dps, t))
    lt.start()
    rt.start()

def classify_color():
    # yellow 86, 75, 8
    #wait_ready_sensors(True)
    rgb = color_sensor.get_rgb()
    
    print(rgb)
    if (55 < rgb[0] < 90 and 50 < rgb[1] < 90 and 0 < rgb[2] < 15):
        return "trash" # yellow
    elif (10 < rgb[0] < 30 and 10 < rgb[1] < 20 and 14 < rgb[2] < 40):
        return "person/seat" # purple
    elif (65 < rgb[0] < 95 and 5 < rgb[1] < 35 and 0 < rgb[2] < 30):
        return "trash" # orange
    elif (0 < rgb[0] < 15 and 20 < rgb[1] < 52 and 0 < rgb[2] < 25):
        return "person/seat" # green
    return "fail"
    
    #if 0.459 < r < 0.550 and 0.332 < g < 0.4386 and 0.040 < b < 0.1747:
        #return "yellow"
    #if  orange rgb's:
        #return "orange"
    #if purple rgb's:
    #    return purple
    # if green rgb's
    #    return green
    #return "not yellow"

def color_is_trash():

    color_data = color_sensor.get_rgb()
    if color_data is not None:
#         normalized_tuple = normalize(color_data[0], color_data[1], color_data[2])
#         decision = classify_color(normalized_tuple[0], normalized_tuple[1], normalized_tuple[2])
        decision = classify_color(color_data[0], color_data[1], color_data[2])
    if decision == "yellow" or decision == "orange":
        print("decision")
        reset_brick()
        return True
    print("not detected")
    reset_brick()
    return False




def sensor_placed_on_block(direction):
    curr_angle = 0
    while (classify_color != "yellow" or "orange" or "green" or "purple") and (curr_angle < 90):
        curr_angle = direction*abs((curr_angle)+5)
        color_motor.set_position(curr_angle)
    return curr_angle 

def avoid_block():
    move_backwards(20,1)
    turn_left()
    move_forwards(20,1)
    turn_right()
    move_forwards(20,5)
    turn_right()
    move_forwards(20,1)
    turn_left()

def block_in_range():
    if block_us.get_value() < 12: # 12 is the range we wanna detect
        stop_wheels()
        angle = sensor_placed_on_block(1)

        if angle < 20: # change value: block is to the left of the gate
            if color_is_trash():
                turn_left(20,2) # change this and use angle to know how much to turn or just turn the gate is wide
                collect_trash()
                move_backwards(20,1)
        
        if angle > 20: # change value: block is in front of the gate
            if color_is_trash():
                collect_trash()
            else:
                avoid_block()
                


def collect_trash():
    #time.sleep(0.02)
    #block_color = single_color_collection()
    
    print("hi")
    #if block_color == 'yellow':
    print("gate open")
    gate.set_power(-20)
    time.sleep(1)
    left_wheel.set_power(-22)
    right_wheel.set_power(-20)
    time.sleep(1)
    gate.set_power(20)
    time.sleep(0.4)

    BP.reset_all()
    return True
    #return False

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
        
    BP.reset_all()
    return current_angle

def check_cubes_within_range():
    step = 5
    sleep_time = 0.4
    max_angle = 150
    
    color_motor.reset_encoder()
    current_angle = 0
    direction = 1
    
    while True:
#         detected_color = color_sensor.get_color() #replace with actual color detection algorithm
        #print(color_sensor.get_rgb())
        detected_color = classify_color()
        if detected_color == "trash":
            print("Target color detected. Stopping motor.")
            
            BP.reset_all()
            return True, current_angle, detected_color
        
        elif detected_color == "person/seat":
            print("Person/Seat detected")
            BP.reset_all()
            return True, current_angle, detected_color
        
        current_angle += step * direction
        
        if current_angle > max_angle:
            direction = -1
            current_angle = max_angle
            
        elif current_angle < 0:
            current_angle = 0
            print("Motor return to forward limit.")
            
            BP.reset_all()
            return False, current_angle, detected_color
        
        
        print(current_angle)
        color_motor.set_position(current_angle)
        time.sleep(sleep_time)
        
def collect_cubes_within_range():
    global collecting
    #time.sleep(3)
    while True:
        with data_lock:
            # print(collecting)
            if collecting:
                if_detected, cs_angle, detected_color  = check_cubes_within_range();
                
                #block detected
                if if_detected:
                    if detected_color == "trash":
                        print(f"reset color_sensor:{cs_angle}")
                        rotate_colorsensor_motor_by_degree(-cs_angle)
                        print("collecting")
                        if cs_angle > 55:
                            collect_trash()
                        else:
                            right_wheel.set_power(-20)
                            time.sleep(0.5)
                            collect_trash()
                    else:
                        rotate_colorsensor_motor_by_degree(-cs_angle)
                        print(detected_color)
                        print("done in check")
                else:
                    print("no block detected")
                with data_lock:
                    collecting = False
                time.sleep(1)
        
def check_for_blocks():
    #collecting = False
    global collecting
    while not collecting:
        #time.sleep(4)
        print("repeating while\n\n\n")
        time.sleep(2)
        distance = block_us.get_value()
        #wait_ready_sensors(True)
        #block_us = EV3UltrasonicSensor(2)
        print(distance)
        if distance < 13:
            stop_wheels()
            print("less than 13, analyzing")
            with data_lock:
                collecting = True
                print("check for blocks", collecting)

            #collect_cubes_within_range()
            print("done in check\n\n\n\n\n\n")
            #reset_brick()
        else:
            with data_lock:
                print("check for blocks", collecting)
        time.sleep(0.1)
        
            
            
            
        
            
                
# sensor_placed_on_block(1)
# color_is_trash()
#collect_cubes_within_range()
# check_for_blocks()
#print(classify_color())
# while True: 
#         color_rgb = color_sensor.get_rgb()
#         time.sleep(0.2)
#         print(color_rgb)
# for i in range(10):
#     if (block_us.get_value())<12:
#         print(block_us.get_value())
#         BP.reset_all()
#     time.sleep(1)
#     
# def set_collecting():
#     global collecting
#     for i in range(600):
#         print("hey")
#         time.sleep(0.5)
#         if i > 5:
#             with data_lock:
#                 collecting = 5000
#                 print("set_collecting i:", i, "set_collecting done_collecting:", done_collecting)
#         else:
#             print("set_collecting i:", i, "set_collecting collecting", done_collecting)
# #             with condition:
# #                 collecting = 5000
# #                 condition.notify()
# def set_done_collecting():
#     for i in range(600):
#         print("hi")
#         time.sleep(0.5)
#         if i > 5:
#             with data_lock:
#                 #done_collecting = 5
#                 #condition.wait()
#                 print("done_set_collecting i:", i, "done_set_collecting collecting", collecting)
#         else:
#             print("done_set_collecting i:", i, "done_set_collecting collecting", collecting)            
# 
# t1 = threading.Thread(target=set_collecting)
# t2 = threading.Thread(target=set_done_collecting)
#         
# t1.start()
# t2.start()



t1 = threading.Thread(target=check_for_blocks)
t2 = threading.Thread(target=collect_cubes_within_range)
t3 = threading.Thread(target=move_forward, args=(18,10))
#
wait_ready_sensors(True)
#BP.reset_all()

t1.start()
t2.start()
t3.start()
