import pandas as pd

# Load the Excel file
df = pd.read_excel('dataset.xlsx')

# Convert it to a CSV file
df.to_csv('data.csv', index=False)