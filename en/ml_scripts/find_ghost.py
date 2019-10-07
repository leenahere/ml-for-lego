#!/usr/bin/env python3

from ev3dev2.motor import MoveSteering, OUTPUT_B, OUTPUT_C
from ev3dev.ev3 import *
import math
from time import sleep
import requests
import glob
import os
import re

CM_PER_SECOND = 5 # determined by trial and error. cm that robot travels with speed set to 10
ENDPOINT_ADDRESS = '192.168.100.144'

steer_pair = MoveSteering(OUTPUT_B, OUTPUT_C)


def calc_coordinates(heading, dist):
    dist_to_cm_ratio = int(open("./../helper/measure.txt").readline().rstrip()) / 100
    print('ratio is ' + str(dist_to_cm_ratio))
    theta_for_calc = math.radians(heading)
    ghost_x = dist * math.tan(theta_for_calc)
    ghost_y = dist * dist_to_cm_ratio
    return ghost_x, ghost_y


def find_ghost():
    search_results = glob.glob('./models/*.sav')
    latest_file = max(search_results, key=os.path.getctime)
    pattern = re.compile('./models/ghost_regressor.*.sav')
    print(latest_file)
    print(pattern.match(latest_file))
    if pattern.match(latest_file):
        mode = "one"
    else:
        mode = "two"

    session_id = latest_file.split('regressor')[1].split('.sav')[0]
    timestamp = str(25.0)
    r = requests.get('http://' + ENDPOINT_ADDRESS + ':80/api/predict/ghost/' + timestamp + '/' + mode + '/' + session_id)
    y = r.json()
    print(y)
    ghost_est_x, ghost_est_y = calc_coordinates(y[0][0], y[1][0])

    seconds_y = ghost_est_y / CM_PER_SECOND
    seconds_x = abs(ghost_est_x / CM_PER_SECOND)

    steer_pair.on_for_seconds(steering=0, speed=10, seconds=seconds_y)
    sleep(0.5)
    if(ghost_est_x < 0):
        steer_pair.on_for_seconds(steering=-90, speed=10, seconds=2.1)
    else:
        steer_pair.on_for_seconds(steering=90, speed=10, seconds=2.1)
    steer_pair.on_for_seconds(steering=0, speed=10, seconds=seconds_x)


if __name__ == "__main__":
    find_ghost()
