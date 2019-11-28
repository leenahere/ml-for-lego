#!/usr/bin/env python3

import pandas as pd
import os

os.chdir('./../csv_data')

all_filenames = ['data_1.csv', 'data_2.csv', 'data_3.csv', 'data_4.csv', 'data_5.csv', 'data_6.csv', 'data_7.csv', 'data_8.csv', 'data_9.csv']

# combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])

# export to csv
combined_csv.to_csv( "./../csv_data/combined_csv.csv", index=False, encoding='utf-8-sig')
