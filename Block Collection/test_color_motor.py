from utils import sound
from utils.brick import TouchSensor, EV3ColorSensor, EV3UltrasonicSensor, wait_ready_sensors, reset_brick, BP, Motor
import time
from time import sleep

color_motor = Motor("C")

def test_sensor_placed_on_block(direction):
    
    color_motor.reset_encoder()
    curr_angle = 0
    while (abs(curr_angle) < 150):
        #color_motor.reset_encoder()
        #curr_angle = direction*(abs((curr_angle)+5))
        curr_angle = direction*(curr_angle*direction +5 )
        color_motor.set_position(curr_angle)
        time.sleep(0.3)
        print(curr_angle)
    BP.reset_all()
    return curr_angle


# roates the motor by a specified degree amount
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

rotate_colorsensor_motor_by_degree(-150)