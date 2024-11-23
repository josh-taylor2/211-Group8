#!/usr/bin/env python3

"""
Module to play sounds when the touch sensor is pressed.
This file must be run on the robot.
"""
 
from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors

SOUND1 = sound.Sound(duration=0.3, pitch="A5", volume=300)
SOUND2 = sound.Sound(duration=0.3, pitch="A3", volume=300)

TOUCH_SENSOR = TouchSensor(1)


wait_ready_sensors() # Note: Touch sensors actually have no initialization time


def play_sound():
    "Play a single note."
    print("song played")
    SOUND1.play()
    SOUND1.wait_done()


def play_sound_on_button_press():
    "In an infinite loop, play a single note when the touch sensor is pressed."
    try:
        while True:
            if TOUCH_SENSOR.is_pressed():
                play_sound()
            
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        exit()


if __name__=='__main__':

    # TODO Implement this function
    play_sound_on_button_press()
