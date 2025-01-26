import pandas as pd
import json

def generate_aligned_adaptive_card(dataframe, subject):
    """
    Generates an Adaptive Card table with strict alignment and consistent row coloring.

    Args:
        dataframe (pd.DataFrame): The data to include in the table.
        subject (str): The table header/title.

    Returns:
        dict: The JSON representation of the Adaptive Card.
    """
    # Start with the Adaptive Card template
    adaptive_card_template = {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.0",
        "body": [
            {
                "type": "TextBlock",
                "text": subject,
                "weight": "bolder",
                "size": "Large",
                "wrap": True
            },
            {
                "type": "Container",
                "items": []
            }
        ]
    }

    # Add the header row
    header_row = {
        "type": "ColumnSet",
        "columns": [
            {
                "type": "Column",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": column_name.strip(),
                        "weight": "bolder",
                        "wrap": True
                    }
                ],
                "width": "1"  # Fixed equal width for all columns
            } for column_name in dataframe.columns
        ],
        "style": "emphasis"  # Dark background for headers
    }
    adaptive_card_template["body"][1]["items"].append(header_row)

    # Add the data rows
    for index, row in dataframe.iterrows():
        row_data = {
            "type": "ColumnSet",
            "columns": []
        }

        # Populate columns
        for column_name, cell_value in row.items():
            cell_value = str(cell_value).strip()  # Ensure no extra spaces
            if column_name == "Issue key":
                # Add clickable links for Issue Key
                # url = "https://www.google.com" if cell_value == "TEST-001" or cell_value == "TEST-002" else "https://www.microsoft.com"

                url,issue_key=extract_url_and_issue_key(cell_value)
                row_data["columns"].append({
                    "type": "Column",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": f"[{issue_key}]({url})",  # Markdown-style link
                            "wrap": True
                        }
                    ],
                    "width": "1"  # Fixed equal width for all columns
                })
            else:
                # Regular text for other columns
                row_data["columns"].append({
                    "type": "Column",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": cell_value,
                            "wrap": True
                        }
                    ],
                    "width": "1"  # Fixed equal width for all columns
                })

        # Apply consistent row styling
        row_data["style"] = "default" if index % 2 == 0 else "emphasis"  # Alternate row colors

        adaptive_card_template["body"][1]["items"].append(row_data)

    # Save the Adaptive Card JSON to a file
    with open('format_data.json', 'w') as json_file:
        json.dump(adaptive_card_template, json_file, indent=4)

    return adaptive_card_template
import re

def extract_url_and_issue_key(input_string):
    """
    Extracts the URL and Issue Key from an HTML string.

    Args:
        input_string (str): The input string containing the HTML link.

    Returns:
        list: A list containing the URL and Issue Key.
    """
    # Define the regular expression to match the URL and Issue Key
    pattern = r'<a href="(https?://[^"]+)"[^>]*>([^<]+)</a>'

    # Search for the pattern in the input string
    match = re.search(pattern, input_string)

    if match:
        # Return the URL and Issue Key
        url = match.group(1)
        issue_key = match.group(2)
        return [url, issue_key]
    else:
        # If no match found, return an empty list
        return []

# Test the function
 


# Sample DataFrame for testing
data = {
    'Eng Lead': ['Venkatesh M', 'Rajesh K', 'Abdul R'],
    'Assignee': ['John Doe', 'Jane Smith', 'Emily Davis'],
    'Issue key': ['<a href="https://domain.com/brower/TEST-01" target="_blank">TESt-02</a>', '<a href="https://domain.com/brower/TEST-01" target="_blank">TESt-03</a>', '<a href="https://domain.com/brower/TEST-01" target="_blank">TESt-04</a>']
}
df = pd.DataFrame(data)

# Call the function with the DataFrame and a subject
subject = "JIRA Issues Table (Aligned)"
adaptive_card_json = generate_aligned_adaptive_card(df, subject)

print("Adaptive Card JSON with fixed alignment saved to 'aligned_table_fixed.json'")


# <a href="https://domain.com/brower/TEST-01" target="_blank">TESt-01<a/>
