from time import sleep
import math
from project.utils.brick import (
    EV3ColorSensor,
    reset_brick,
    wait_ready_sensors,
    TouchSensor,
)
from project.utils import sound
from threading import Thread

# reference unit vectors (pink is approx red+blue)
refs = {
    "RED": (255.0, 0.0, 0.0),
    "GREEN": (0.0, 255.0, 0.0),
    "BLUE": (0.0, 0.0, 255.0),
    "YELLOW": (255.0, 255.0, 0.0),
}

# normalize reference
normalized_refs: dict[str, tuple[float, float, float]] = {}
for name, (rr, gg, bb) in refs.items():
    d = rr + gg + bb
    normalized_refs[name] = (rr / d, gg / d, bb / d)


def get_colour(sensor: EV3ColorSensor):
    r, g, b = sensor.get_rgb()
    # handle zero / very dark readings
    if r is None or g is None or b is None:
        return

    # UNIT-VECTOR / COSINE-SIMILARITY
    denom = r + g + b
    if denom <= 10:
        return "UNKNOWN"
    rn, gn, bn = r / denom, g / denom, b / denom

    # compute cosine similarity and pick best match
    best_name = "UNKNOWN"
    closest_dist = math.inf
    dist = 0
    for name, (rr, gg, bb) in normalized_refs.items():
        dist = math.sqrt((rn - rr) ** 2 + (gn - gg) ** 2 + (bn - bb) ** 2)
        if dist < closest_dist:
            closest_dist = dist
            best_name = name

    if best_name == "YELLOW" and dist > 0.35:
        return "UNKNOWN"

    # threshold to avoid misclassifying ambiguous readings; tune 0.7-0.9
    # if closest_dist >= 0.8:
    print(f"closest_dist {closest_dist} {best_name} {r} {g} {b}")
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

volume = 80
C5 = sound.Sound(duration=1, pitch="C5", volume=volume)
C6 = sound.Sound(duration=1, pitch="E5", volume=volume)
C7 = sound.Sound(duration=1, pitch="G5", volume=volume)
C8 = sound.Sound(duration=1, pitch="C6", volume=volume)

STOP_SENSOR = TouchSensor(1)
DRUMB_SENSOR = TouchSensor(2)
COLOR_SENSOR = EV3ColorSensor(3)

wait_ready_sensors(True)
print("Done waiting.")

colour = "UNKNOWN"
has_started = False


def main():
    try:
        while not STOP_SENSOR.is_pressed():
            sleep(0.01)

        print("starting instrument")
        sleep(1)

        while not STOP_SENSOR.is_pressed():  # exit when stop button is pressed
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
                # print("no colour detected")
                sleep(0.01)

    except BaseException:
        pass
    finally:
        print("Done playing")
        reset_brick()  # Turn off everything on the brick's hardware, and reset it
        exit()


if __name__ == "__main__":
    main()
