#!/usr/bin/env python3

"""
This test is used to collect data from the color sensor.
It must be run on the robot.
"""

# Add your imports here, if any
from time import sleep
from utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor

DELAY_SEC = 0.01  # seconds of delay between measurements
COLOR_SENSOR_DATA_FILE = "../data_analysis/color_sensor.csv"

# complete this based on your hardware setup
COLOR_SENSOR = EV3ColorSensor(1)
TOUCH_SENSOR = TouchSensor(2)

wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.


def collect_color_sensor_data():
    "Collect color sensor data."
    try:
        output_file = open(COLOR_SENSOR_DATA_FILE, "w")
        while not TOUCH_SENSOR.is_pressed():
            pass
        print("Touch sensor pressed")
        sleep(1)
        print("Starting to collect rgb color samples")
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        pass
    finally:
        print("Done collecting US distance samples")
    


if __name__ == "__main__":
    collect_color_sensor_data()
