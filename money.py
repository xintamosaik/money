import pandas as pd

# Load the data and prepare initial categories
df = pd.read_csv('money.csv')
df['Category'] = 'Other'

# Define initial categories with keywords
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

# Automatically categorize known keywords
for category, keywords in categories.items():
    df.loc[df['Description'].isin(keywords), 'Category'] = category.capitalize()

# Manual categorization for 'Other' rows
other_rows = df[df['Category'] == 'Other']

for idx, row in other_rows.iterrows():
    print(f"\nDescription: {row['Description']}")
    category = input("Enter the category (or type 'skip' to ignore, 'exit' to stop): ").strip().lower()
    
    if category == 'exit':
        break
    elif category != 'skip':
        df.at[idx, 'Category'] = category.capitalize()  # Update the row with the entered category

# Save the categorized data to a new CSV
df.to_csv('money_categorized.csv', index=False)
print("\nSaved the categorized data to 'money_categorized.csv'")
