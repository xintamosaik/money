import pandas as pd
import json
import os

# Load the data
df = pd.read_csv('money.csv')
df['Category'] = 'Other'

# Define initial categories
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

# Load additional categories from JSON if the file exists
if os.path.exists('new_categories.json'):
    with open('new_categories.json', 'r') as json_file:
        saved_categories = json.load(json_file)
        # Merge saved categories with initial categories
        for category, keywords in saved_categories.items():
            if category in categories:
                categories[category].extend(keywords)
            else:
                categories[category] = keywords

# Automatically categorize known keywords
for category, keywords in categories.items():
    df.loc[df['Description'].isin(keywords), 'Category'] = category.capitalize()

# Prepare to save new categories added during this session
new_categories = {}

# Manual categorization for remaining 'Other' rows
other_rows = df[df['Category'] == 'Other']

for idx, row in other_rows.iterrows():
    print(f"\nDescription: {row['Description']}")
    category = input("Enter the category (or type 'skip' to ignore, 'exit' to stop): ").strip().lower()
    
    if category == 'exit':
        break
    elif category != 'skip':
        # Update the DataFrame
        df.at[idx, 'Category'] = category.capitalize()
        
        # Update the new_categories dictionary
        if category not in new_categories:
            new_categories[category] = []
        new_categories[category].append(row['Description'])

# Save new categories to the JSON file, merging them with any existing saved categories
if os.path.exists('new_categories.json'):
    with open('new_categories.json', 'r') as json_file:
        existing_data = json.load(json_file)
        # Merge new categories into the existing data
        for category, descriptions in new_categories.items():
            if category in existing_data:
                existing_data[category].extend(descriptions)
            else:
                existing_data[category] = descriptions
    # Save the merged data back to the JSON file
    with open('new_categories.json', 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)
else:
    # If no JSON file exists, save new categories directly
    with open('new_categories.json', 'w') as json_file:
        json.dump(new_categories, json_file, indent=4)

