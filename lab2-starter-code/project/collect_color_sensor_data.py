#!/usr/bin/env python3

"""
This test is used to collect data from the color sensor.
It must be run on the robot.
"""

# Add your imports here, if any
from time import sleep
from utils.brick import EV3ColorSensor, reset_brick, wait_ready_sensors, TouchSensor

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
        while True:
            if not TOUCH_SENSOR.is_pressed():
                continue
            print("Touch sensor pressed, collecting rgb data...")
            r, g, b = COLOR_SENSOR.get_rgb()
            if r is not None and g is not None and b is not None: # If None is given, then data collection failed that time
                print("Writting data to file...")
                print(f"{r}, {g}, {b}") # Print the data to the console
                output_file.write(f"{r}, {g}, {b}\n")
            while TOUCH_SENSOR.is_pressed():
                sleep(DELAY_SEC)
            sleep(DELAY_SEC)
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        pass
    finally:
        print("Done collecting US distance samples")
        output_file.close()
        reset_brick() # Turn off everything on the brick's hardware, and reset it
        exit()
    

if __name__ == "__main__":
    collect_color_sensor_data()
