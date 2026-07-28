import requests

# Simple script to fetch issues from Ulwazi repository 
# For learning how GitHub API works
# GitHub API: https://api.github.com/

# GitHub API endpoint for issues
# (format): https://api.github.com/repos/{owner}/{repo}/issues)
# Default repository: canonical/ulwazi
# Define the repository owner and name (variables to store repository info)
owner = "canonical"
repo = "ulwazi"

# Define the URL for fetching issues from the GitHub API (Ulwazi repository)
# Add query parameters for the issue, e.g. state (open/closed);
# label (e.g. coda, docs); per-page (100: get up to 100 results per page)
URL = f"https://api.github.com/repos/{owner}/{repo}/issues?state=open&per_page=100"

# To show terminal output
print(f"Fetching issues from {owner}/{repo}")
print(f"API URL: {URL}")
print("-" * 50)

# Make the GET request to the GitHub API to fetch issues
# Script will use the requests library to send an HTTP GET request to the specified URL,
# wait for the response, and store it in the variable 'response'.
response = requests.get(URL)

# Check if the request was successful (if it returns status code 200 OK)
if response.status_code == 200:
    # Parse the JSON response into a Python list of dictionaries
    # (response.json converts the JSON format response into Python data)
    # Issues will appear as a list, where each item is a dictionary representing one issue
    issues = response.json()

    # Print the number of issues found in the response
    print() # Print a blank line before listing issues for better readability
    print(f"Found {len(issues)} issues")

    # Loop through each issue in the list and print its data (all available fields):
    # title, number, URL, author, assignee, labels, state, created_at,
    # updated_at, closed_at, description, etc.
    for issue in issues:
        print() # Print a blank line before first issue and between each issue for better readability
        print(f"All available fields in issue #{issue['number']}: {issue['title']}")
        print("-" * 50)

        # Loop through each key-value pair in the issue dictionary and print them
        for key in issue:
            # Skip the title field since it's already included in the header
            if key == "title":
                continue # Skip to the next key in the loop
            value = issue[key]
            print(f"{key}: {value}")
else:
    # If the request was not successful, print an error message with the HTTP status code
    print(f"Failed to fetch issues. Error: {response.status_code}")
