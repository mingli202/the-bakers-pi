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

def filter_data(r, g, b):
    if r is not None and g is not None and b is not None:
        if r > 0 and g > 0 and b > 0:
            return True
    return False

def collect_color_sensor_data():
    print("Collect color sensor data.")

    output = []

    try:
        while True:
            if not TOUCH_SENSOR.is_pressed():
                continue
            print("Touch sensor pressed, collecting rgb data...")
            r, g, b = COLOR_SENSOR.get_rgb()
            if filter_data(r, g, b): # If None is given, then data collection failed that time
                print(r, g, b)
                output.append(f"{r}, {g}, {b}")
            while TOUCH_SENSOR.is_pressed():
                sleep(DELAY_SEC)
            sleep(DELAY_SEC)

    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        pass
    finally:
        print("Done collecting US distance samples")

        with open(COLOR_SENSOR_DATA_FILE, "w") as file:
            file.write("\n".join(output))

        reset_brick() # Turn off everything on the brick's hardware, and reset it
        exit()
    

if __name__ == "__main__":
    collect_color_sensor_data()
