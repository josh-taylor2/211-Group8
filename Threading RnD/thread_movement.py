import threading
# Add your imports here, if any
from utils.brick import BP, Motor, EV3ColorSensor, wait_ready_sensors, TouchSensor, reset_brick, EV3UltrasonicSensor
from time import sleep

DELAY = 0.1
cs_data = "floor_yellow_results.csv"

# complete this based on your hardware setup
#color = EV3ColorSensor(2)
#TOUCH_SENSOR = TouchSensor(1)



#wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.


BP.reset_all()

DPS = 0
SLEEP_MOTOR = 3
SLEEP_US = 0.3
DELAY = 0.1
cs_data = "test_results.csv"
 

block_ultrasonic = EV3UltrasonicSensor(1)
wall_ultrasonic = EV3UltrasonicSensor(3)
#wall_ultrasonic = EV3Ultrasonic Sensor(2)
left_motor = Motor("C")
right_motor = Motor("D")
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
    print(r, g, b)
    r_norm = r/(r+g+b)
    g_norm = g/(r+g+b)
    b_norm = b/(r+g+b)

    return(r_norm, g_norm, b_norm)





#this runs similarly to the color collection program, but instead of printing the RGB values
#That is collects, it prints what it thinks the color of the floor is
def continuous_color_sensor_collection():
    counter = 0
    
    #These variables hold the three values that will be averaged in order to calculate the "current color guess"
    first = (0, 0, 1)
    second = (0, 0, 1)
    third = (0, 0, 1)

    while counter < 600:
        counter += 1
        color_data = color.get_rgb()
        if color_data is not None:

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
        sleep(0.1)
    reset_brick()
    return decision
                

        
def main_function():
    

    #t3 = threading.Thread(target = get_distance_to_block, args = (0.3,))
    #t4 = threading.Thread(target = stop_moving, args = (2,))
    #t5 = threading.Thread(target = get_distance_to_wall, args = (0.3,))
    print("hi")
    continuous_color_sensor_collection()
    #move_forward(20, 6)
    
    #if continuous_color_sensor_collection() == "blue":
     #   t3.start()
      #  turn_right(15, 4)
    
    #move_forward(20, 4)
    #turn_right(-15, 4)

#     t3.start()
#     t5.start()
#     time.sleep(6)
#     t4.start()
    print("bye")
    
print("hello world")
#main_function()

#move_forward(-40,4)
    




