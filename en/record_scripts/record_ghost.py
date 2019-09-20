#!/usr/bin/env python3

from ev3dev.auto import *
import csv
import time

btn = Button()
ir = InfraredSensor()
ir.mode = 'IR-SEEK'

header = ['time', 'heading', 'distance']
with open(r'./../csv_data/ghost_location.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)

timestamp_start = time.time()

Sound.speak('Alright, lets play hide and seek')

abortion_counter = 0
data = []

while not (btn.any() or abortion_counter > 4):
    timestamp = time.time() - timestamp_start
    heading = ir.value(0)
    distance = ir.value(1)
    print(heading)
    print(distance)
    if (heading == 0) and (distance == 100):
        abortion_counter += 1
    else:
        abortion_counter = 0

    data_point = [timestamp, heading, distance]
    data.append(data_point)


if abortion_counter > 4:
    for i in range(0,5):
        del data[-1]

with open('./../csv_data/ghost_location.csv', 'a') as file:
    writer = csv.writer(file)
    writer.writerows(data)

Sound.speak('I cant see my ghost friend anymore')
time.sleep(1)