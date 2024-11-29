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

def classify_block(r, g, b):
    if 0.459 < r < 0.550 and 0.332 < g < 0.4386 and 0.040 < b < 0.1747:
        return "yellow"
    return "not yellow"

def classify_floor(r, g, b):
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

def convert_to_rgb():
    color = color_sensor.get_rgb()
    return color[0], color[1], color[2]
    
def normalize(r, g, b):
    print(r, g, b)
    r_norm = r/(r+g+b)
    g_norm = g/(r+g+b)
    b_norm = b/(r+g+b)

    return(r_norm, g_norm, b_norm)

def single_color_collection(r, g, b):

    
    normalized_tuple = normalize(r, g, b)
    decision = classify_color(normalized_tuple[0], normalized_tuple[1], normalized_tuple[2])
    print(normalized_tuple)
    print(decision)

    reset_brick()
    return decision

def collect_trash():
    #time.sleep(0.02)
    r, g, b = convert_to_rgb()
    block_color = single_color_collection(r, g, b)
    
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

def avoid_block():
    while True:
        
        left_wheel.set_power(-25)
        right_weel.set_power(-15)
        sleep(1.3)
        
        left_wheel.set_power(-22)
        right_wheel.set_power(-20)
        sleep(1.3)
        
        left_wheel.set_power(-15)
        right_wheel.set_power(-25)
        sleep(1.3)
        
        r, g, b = convert_to_rgb()
        normalized = normalize(r, g, b)
        
        #Verify if there's another block in the robot's path or if it's water with appropriate function
        #If block
        if classify_block(normalized[0], normalized[1], normalized[2]) == "not yellow":
            avoid_block()
            
        else:
            collect_trash()
            
        if classify_floor(r, g, b) == "blue":
            #This will eventually call the function that we'll have to avoid water
            print("water")
            
            
            
        else:
            break
        
        
    
    