### Heres the code that controls everything

# from project.speaker_button import play_sound
# from project.collect_color_sensor_data import collect_color_sensor_data
# from project.collect_us_sensor_data import collect_continuous_us_data

from time import sleep
import math
from project.utils.brick import EV3ColorSensor, reset_brick, wait_ready_sensors, TouchSensor
from project.utils import sound


C5 = sound.Sound(duration=1.0, pitch="C5", volume=100)
C6 = sound.Sound(duration=1.0, pitch="C6", volume=100)
C7 = sound.Sound(duration=1.0, pitch="C7", volume=100)
C8 = sound.Sound(duration=1.0, pitch="C8", volume=100)

STOP_SENSOR = TouchSensor(1)
DRUMB_SENSOR = TouchSensor(2)
COLOR_SENSOR = EV3ColorSensor(3)


# reference unit vectors (pink is approx red+blue)
refs = {
    "RED": (255.0, 0.0, 0.0),
    "GREEN": (0.0, 255.0, 0.0),
    "BLUE": (0.0, 0.0, 255.0),
    "YELLOW": (255.0, 255.0, 0.0),
}

# normalize reference
normalized_refs = {}
for name, (rr, gg, bb) in refs.items():
    d = rr + gg + bb
    normalized_refs[name] = (rr / d, gg / d, bb / d)


def get_colour(sensor: EV3ColorSensor):
    r, g, b = sensor.get_rgb()
    # handle zero / very dark readings
    total = r + g + b
    if total < 10:  # sensor returned almost nothing; tune as needed
        return "UNKNOWN"

    # UNIT-VECTOR / COSINE-SIMILARITY
    denom = r + g + b
    if denom == 0:
        return "UNKNOWN"
    rn, gn, bn = r / denom, g / denom, b / denom

    # compute cosine similarity and pick best match
    best_name = "UNKNOWN"
    closest_dist = math.inf
    for name, (rr, gg, bb) in normalized_refs.items():
        dist = math.sqrt((rn - rr) ** 2 + (gn - gg) ** 2 + (bn - bb) ** 2)
        if dist < closest_dist:
            closest_dist = dist
            best_name = name

    if best_name == "YELLOW" and closest_dist > 0.35:
        return "UNKNOWN"
    return best_name
    # return "UNKNOWN"


# function that just loops and checks for inputs; exits when exception
# each iter.:
    # get touch sensor 1 (stop)
    # get colour
    # get touch sensor 2 (drum)

    # if touch sensor 1 (stop): exit
    # process colour => (RED, GREEN, BLUE, YELLOW)
    # switch colour, case 1-4 => sound(note)
    # if drum => rotate motor 180deg

wait_ready_sensors(True)
print("Done waiting.")

def bake_the_pi():
    
    try:
        i = 0
        while not STOP_SENSOR.is_pressed():
            sleep(0.01)

        print("starting instrument")
        sleep(1)


        while not STOP_SENSOR.is_pressed(): # exit when stop button is pressed
            if DRUMB_SENSOR.is_pressed():
                print("smash drumb")
                
            colour = get_colour(COLOR_SENSOR)

            if colour == "RED":
                C5.play()
                C5.wait_done()
            elif colour == "GREEN":
                C6.play()
                C6.wait_done()
            elif colour == "BLUE":
                C7.play()
                C7.wait_done()
            elif colour == "YELLOW":
                C8.play()
                C8.wait_done()
            else:
                print("no colour detected")
                sleep(0.01)

            print(f"iteration: {i}")
            i += 1
    except BaseException:
        pass
    finally:
        print("Done playing")
        reset_brick() # Turn off everything on the brick's hardware, and reset it
        exit()


if __name__ == "__main__":
    bake_the_pi()