from classes.conditions import Conditions
from classes.tideCurrent import TideCurrent
from classes.coordinates import Coordinates
import pandas as pd

# Read the csv file
df = pd.read_csv('data/route.csv')

def getConditionsArray():
    conditionsArray = []
    for _, row in df.iterrows():
        conditions = Conditions(row['Speed Over Ground'], row['Course'],
                                row['Heel Angle'], row['Wind Speed'], 
                                row['Wind Direction'], 
                                TideCurrent(row['Tide Current Speed'], row['Tide Current Direction']),
                                Coordinates(row['Coordinates'].split(',')[0], row['Coordinates'].split(',')[1]))
        conditionsArray.append(conditions)
    return conditionsArray