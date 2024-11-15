import sys
# setting path
sys.path.append('../')

import os
from prompt import get_result
import pandas as pd

OUTPUT_PATH = '../data/results/'
LOCAL_DATE_TIME = '2024-11-13 10:55'

locations = pd.read_csv("../data/locations.csv", sep=";")

i = 0
for loc in locations.iloc:
    i += 1
    print(f"Processing location #{i} - {loc['Name']}")
    if (os.path.isfile(f"{OUTPUT_PATH}output_{loc['Name']}.json")):
        print('Location already processed - skip')
        continue
    with open(f"{OUTPUT_PATH}output_{loc['Name']}.json", "w", encoding='utf8') as outfile:
        print('Triggering LLM and writing to file')
        outfile.write(get_result(loc, LOCAL_DATE_TIME))