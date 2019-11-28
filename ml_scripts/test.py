import requests
import sys
import glob
import os
import re

search_results = glob.glob('./models/digit_classifier*.sav')
if len(search_results) > 0:
    latest_file = max(search_results, key=os.path.getctime)
    print(search_results)
    print(latest_file)
    session_id = latest_file.split('digit_classifier')[1].split('.sav')[0]
    print(session_id)

search_results = glob.glob('./models/*.sav')
print(search_results)
latest_file = max(search_results, key=os.path.getctime)
pattern = re.compile('./models/ghost_regressor.*.sav')
print(latest_file)
print(pattern.match(latest_file))
if pattern.match(latest_file):
    mode = "one"
else:
    mode = "two"

session_id = latest_file.split('regressor')[1].split('.sav')[0]

print(mode)
print(session_id)