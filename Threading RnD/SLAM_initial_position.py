from utils.brick import wait_ready_sensors, EV3UltrasonicSensor, EV3GyroSensor, Motor, BP
import math
from time import sleep
import SLAM
import thread_movement
import threading
BP.reset_all()
# Initialize sensors
wall_us = EV3UltrasonicSensor(3)
block_us = EV3UltrasonicSensor(1)
#gyro_sensor = EV3GyroSensor(4)
left_motor = Motor('C')
right_motor = Motor('D')


def get_pos():
    x_candidate = []
    y_candidate = []
    for i in range(38):
        wall_dist = SLAM.get_wall_US_distance()
        block_dist = SLAM.get_block_US_distance()
        print("wall: " + str(wall_dist))
        print("block: " + str(block_dist))
        SLAM.add_position_candidates(x_candidate, y_candidate, wall_dist)
        sleep(0.3)
        i += 1
    print(SLAM.get_self_position(x_candidate, y_candidate))
        
    
 
wait_ready_sensors()
while True:
    print("block: " + str(SLAM.get_block_US_distance()))
    print("wall: " + str(SLAM.get_wall_US_distance()))
    sleep(0.1)


#move_thread = threading.Thread(target = thread_movement.turn_right(20,7), args = ())
#value_thread = threading.Thread(target = get_pos(), args = ())

#move_thread.start()
#value_thread.start()







