from datetime import datetime

def filter_face_events(events):
    """Filters events related to face detection."""
    face_events = []
    for event in events:
        # Ensure we are checking against the correct key
        if event.get('event_type') == 'face':  
            face_events.append(event)
    return face_events


def filter_license_plate_events(events):
    """Filters and returns unique license plate events based on rules."""
    filtered_events = []
    seen_plates = set()

    for event in events:
        # Ensure we are checking against the correct key
        if event.get('event_type') == 'license_plate':
            # plate_number = extract_plate_number(event.get('data'))  # Use .get() to avoid KeyError
            # if plate_number not in seen_plates:
            #     seen_plates.add(plate_number)
            filtered_events.append(event)

    return filtered_events
