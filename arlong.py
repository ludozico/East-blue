"""
This module contains code for processing KDrama data.
"""

import datetime
import pandas as pd

# Load the CSV data into a pandas DataFrame and convert 'Start_date' to datetime format
df = pd.read_csv('top100_kdrama.csv', parse_dates=['Start_date'], date_parser=lambda x: pd.to_datetime(x, errors='coerce', format='%m/%d/%Y'))

# Filter rows where 'Start_date' is more recent than 01/01/2018
df2 = df[df['Start_date'] > datetime.datetime(2018, 1, 1)]

# Get a statistical summary of the data
print(df2.describe())

print(df2.columns)

names = df2['Main Role'].str.split(', ', expand=True).stack()
name_counts = names.value_counts()

print(name_counts)

