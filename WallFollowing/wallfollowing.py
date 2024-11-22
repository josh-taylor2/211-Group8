from utils.brick import wait_ready_sensors, EV3UltrasonicSensor, EV3GyroSensor, Motor, BP
import math
from time import sleep

board_length = 122
angle_error = 10

BP.reset_all()
wait_ready_sensors()

wall_us = EV3UltrasonicSensor(1)
block_us = EV3UltrasonicSensor(3)
left_motor = Motor('C')
right_motor = Motor('D')

# Keeping the robot at a given distance from the wall
def wallfollowing(distance_from_wall):
    # If the distance from the wall is too small, the robot will move away from the wall
    actual_distance = wall_us.get_value()
    print(actual_distance)
    while actual_distance != None or wall_us.get_value() <= 80:
        actual_distance = wall_us.get_value()
        print(actual_distance)
        #if the distance from the wall is within 2 cm of the desired distance, the robot will continue moving forward
        if abs(actual_distance - distance_from_wall) <= 2:
            left_motor.set_power(20)
            right_motor.set_power(20)
            sleep(2)
        # If the distance from the wall is too large, the robot will adjust itself to move closer to the wall
        elif actual_distance - distance_from_wall > 2:
            left_motor.set_power(25)
            right_motor.set_power(15)
            sleep(2)
        # If the distance from the wall is too small, the robot will adjust itself to move away from the wall
        elif actual_distance - distance_from_wall < -2:
            left_motor.set_power(15)
            right_motor.set_power(25)
            sleep(2)


# Testing
wallfollowing(10)






    

    
            




    





 



        
    



