#!/usr/bin/env python3

from ev3dev2.motor import MoveSteering, OUTPUT_B, OUTPUT_C
from ev3dev.ev3 import *
import math
from time import sleep

DIST_TO_CM_RATIO = 0.42
CM_PER_SECOND = 5 # determined by trial and error. cm that robot travels with speed set to 10

steer_pair = MoveSteering(OUTPUT_B, OUTPUT_C)


def calc_coordinates(heading, dist):
    theta_for_calc = math.radians(heading)
    ghost_x = dist * math.tan(theta_for_calc)
    ghost_y = dist * DIST_TO_CM_RATIO
    return ghost_x, ghost_y

# TODO
#load model(s) here. Figure out how they come from web app
#predict heading and label by models (figure out if prediciton can be done on robot or in backend)

ghost_est_x, ghost_est_y = calc_coordinates(16.25, 172.7) # prediction should be input params for calc_coordinates

seconds_y = ghost_est_y / CM_PER_SECOND
seconds_x = abs(ghost_est_x / CM_PER_SECOND)

steer_pair.on_for_seconds(steering=0, speed=10, seconds=seconds_y)
sleep(0.5)
if(ghost_est_x < 0):
    steer_pair.on_for_seconds(steering=-90, speed=10, seconds=2.1)
else:
    steer_pair.on_for_seconds(steering=90, speed=10, seconds=2.1)
steer_pair.on_for_seconds(steering=0, speed=10, seconds=seconds_x)