import threading
from utils.brick import wait_ready_sensors, TouchSensor, EV3UltrasonicSensor, BP, Motor
from time import sleep

BP.reset_all()

DPS = 0
SLEEP_MOTOR = 3
SLEEP_US = 0.3

block_ultrasonic = EV3UltrasonicSensor(1)
#wall_ultrasonic = EV3Ultrasonic Sensor(2)
left_motor = Motor("C")
right_motor = Motor("A")
wait_ready_sensors()

def move_forward(dps, sleep_motor):
    left_motor.set_dps(dps)
    right_motor.set_dps(dps)
    time.sleep(sleep_motor)

#move_forward(1, 5)