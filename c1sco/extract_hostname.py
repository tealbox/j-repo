import re

# Function to extract hostname from a file
def extract_hostname(file_path):
    # Define the regex pattern
    pattern = r"hostname\s+(\S+)"
    
    try:
        # Open and read the file
        with open(file_path, "r") as file:
            content = file.read()
        
        # Search for the pattern in the file content
        match = re.search(pattern, content)
        
        if match:
            # Extract the hostname (group 1 of the match)
            hostname = match.group(1)
            return hostname
        else:
            return "Hostname not found in the file."
    
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
file_path = "config.txt"  # Replace with your file path
hostname = extract_hostname(file_path)
print(f"Extracted Hostname: {hostname}")
