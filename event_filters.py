from datetime import datetime

def filter_face_events(events):
    """Filters and returns unique face events based on rules."""
    filtered_events = []
    seen_faces = set()

    for event in events:
        if event['type'] == 'face':
            face_id = extract_face_id(event['data'])  # Your custom function to extract face ID
            if face_id not in seen_faces:
                seen_faces.add(face_id)
                filtered_events.append(event)

    return filtered_events

def filter_license_plate_events(events):
    """Filters and returns unique license plate events based on rules."""
    filtered_events = []
    seen_plates = set()

    for event in events:
        if event['type'] == 'license_plate':
            plate_number = extract_plate_number(event['data'])  # Your custom function to extract plate number
            if plate_number not in seen_plates:
                seen_plates.add(plate_number)
                filtered_events.append(event)

    return filtered_events

def filter_events_on_same_day(events, event_type):
    """Identifies events of the same type that occurred on the same day in multiple locations."""
    same_day_events = []

    for i, event1 in enumerate(events):
        for event2 in events[i+1:]:
            if event1['type'] == event_type and event2['type'] == event_type:
                date1 = event1['timestamp'].split(' ')[0]
                date2 = event2['timestamp'].split(' ')[0]
                if date1 == date2 and event1['location'] != event2['location']:
                    same_day_events.append((event1, event2))

    return same_day_events

# Helper functions (to be implemented according to your requirements)
def extract_face_id(image_data):
    """Extracts a unique face ID from the image data."""
    # Logic to extract face ID goes here
    return "some_face_id"

def extract_plate_number(image_data):
    """Extracts the license plate number from the image data."""
    # Logic to extract license plate number goes here
    return "some_plate_number"
