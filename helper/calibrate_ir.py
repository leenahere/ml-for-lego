#!/usr/bin/env python3

from ev3dev2.motor import MoveSteering, OUTPUT_B, OUTPUT_C
from ev3dev.ev3 import *
import math
from time import sleep

btn = Button()
ir = InfraredSensor()
ir.mode = 'IR-SEEK'


def enter_distance():
    counter = 0
    print("Enter distance in cm, increase by 5 with up button and decrease by 5 with down button, confirm with center button")
    while not btn.enter:
        if btn.up:
            counter += 5
            print(counter)
            sleep(0.3)
        if btn.down:
            counter -= 5
            print(counter)
            sleep(0.3)
    return counter


def calibrate():
    abortion_counter = 0
    while not (btn.any() or abortion_counter > 4):
        heading = ir.value(0)
        distance = ir.value(1)
        print(distance)
        print(heading)
        if (heading == 0) and (distance == 100):
            abortion_counter += 1
        else:
            abortion_counter = 0

    Sound.speak('Stop, reached maximum distance')
    measured_distance = enter_distance()

    with open('measure.txt', 'w+') as f:
        f.write(str(measured_distance))


if __name__ == "__main__":
    calibrate()
