from utils.brick import wait_ready_sensors, EV3UltrasonicSensor, EV3GyroSensor, Motor, BP
import math
from time import sleep
import threading

board_length = 122
angle_error = 10

BP.reset_all()

wall_us = EV3UltrasonicSensor(1)
block_us = EV3UltrasonicSensor(3)
gyro_sensor = EV3GyroSensor(4)
left_motor = Motor('C')
right_motor = Motor('D')



# I think we'll need this? Not used yet.
class self_position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class landmark:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y


# Return the list of US sensor value in x, y direction and gyro sensor value in degrees
def get_wall_US_distance():
    if wall_us.get_value() == None:
        z = 0
    else:  
        z = wall_us.get_value()
    if gyro_sensor.get_both_measure() == None:
        g = [0, 0]
    else:
        g = gyro_sensor.get_both_measure()
    
    theta = reduce_angle(g[0])

    # calculate US sensor value in x and y direction
    x = z * math.cos(math.radians(theta)) 
    y = z * math.sin(math.radians(theta))

        
    distance = [float(z), round(x, 2), round(y, 2), round(theta, 2)]
    
    return distance

def get_block_US_distance():
    if block_us.get_value() == None:
        z = 0
    else:  
        z = block_us.get_value()
    if gyro_sensor.get_both_measure() == None:
        g = [0, 0]
    else:
        g = gyro_sensor.get_both_measure()
    
    theta = reduce_angle(g[0])

    # calculate US sensor value in x and y direction
    x = z * math.cos(math.radians(theta)) 
    y = z * math.sin(math.radians(theta))

        
    distance = [float(z), round(x, 2), round(y, 2), round(theta, 2)]
    
    return distance

# reduce the theta to 0~360 // tested
def reduce_angle(angle):
    reduced_angle = abs(angle) % 360
    return reduced_angle

# determine if the gyro sensor is facing +x,+y or -x,-y   // tested
# +x,+y -> 1, -x,-y -> -1
def gyro_direction(angle):
    x_pos_range = range(0-angle_error, 0+angle_error+1)
    y_pos_range = range(90-angle_error, 90+angle_error+1)
    x_neg_range = range(180-angle_error, 180+angle_error+1)
    y_neg_range = range(270-angle_error, 270+angle_error+1)
    direction = 1
    if abs(angle) in x_pos_range or abs(angle) in y_pos_range:
        direction = -1
    if abs(angle) in x_neg_range or abs(angle) in y_neg_range:
        direction = 1
    print(direction)
    return direction


# Check if the distance received is entirely in x direction (angle error +- 2 deg) // tested
def is_x_distance(distance):
    x_pos_range = range(0-angle_error, 0+angle_error+1)
    x_neg_range = range(180-angle_error, 180+angle_error+1)
    angle = reduce_angle(distance[3])
    if abs(angle) in x_pos_range or abs(angle) in x_neg_range:
        x = distance[1]
        return True
    else:
        return False

# Check if the distance received is entirely in y direction (angle error +- 2 deg) // tested
def is_y_distance(distance):
    y_pos_range = range(90-angle_error, 90+angle_error+1)
    y_neg_range = range(270-angle_error, 270+angle_error+1)
    angle = reduce_angle(distance[3])
    if abs(angle) in y_pos_range or abs(angle) in y_neg_range:
        y = distance[1]
        return True
    else:
        return False

# Get the average of the values in the list // tested
def get_average(list):
    sum = 0
    for i in range(len(list)):
        sum = sum + list[i]
    avg = round(sum/len(list), 2)
    return avg




# Get 30 values of the US sensor and average the x and y value -> returns the position of the robot
def add_position_candidates(x_candidate: list, y_candidate: list, distance: list):
    if is_x_distance(distance) and distance[1] != 0:
        x_position = (board_length + (gyro_direction(distance[3])*((distance[0])+15))) % board_length
        x_candidate.append(x_position)
        print(x_position)
    if is_y_distance(distance) and distance[2] != 0:
        y_position = (board_length + (gyro_direction(distance[3])*((distance[0])+15))) % board_length
        y_candidate.append(y_position)
        print(y_position)
    else:
        pass
    

    return [x_candidate, y_candidate]


def get_self_position(x_candidate, y_candidate):
    x_fp = get_average(x_candidate)
    y_fp = get_average(y_candidate)

    pos = [x_fp, y_fp]
    
    return pos



# Testing

# gyro_sensor testing

#re_angle = reduce_angle(gyro_sensor.get_both_value()[0])
#print(re_angle)

#print(gyro_direction(270))
#print(round(reduce_angle(368.76394723), 2))
#print(is_y_distance())
#print(get_average([2, 4, 5, 3, 5, 6, 6]))

# Distance testing
#while True:
 #   print("wall: " + str(get_US_distance(wall_us,gyro_sensor)))
  #  print("block: " + str(get_US_distance(block_us,gyro_sensor)))
   # sleep(0.3)




    

    
            




    





 



        
    



