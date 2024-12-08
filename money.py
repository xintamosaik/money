import pandas as pd
import os


# Load the data
df = pd.read_csv('money_full_with_dates.csv')
# Extract year, month, and day from 'Started Date' column
df['Started Date'] = pd.to_datetime(df['Started Date'])
df['Year'] = df['Started Date'].dt.year
df['Month'] = df['Started Date'].dt.month
df['Day'] = df['Started Date'].dt.day
print(df)