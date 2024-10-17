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

    for event in events_data:
        event_id = event["event_id"]
        substation_id = event["SubstationId"]
        image_url = event["event_url"]
        timestamp = datetime.strptime(event["timestamp"], "%Y-%m-%dT%H:%M:%S")
        event_type = event.get("event_type", "face")  # Default to face if no type is provided
        save_path = os.path.join(save_directory, f"{event_id}_.png")
        
        # Ensure the image exists at the given path
        if os.path.exists(image_url):
            os.system(f"cp {image_url} {save_path}")
        else:
            print(f"Image not found at {image_url}, skipping event {event_id}.")
            continue

        snapshot_path = save_path

        # Check for duplicates or threats based on event type (face or license plate)
        event_status = check_event(event_id, timestamp, substation_id, snapshot_path, event_type)
        
        if event_status is None or "Duplicate" not in event_status:
            store_event(event_id, substation_id, snapshot_path, timestamp, event_type)
            print(f"{event_type.capitalize()} event {event_id} stored successfully at {timestamp} and it's a {event_status}")
        else:
            print(f"{event_status} for ID: {event_id} at {timestamp}.")

if __name__ == "__main__":
    # print(get_all_events())
    clear_database()
    # capture_image_from_camera()  
    # main()