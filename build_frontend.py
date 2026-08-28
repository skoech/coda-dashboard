import json # For reading issues.json
from datetime import datetime   # Shows date refreshed
from jinja2 import Template # Import the Template class from the jinja2 module for use in rendering HTML templates with dynamic data (fills the placeholders, and converts template into final HTML).
import mistune # Markdown parser for converting Markdown text to HTML


# Build the dashboard HTML page using the issues loaded from issues.json and the Jinja2 template
def load_json(json_path):
    """
    Load issues from issues.json: open the JSON file, read its contents, and parse it into a Python list of dictionaries.

    Args:
        json_path (str): Path to issues.json (the JSON file containing the fetched issues)
        
    Returns:
        A list of dictionaries, with each dictionary representing an issue from a repository.
    """

    with open(json_path, 'r') as file: # Open and read issues.json using the context manager
        issues = json.load(file) # Parse issues.json into a Python list of dictionaries
        return issues # Return the list of issues to the caller function (main)

def build_dashboard(json_path, template_path, output_path):
    """
    Build the static dashboard HTML page using the issues loaded from issues.json and the Jinja2 template
    
    Args:
        json_path (str): Path to issues.json
        template_path (str): Path to the Jinja2 template file (jinja_template.html)
        output_path (str): Path to the output HTML file

    Returns: 
        None: The function does not return any value; it writes the rendered HTML to the specified output path.
    """

    # Load issues from issues.json using the load_json function
    issues = load_json(json_path) # Call the load_json function to load issues from issues.json  
    print(f"Loaded {len(issues)} issues from {json_path}.")

    # Load template from jinja_template.html using the context manager
    with open(template_path, 'r') as file:
        template = Template(file.read()) # Read the contents of the template file and create a Jinja2 Template object

    # Process each issue
    for issue in issues:
        if issue.get('body'):

            # Convert Markdown to HTML
            html_text = strip_markdown(issue['body'])

            # Truncate to 500 chars
            if len(html_text) > 500:
                issue['body_truncated'] = html_text[:500] + '...'
            else:
                issue['body_truncated'] = html_text
        else:
            issue['body_truncated'] = "No description provided"


    # Render the template with the issues data
    print ("Generating dashboard HTML...")
    rendered_html = template.render(
        title="CODA dashboard",
        issues=issues,
        issue_count=len(issues),
    )

    # Save the rendered HTML
    with open(output_path, 'w') as file:
        file.write(rendered_html)

    print(f"Dashboard HTML generated and saved. Open {output_path} in a web browser to view the dashboard.")

def strip_markdown(text):
    """
    Convert Markdown to HTML for proper rendering

    Args:
    text (str): The Markdown text to clean

    Returns:
        str: HTML-rendered text from the Markdown input
    """
    if not text: # If there's no description/ text is empty or None
        return "No description provided"

    return mistune.markdown(text)

if __name__ == "__main__":
    build_dashboard('issues.json', 'jinja_template.html', 'index.html') # Call the build_dashboard function to build the dashboard when the script is run directly
