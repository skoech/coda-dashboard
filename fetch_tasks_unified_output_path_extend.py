import requests # For HTTP requests to the GitHub API
import json     # For saving the fetched issues to a JSON file
import yaml     # For reading the YAML config file
import os       # For file path operations (e.g., checking if a file exists, creating directories and files)
import sys      # For exiting the program with sys.exit() when an error occurs
from pprint import pprint # Pretty print the config dictionary for better readability in the terminal output

## Read the YAML config, fetch issues from the GitHub API and save them to a JSON file
def read_config(config_path):
    """
    Read the YAML configuration file

    Args: 
        config_path (str): Path to the YAML config file

    Returns:
        A dictionary with the configuration data
    """
    with open(config_path, 'r') as file: # Use the context manager to open and read the YAML file (ensures the file is properly closed after reading)
        config = yaml.safe_load(file) # Parse the YAML file into a Python dictionary (which can be read and easily manipulated by the code)
    # File automatically closes
    # Config now contains Python data
    print(type(config)) # Print the type of the config variable (should be a dictionary)
    pprint(config) # Pretty print the config dictionary
    return config # Return the config dictionary to the caller function (main)

## Fetch issues from the repositories specified in the config  file using the GitHub API
def fetch_issues(owner, repo, labels=None, state='open'):

    """
    Fetch issues from a GitHub repository using the GitHub API
    
    Args:
        owner (str): The owner of the repository, e.g., 'canonical'
        repo (str): The name of the repository, e.g., 'ulwazi'
        labels (list): A list of labels to filter issues by. Optional parameter, default: None (no label filter; fetch all issues regardless of labels)
        state (str): The state of the issues to fetch; default: 'open'

    Returns:
        A list of dictionaries, with each dictionary representing an issue from a repository
    """
    # Define the URL for fetching issues from the GitHub API
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    # Make the GET request to the GitHub API to fetch issues
    # Script will use the requests library to send an HTTP GET request to the specified URL,
    # wait for the response, and store it in the variable 'response'.
    response = requests.get(url)

    if response.status_code == 200:
        issues = response.json() # Parse the JSON response into a Python list of dictionaries
        print(f"Found {len(issues)} issues in {owner}/{repo}") # Print the number of issues found in the response
        return issues # Return the list of issues to the caller function (main)
    else:
        print(f"Failed to fetch issues from {owner}/{repo}. Error: {response.status_code}") # If the request was not successful, print an error message with the HTTP status code
        print("Script exiting...") # Print a message indicating that the script is exiting due to the error
        print({response.text}) # Print the response text for debugging purposes
        sys.exit(1) # Exit the program with a non-zero exit code to indicate an error occurred

def save_to_json(issues, output_path):
    """
    Save the fetched issues to a JSON file

    Args:
        issues (list): A list of dictionaries, with each dictionary representing an issue from a repository
        output_path (str): Path to the JSON file where the issues will be saved
    """
    with open(output_path, 'w') as file: # Use the context manager to open the JSON file to write to (ensures that the file is properly closed after writing)
        json.dump(issues, file, indent=2) # Write the issues to the JSON file with indentation for better readability
        print(f"Saved {len(issues)} issues to {output_path}") # Print a confirmation message that the issues have been saved to the specified JSON file

def main():
    config_path = 'config.yaml' # Path to the YAML config file
    config = read_config(config_path) # Call the function to read the config file; save the returned dictionary in the variable 'config'

    # Create an empty array to store all issues from all repositories in memory (Don't write to JSON file until all issues have been fetched)
    all_issues = [] 

    # Loop through all the repos in the config file and fetch issues for each repo
    for repo_config in config['repositories']: # Loop through each repository configuration in the 'repositories' list from the config dictionary
        owner = repo_config['owner'] # Get the repository owner from the current repository config
        repo = repo_config['repo'] # Get the repository name from the current repository config

        print(f"Fetching issues from {owner}/{repo}") # Print a  message saying which repository is being processed
        issues = fetch_issues(owner, repo) # Call the function to fetch issues from the GitHub API; save the returned list of issues in the variable 'issues'

        # Create an empty array to store all issues from all repositories in memory (Don't write to JSON file until all issues have been fetched). Uses the extend() method. Builds up memory as the loop runs, and then writes once at the end of the loop. This is more efficient than writing to the JSON file after each repository is processed. Initially, I had the "save_to_json" function call inside the loop, which would write to the JSON file after each repository is processed. This was inefficient because of the multuple writes to disk; say we had 100 repos, that would mean 100 disk writes instead of one, which would be bad for performance.
        all_issues.extend(issues) # Add the fetched issues to the 'all_issues' array using the extend() method (adds each issue in the 'issues' list to the 'all_issues' list/collection)

        # Save all the fetched issues to a JSON file at once after all issues have been fetched from all repositories in the config file
        output_path = 'issues.json' # Define the output path for the JSON file where the issues will be saved

    save_to_json(all_issues, output_path) # Call the function to save the fetched issues to the JSON file created in the previous step
    print(f"\nSaved {len(all_issues)} total to {output_path}") # Print a confirmation message that the total number of issues after all looping through all repositories have been saved to the JSON file

if __name__ == "__main__":
    main()
