"""
Load Data from csv file on source/data.csv
"""
import pandas as pd 

frame = pd.read_csv("./source/data.csv")

DATA = dict()

for idx, data in frame.iterrows():
    DATA[str(idx)] = dict(dict(data.apply(str)))
    