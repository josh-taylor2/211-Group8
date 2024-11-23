from utils.brick import wait_ready_sensors, EV3UltrasonicSensor, Motor, BP
from time import sleep
import threading

BP.reset_all()

DPS = 0
SLEEP_MOTOR = 3
SLEEP_US = 0.3
DELAY = 0.1

ultra = EV3UltrasonicSensor(1)
ultra2 = EV3UltrasonicSensor(3)

left_motor = Motor("C")
right_motor = Motor("D")

wait_ready_sensors()

def get_US_value():
    while True:
        print("block:" + str(ultra.get_raw_value()))
        print("wall:" + str(ultra2.get_raw_value())) # => starts with centimeter reading
        sleep(0.3)

def move():
    left_motor.set_power(-40)
    right_motor.set_power(-40)


ut = threading.Thread(target = get_US_value, args = ())
mt = threading.Thread(target = move, args = ())
ut.start()
mt.start()
