# grab a file named money.csv

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read the file
df = pd.read_csv('money.csv')




# I want to find out where I can save money
# So where is the money going to?

# We need to prepare the data for analysis
# Before we drop anything, let's categorize the data

# This is where the output from the last line appears for new categories

df['Category'] = 'Other'


categories = {
    'travel': ['FlixBus', 'Ampido', 'Deutsche Bahn', 'VRR', 'Rheinbahn', 'Interparking Cob Xenti'],
    'food': ['Aldi', 'Rewe', 'Lidl', 'Uber Eats', 'Trinkhalle Dinoya', 'Kaufland', 'Bistro Essart Gmbh & C'],
    'health': ['Center Apotheke E.', 'Fielmann', 'Evo Payments'],
    'debt': ['To Agentur Für Arbeit', 'To KfW Frankfurt', 'To Bundeskasse - Dienstort Halle (Darlehen)'],
    'communication': ['To Vodafone GmbH', 'To congstar - eine Marke der Telekom Deutschland GmbH'],
    'rent': ['To Eduard Koch'],
    'payment': ['Payment from Ulf Dellbrugge', 'Payment from Iq Digital Media Marketing Gmbh'],
    'fun': ['YouTube', 'Microsoft'],
    'exchange': ['Exchanged to EUR'],
    'unknown': ['SNCB'],
    'energy': ['To Tibber Deutschland GmbH'],
}

for category, keywords in categories.items():
    df.loc[df['Description'].isin(keywords), 'Category'] = category.capitalize()


print (df[df['Category'] == 'Other'].tail(10))

# Ask me for the last line if it fits a category, then save the category to a json file

while True:
    print('Enter the category for the following description:')
    print(df[df['Category'] == 'Other'].tail(1))
    category = input()
    if category == 'exit':
        break
    # add it to memory and later save it to file
    df.loc[df['Category'] == 'Other', 'Category'] = category.capitalize()

# save the categories to a file
df.to_csv('money_categorized.csv', index=False)

