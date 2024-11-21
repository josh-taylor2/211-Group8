from utils.brick import wait_ready_sensors, EV3UltrasonicSensor, EV3GyroSensor, Motor, BP
import math
from time import sleep
import threading

board_length = 122

BP.reset_all()

DPS = 0
SLEEP_MOTOR = 3
SLEEP_US = 0.3
DELAY = 0.1


# Initialize sensors
us_sensor = EV3UltrasonicSensor(1)
gyro_sensor = EV3GyroSensor(2)

left_motor = Motor("C")
right_motor = Motor("D")

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
def get_US_distance(us_sensor, gyro_sensor):
    if us_sensor.get_value() == None:
        z = 0
    else:  
        z = us_sensor.get_value()
    if gyro_sensor.get_both_measure() == None:
        g = [0, 0]
    else:
        g = gyro_sensor.get_both_measure()
    
    theta = g[0]

    # calculate US sensor value in x and y direction
    x = z * math.cos(math.radians(theta)) 
    y = z * math.sin(math.radians(theta))
        
    distance = [float(z), x, y, theta]
    
    return distance

# reduce the theta to 0~360
def reduce_angle(angle):
    reduced_angle = angle % 360
    return reduced_angle

# determine if the gyro sensor is facing +x,+y or -x,-y
# +x,+y -> 1, -x,-y -> -1
def gyro_direction(angle):
    direction = 1
    if abs(angle) >= 0 or abs(angle) <= 2 or abs(angle) >= 88 or abs(angle) <= 92:
        direction = 1
    if abs(angle) >= 178 or abs(angle) <= 182 or abs(angle) >= 268 or abs(angle) <= 272:
        direction = -1
    return direction

# Check if the distance received is entirely in x direction (angle error +- 2 deg)
def is_x_distance(distance):
    angle = reduce_angle(distance[3])
    if abs(angle) >= 0 or abs(angle) <= 2 or abs(angle) >= 178 or abs(angle) <= 182:
        x = distance[1]
        return True
    else:
        return False

# Check if the distance received is entirely in y direction (angle error +- 2 deg)
def is_y_distance(distance):
    angle = reduce_angle(distance[3])
    if abs(angle) >= 88 or abs(angle) <= 92 or abs(angle) >= 268 or abs(angle) <= 272:
        y = distance[1]
        return True
    else:
        return False

# Get the average of the values in the list
def get_average(list):
    sum = 0
    for i in range(list):
        sum = sum + list[i]
    return sum/len(list)

# Get 30 values of the US sensor and average the x and y value -> returns the position of the robot
def get_US_self_position(self_position, us_sensor, gyro_sensor):
    pos = []
    x_candidate = []
    y_candidate = []

    for i in 30:
        distance = get_US_distance(us_sensor, gyro_sensor)
        if is_x_distance:
            x_position = (board_length - (gyro_direction(distance[3])*distance[1])) % board_length
            x_candidate.append(x_position)
        if is_y_distance:
            y_position = (board_length - (gyro_direction(distance[3])*distance[2])) % board_length
            y_candidate.append(y_position)
        else:
            pass
        i += i
        time.sleep(0.3)
    
    
    x_fp = get_average(x_candidate)
    y_fp = get_average(y_candidate)

    pos = [x_fp, y_fp]

    return pos



left_motor.set_power(-40)
right_motor.set_power(-40)
sleep(4)
BP.reset_all()
get_US_distance(us_sensor, gyro_sensor)



    

    
            




    





 



        
    



