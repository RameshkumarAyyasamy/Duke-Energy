import os
import uuid
import json
from datetime import datetime
from camera import capture_image_from_camera
from event_processing import check_event
from database import store_event, clear_database, clear_events, get_all_events
from mock import json_data

json_file_path = 'events_data.json'

def main():
    save_directory = "./localSnap"  # Directory for saving snapshots
    os.makedirs(save_directory, exist_ok=True)  # Create the directory if it doesn't exist

    # Read the event data from the JSON file
    with open(json_file_path, 'r') as file:
        events_data = json.load(file)

        # print("Events data loaded: ", events_data)

    for event in events_data:
        event_id = event["event_id"]
        substation_id = event["SubstationId"]
        image_url = event["event_url"]
        timestamp = datetime.strptime(event["timestamp"], "%Y-%m-%dT%H:%M:%S")
        save_path = os.path.join(save_directory, f"{event_id}_.png")
        
        # Ensure the image exists at the given path
        if os.path.exists(image_url):
            os.system(f"cp {image_url} {save_path}")
        else:
            print(f"Image not found at {image_url}, skipping event {event_id}.")
            continue

        snapshot_path = save_path

        # Check for duplicates or threats
        event_status = check_event(event_id, timestamp, substation_id, snapshot_path)
        if event_status == "No duplicate or threat found":
            store_event(event_id, substation_id, snapshot_path, timestamp)
            print(f"Event {event_id} stored successfully at {timestamp}.")
        else:
            print(f"{event_status} for ID: {event_id} at {timestamp}")
 

if __name__ == "__main__":
    clear_database()
    # clear_events()
    capture_image_from_camera()  
    
    main()