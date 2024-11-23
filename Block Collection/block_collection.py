from utils.brick import wait_ready_sensors, EV3ColorSensor, Motor, BP, reset_brick
import math
import time
from time import sleep
BP.reset_all()

#R[0.460, 0.549] G[0.333, 0.4385] B[0.0701, 0.1746]

color_sensor = EV3ColorSensor(4)
gate = Motor('A')
left_wheel = Motor('C')
right_wheel = Motor('B')

def classify_color(r, g, b):
    if 0.459 < r < 0.550 and 0.332 < g < 0.4386 and 0.040 < b < 0.1747:
        return "yellow"
    return "not yellow"

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

    reset_brick()
    return decision

def move_left_wheel():
        left_wheel.set_power(20)
        time.sleep(3)

def move_right_wheel():
        right_wheel.set_power(20)
        time.sleep(3)

def collect_trash():
    #time.sleep(0.02)
    block_color = single_color_collection()
    
    print("hi")
    if block_color == 'yellow':
        print("gate open")
        gate.set_power(-20)
        time.sleep(1)
        left_wheel.set_power(-22)
        #time.sleep(3)
        right_wheel.set_power(-20)
        time.sleep(1)
        #gate.set_dps(0)
        #gate.set_dps(0)
        #left_wheel.set_dps(0)
        #right_wheel.set_dps(0)
        #time.sleep(2)
        #gate.set_dps(0)
        BP.reset_all()
        return True
    return False
#BP.reset_all()
wait_ready_sensors(True)
collect_trash()