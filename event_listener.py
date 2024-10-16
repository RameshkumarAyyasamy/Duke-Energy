import requests
import os  # Import os to manage directories

def pull_snapshot(event_url, save_path):
    """Pull a snapshot from the given URL and save it locally."""
    try:
        response = requests.get(event_url)
        response.raise_for_status()  # Check if request was successful
        
        # Save the image locally
        with open(save_path, 'wb') as file:
            file.write(response.content)
        
        return save_path
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Specific HTTP error
        return None
    except Exception as e:
        print(f"Failed to pull snapshot: {e}")  # General error handling
        return None
