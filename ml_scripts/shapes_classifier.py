#!/usr/bin/env python3

# Import the EV3-robot library
from ev3dev.auto import *
import requests
import glob
import os

# endpoint address of manthano server
ENDPOINT_ADDRESS = '192.168.100.144'

# Connect motors
left_motor = LargeMotor(OUTPUT_B)
assert left_motor.connected
right_motor = LargeMotor(OUTPUT_C)
assert right_motor.connected

# Connect touch sensor and color sensors
ts = TouchSensor()
assert ts.connected
col_left = ColorSensor('in1')
assert col_left.connected
col_mid = ColorSensor('in2')
assert col_mid.connected
col_right = ColorSensor('in4')
assert col_right.connected

# Change color sensor mode
col_left.mode = 'COL-REFLECT'
col_mid.mode = 'COL-REFLECT'
col_right.mode = 'COL-REFLECT'

left_sensor_list = []
mid_sensor_list = []
right_sensor_list = []
left_motor_list = []
right_motor_list = []


def run():
    left = []
    middle = []
    right = []

    Sound.speak("Hallo")

    while not ts.value():
        # Add sensor values to respective list
        left.append(col_left.value())
        middle.append(col_mid.value())
        right.append(col_right.value())

        # As long as the color sensor in the middle is on the black line, the robot should drive straight
        if middle[-1] < 10:
            right_motor.run_forever(speed_sp=90)
            left_motor.run_forever(speed_sp=90)

        # Once all three sensors only see white surface, iterate through the right and left sensor list
        if left[-1] > 40 and middle[-1] > 40 and right[-1] > 40:
            found = False
            iterator = -2
            while not found:
                # Depending on the sensor that last saw the black line, turn right or left
                if left[iterator] < 10:
                    right_motor.run_forever(speed_sp=100)
                    left_motor.run_forever(speed_sp=-100)
                    found = True
                if right[iterator] < 10:
                    right_motor.run_forever(speed_sp=-100)
                    left_motor.run_forever(speed_sp=100)
                    found = True
                iterator -= 1
                # Make sure that list index isn't out of range
                if abs(iterator) > len(left) or abs(iterator) > len(right):
                    break

        left_sensor_list.append(col_left.value())
        mid_sensor_list.append(col_mid.value())
        right_sensor_list.append(col_right.value())
        left_motor_list.append(left_motor.speed)
        right_motor_list.append(right_motor.speed)

    left_motor.stop()
    right_motor.stop()

    # Why divide by 1000 instead of average? Length of recording should be represented in data. Therefore, average is insufficient
    lefty = sum(left_sensor_list) / 1000
    midy = sum(mid_sensor_list) / 1000
    righty = sum(right_sensor_list) / 1000
    leftm = sum(left_motor_list) / 1000
    rightm = sum(right_motor_list) / 1000

    X_new = str(lefty) + ',' + str(midy) + ',' + str(righty) + ',' + str(leftm) + ',' + str(rightm)

    print(str(lefty) + ',' + str(midy) + ',' + str(righty) + ',' + str(leftm) + ',' + str(rightm))

    search_results = glob.glob('./models/shapes_classifier*.sav')
    latest_file = max(search_results, key=os.path.getctime)
    session_id = latest_file.split('shapes_classifier')[1].split('.sav')[0]

    # Get Model Prediciton from backend
    r = requests.get('http://' + ENDPOINT_ADDRESS + ':8080/api/predict/shapes/' + X_new + '/' + session_id)
    y = r.json()

    string_speak = ''.join(str(e) for e in y)
    print(''.join(str(e) for e in y))
    Sound.speak(string_speak)


if __name__ == "__main__":
    run()
