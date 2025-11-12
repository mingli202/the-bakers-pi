from time import sleep
from project.utils.brick import (
    Motor,
)

def move_straight(motor1: Motor, motor2: Motor, power: int) :
    motor1.set_power(power)
    motor2.set_power(power)


def stop_move(motor1: Motor, motor2: Motor) :
    motor1.set_power(0)
    motor2.set_power(0)

def turn_right(motor1: Motor, motor2: Motor, power: int) :
    motor1.set_power(power)
    motor2.set_power(-power)

def turn_left(motor1: Motor, motor2: Motor, power: int) :
    motor1.set_power(-power)
    motor2.set_power(power)


