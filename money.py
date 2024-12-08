import pandas as pd
import json
import os


# Load the data
df = pd.read_csv('money-full.csv')
df['Category'] = 'Other'

# Define initial categories
categories = {}

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


# clear data from categories "personal, unknown and tax"

# get the first date and the last date
first_date = df['Started Date'].min()
last_date = df['Started Date'].max()
print (f"\nFirst date: {first_date}")
print (f"Last date: {last_date}")
# how many years, months and days between the first and the last date
first_date = pd.to_datetime(first_date)
last_date = pd.to_datetime(last_date)
total_days = (last_date - first_date).days
years = total_days // 365
months = (total_days % 365) // 30
total_months = (years * 12) + months
days = (total_days % 365) % 30
print (f"\nBetween {first_date} and {last_date} there are {years} years, {months} months and {days} days")

total_rows_total = df.shape[0]
print (f"\nTotal rows: {total_rows_total}")
df = df[df['Category'] != 'Personal']

total_rows_after_personal = df.shape[0]
print (f"Total rows after removing 'Personal': {total_rows_after_personal}")
df = df[df['Category'] != 'Unknown']

total_rows_after_unknown = df.shape[0]
print (f"Total rows after removing 'Unknown': {total_rows_after_unknown}")

df = df[df['Category'] != 'Tax']
total_rows_after_tax = df.shape[0]
print (f"Total rows after removing 'Tax': {total_rows_after_tax}")
# income

income = df[df['Category'] == 'Payment']
total_rows_income = income.shape[0]
print (f"Total rows for 'Payment': {total_rows_income}")
income_sum = income['Amount'].sum()

print (f"\nTotal income: ${income_sum:.2f}")

# expenses
expenses = df[df['Category'] != 'Payment']
total_rows_expenses = expenses.shape[0]

print (f"Total rows for expenses: {total_rows_expenses}")
expenses_sum = expenses['Amount'].sum()

print (f"Total expenses: ${expenses_sum:.2f}")

# percentages of expenses
expenses_by_category = expenses.groupby('Category').sum()
# percentages
expenses_by_category['Percentage'] = expenses_by_category['Amount'] / expenses_sum * 100
expenses_by_category = expenses_by_category.sort_values('Amount', ascending=False)
# monthly
expenses_by_category['Monthly'] = expenses_by_category['Amount'] / total_months

print("\nExpenses by category:")
# print only the amounts and the percentages 
print(expenses_by_category[['Amount', 'Percentage', 'Monthly']])

# put the data in a new csv file
expenses_by_category[['Amount', 'Percentage', 'Monthly']].to_csv('expenses_by_category.csv')
print(first_date)
print(last_date)
print((last_date - first_date).days)



print(total_months)

