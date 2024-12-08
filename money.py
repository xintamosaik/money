import pandas as pd
import os


# Load the data
df = pd.read_csv('money_full_with_dates.csv')
# Extract year, month, and day from 'Started Date' column
df['Started Date'] = pd.to_datetime(df['Started Date'])
df['Year'] = df['Started Date'].dt.year
df['Month'] = df['Started Date'].dt.month
df['Day'] = df['Started Date'].dt.day

this_year = df[df['Year'] == 2024]


last_month = this_year[this_year['Month'] == 11]
print(last_month)

food_last_month =  last_month[last_month['Category'] == 'Food']
sum_food_last_month = food_last_month['Amount'].sum()
print(f"Total amount for Food: {sum_food_last_month}")