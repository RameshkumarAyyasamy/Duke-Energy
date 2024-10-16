import cv2
import os
import json
import uuid
from datetime import datetime

# File where events will be stored
json_file_path = 'events_data.json'

def capture_image_from_camera(save_directory='./captured_images'):
    """Capture an image from the camera and save it to the folder."""
    os.makedirs(save_directory, exist_ok=True)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    image_captured = False  # Track whether an image has been captured

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        cv2.imshow('Camera Feed', frame)

        # Press 's' to save the image
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            event_id = str(uuid.uuid4())
            timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            image_name = f"{event_id}.png"
            save_path = os.path.join(save_directory, image_name)

            cv2.imwrite(save_path, frame)
            print(f"Image saved to {save_path}")

            # Add the image event to the JSON data in events_data.json
            add_image_event_to_json(event_id, timestamp, save_path)
            image_captured = True  # Mark that an image was captured

            # Exit the loop after saving the image
            break

        # Press 'q' to quit
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Check if an image was captured
    if not image_captured:
        print("Failed to capture image. Exiting.")
    else:
        print("Image capture completed successfully.")

def add_image_event_to_json(event_id, timestamp, image_path, substation_id="Substation1"):
    """Add a new image event to the JSON data in events_data.json."""
    new_event = {
        "event_id": event_id,
        "timestamp": timestamp,
        "event_url": image_path,
        "SubstationId": substation_id
    }

    # Check if the JSON file exists; if not, create an empty list
    if not os.path.exists(json_file_path):
        events_data = []
    else:
        # Load existing data from events_data.json
        with open(json_file_path, 'r') as file:
            events_data = json.load(file)

    # Append the new event to the data
    events_data.append(new_event)

    # Write the updated data back to events_data.json
    with open(json_file_path, 'w') as file:
        json.dump(events_data, file, indent=4)

    print(f"Event {event_id} added with timestamp {timestamp}.")

if __name__ == "__main__":
    # Capture image and update events_data.json
    capture_image_from_camera(save_directory='./localSnap')
