#!/usr/bin/env python3

# Import the EV3-robot library
from ev3dev.auto import *
import csv
from time import sleep

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

btn = Button()

left_sensor_list = []
mid_sensor_list = []
right_sensor_list = []
left_motor_list = []
right_motor_list = []


def average(list):
    return sum(list) / float(len(list))


def run():
    left = []
    middle = []
    right = []

    # Stops once touch sensor has been pressed
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


def which_number():
    counter = 0
    print("Druecke den Hoch-Button, um die Zahl einzugeben, die du aufnehmen willst. Bestaetige die Zahl mit dem mittleren Button.")
    while not btn.enter:
        if btn.up:
            counter += 1
            print(counter)
            sleep(0.3)
        if btn.down:
            counter -= 1
            print(counter)
            sleep(0.3)
    return counter


number = which_number()
print(str(number) + ' wird aufgenommen')
filename = r'./../csv_data/ziffern.csv'
f = open(filename, 'a')

run()

left_motor.stop()
right_motor.stop()

print("Wenn du die aufgenommenen Daten speichere willst, druecke den mittleren Button zum Bestaetigen. Um die Daten zu verwerfen, druecke den Unten-Button.")
while not btn.any():
    sleep(0.01)

if btn.enter:
    lefty = average(left_sensor_list)
    midy = average(mid_sensor_list)
    righty = average(right_sensor_list)
    leftm = average(left_motor_list)
    rightm = average(right_motor_list)
    data_point = [lefty, midy, righty, leftm, rightm, number]
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data_point)
    print("Saved data")
elif btn.down:
    print("Discarded")