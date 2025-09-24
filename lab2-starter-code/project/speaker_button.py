#!/usr/bin/env python3

"""
Module to play sounds when the touch sensor is pressed.
This file must be run on the robot.
"""
 
from time import sleep
from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors

DELAY_SEC = 0.01

SOUND = sound.Sound(duration=1, pitch="C5", volume=100)
TOUCH_SENSOR = TouchSensor(1)


wait_ready_sensors() # Note: Touch sensors actually have no initialization time


def play_sound():
    "Play a single note."
    SOUND.play()
    SOUND.wait_done()


def play_sound_on_button_press():
    "In an infinite loop, play a single note when the touch sensor is pressed."
    try:
        while True:
            if TOUCH_SENSOR.is_pressed():
                play_sound()
                while TOUCH_SENSOR.is_pressed():
                    sleep(DELAY_SEC)
            sleep(DELAY_SEC)
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        exit()
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        exit()


if __name__=='__main__':
    play_sound()

    # TODO Implement this function
    play_sound_on_button_press()
