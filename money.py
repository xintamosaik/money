import pandas as pd
import json
import os

# Load the data
df = pd.read_csv('money.csv')
df['Category'] = 'Other'

# Define initial categories
categories = {
   
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
    # Save the merged data back to the JSON file and remove duplicates
    with open('new_categories.json', 'w') as json_file:
        existing_data = {category: list(set(descriptions)) for category, descriptions in existing_data.items()}
        # sort the dictionary
        existing_data = dict(sorted(existing_data.items()))
        # and the entries
        for key, value in existing_data.items():
            existing_data[key] = sorted(value)
        json.dump(existing_data, json_file, indent=4)

else:
    # If no JSON file exists, save new categories directly
    with open('new_categories.json', 'w') as json_file:
        json.dump(new_categories, json_file, indent=4)


# get all the food categories
food = df[df['Category'] == 'Food']

print(food)

# same for tax
tax = df[df['Category'] == 'Tax']

print(tax)

# sum tax
tax_sum = tax['Amount'].sum()
print(tax_sum)

food_sum = food['Amount'].sum()
print(food_sum)