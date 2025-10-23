from time import sleep
import math
from project.utils.brick import (
    EV3ColorSensor,
    Motor,
    reset_brick,
    wait_ready_sensors,
    TouchSensor,
)
from project.utils import sound

# reference unit vectors (yellow is green + red)
refs = {
    "RED": (255.0, 0.0, 0.0),
    "GREEN": (0.0, 255.0, 0.0),
    "BLUE": (0.0, 0.0, 255.0),
    "YELLOW": (255.0, 255.0, 0.0),
}

# normalize reference colors to unit vectors
normalized_refs: dict[str, tuple[float, float, float]] = {}
for name, (rr, gg, bb) in refs.items():
    d = rr + gg + bb
    normalized_refs[name] = (rr / d, gg / d, bb / d)


def get_colour(sensor: EV3ColorSensor):
    """
    Detect the color currently seen by the EV3 color sensor.

    The function reads raw RGB values from the sensor, normalizes them,
    and compares them against reference unit vectors using Euclidean distance.
    It returns the name of the closest matching color if within a threshold.

    Args:
        sensor (EV3ColorSensor): The EV3 color sensor instance.

    Returns:
        str: The detected color name ("RED", "GREEN", "BLUE", "YELLOW", or "UNKNOWN").
    """
    r, g, b = sensor.get_rgb()
    # handle zero / very dark readings
    if r is None or g is None or b is None:
        return

    # normalize RGB values to unit vectors
    denom = r + g + b
    if denom <= 10:
        return "UNKNOWN"
    rn, gn, bn = r / denom, g / denom, b / denom

    # Find the closest reference color by Euclidean distance
    best_name = "UNKNOWN"
    closest_dist = math.inf
    for name, (rr, gg, bb) in normalized_refs.items():
        dist = math.sqrt((rn - rr) ** 2 + (gn - gg) ** 2 + (bn - bb) ** 2)
        if dist < closest_dist:
            closest_dist = dist
            best_name = name
    
    # threshold to avoid misclassifying ambiguous readings and noise
    if best_name == "YELLOW" and not (0.22 < dist < 0.35):
        return "UNKNOWN"
    elif best_name == "RED" and closest_dist > 0.2:
        return "UNKNOWN"
    elif best_name == "GREEN" and not (0.3 < closest_dist < 0.45):
        return "UNKNOWN"
    elif best_name == "BLUE" and not (0.45 < closest_dist < 0.6):
        return "UNKNOWN"

    if r + g + b < 69:
        return "UNKNOWN"

    return best_name


# function that just loops and checks for inputs; exits when exception
# each iter.:
# get touch sensor 1 (stop)
# get colour
# get touch sensor 2 (drum)

# if touch sensor 1 (stop): exit
# process colour => (RED, GREEN, BLUE, YELLOW)
# switch colour, case 1-4 => sound(note)
# if drum => rotate motor 180deg


def main():
    """
    Main control loop for the color-drum instrument.

    The program waits for the user to press the "start" touch sensor,
    then continuously checks:
      - The color sensor to determine which note to play.
      - A drum touch sensor to toggle motor rotation (simulating drumming).
      - A stop touch sensor to exit the program.

    Each detected color corresponds to a specific musical note played
    through the EV3 sound module.

    Pressing the "stop" sensor ends the program gracefully.
    """
    # Initialize note sounds and hardware components
    volume = 100
    C5 = sound.Sound(duration=1, pitch="C5", volume=volume)
    C6 = sound.Sound(duration=1, pitch="E5", volume=volume)
    C7 = sound.Sound(duration=1, pitch="G5", volume=volume)
    C8 = sound.Sound(duration=1, pitch="C6", volume=volume)

    STOP_SENSOR = TouchSensor(1)
    DRUMB_SENSOR = TouchSensor(2)
    COLOR_SENSOR = EV3ColorSensor(3)
    MOTOR = Motor("A")

    wait_ready_sensors(True)
    print("Done waiting.")

    try:
        # Wait for user to press STOP_SENSOR to begin operation
        while not STOP_SENSOR.is_pressed():
            sleep(0.01)

        print("starting instrument")
        sleep(1)

        colour = "UNKNOWN"
        has_started = False

        # Main loop: runs until stop sensor is pressed again
        while not STOP_SENSOR.is_pressed():
            # Toggle motor rotation on drum touch
            if DRUMB_SENSOR.is_pressed():
                if has_started:
                    MOTOR.set_power(0)
                    has_started = False
                else:
                    MOTOR.set_power(-50)
                    has_started = True
                sleep(0.5)

            # Detect color and play corresponding note
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
                sleep(0.01)

    except BaseException:
        pass
    finally:
        print("Done playing")
        reset_brick()  # Turn off everything on the brick's hardware, and reset it
        exit()


if __name__ == "__main__":
    main()
