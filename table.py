import pandas as pd

# Define column names
columns_names = ['Eng Lead', 'Assignee', 'Issue key']

# Generate some sample data
row_data = [
    ['Venkatesh M', 'John Doe', 'PROJ-101'],
    ['Rajesh K', 'Jane Smith', 'PROJ-102'],
    ['Abdul R', 'Emily Davis', 'PROJ-103'],
    ['Suresh P', 'Chris Brown', 'PROJ-104'],
    ['Kiran V', 'Sarah Taylor', 'PROJ-105']
]

# Create a DataFrame
df = pd.DataFrame(row_data, columns=columns_names)

# Save to CSV
csv_filename = 'jira_sample_data.csv'
df.to_csv(csv_filename, index=False)

print(f"Data saved to {csv_filename}")
