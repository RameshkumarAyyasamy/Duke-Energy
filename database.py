import sqlite3
from event_filters import filter_face_events, filter_license_plate_events

def store_event(event_id, substation, snapshot_path, event_time, event_type):
    """Stores an event in the database."""
    conn = sqlite3.connect('surveillance.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS events
                      (id TEXT, substation TEXT, snapshot_path TEXT, event_time TEXT, event_type TEXT)''')
    event_time_str = event_time.strftime("%Y%m%d_%H%M%S")
    cursor.execute('INSERT INTO events (id, substation, snapshot_path, event_time, event_type) VALUES (?, ?, ?, ?, ?)',
                   (event_id, substation, snapshot_path, event_time_str, event_type))
    conn.commit()
    conn.close()


def find_common_events():
    """Finds and returns common events from the database, optionally filtered."""
    conn = sqlite3.connect('surveillance.db')
    cursor = conn.cursor()
    
    # Get all events
    cursor.execute('SELECT id, substation, snapshot_path, event_time, event_type FROM events')
    events = cursor.fetchall()

    # Check if any events were retrieved
    if not events:
        print("No events found in the database.")
        return []

    # Transform into a list of dicts for easier manipulation
    events_dicts = [
        {
            'event_id': event[0],
            'substation': event[1],
            'snapshot_path': event[2],
            'timestamp': event[3],
            'event_type': event[4]  # Make sure this key matches your filtering logic
        }
        for event in events
    ]

    # Filter face events
    filtered_faces = filter_face_events(events_dicts)
    
    # Filter license plate events
    filtered_plates = filter_license_plate_events(events_dicts)
    
    conn.close()
    
    # Return filtered results, or process them further
    return filtered_faces, filtered_plates

    """Finds and returns common events from the database, optionally filtered."""
    conn = sqlite3.connect('surveillance.db')
    cursor = conn.cursor()
    
    # Get all events
    cursor.execute('SELECT id, substation, snapshot_path, event_time, event_type FROM events')
    events = cursor.fetchall()

    # Debugging: Print the number of events retrieved
    print(f"Number of events retrieved: {len(events)}")

    # Check if any events were retrieved
    if not events:
        print("No events found in the database.")
        return []

    # Transform into a list of dicts for easier manipulation
    events_dicts = [
        {
            'event_id': event[0],
            'substation': event[1],
            'snapshot_path': event[2],
            'timestamp': event[3],
            'type': event[4]
        }
        for event in events
    ]
    
    # Filter face events
    filtered_faces = filter_face_events(events_dicts)
    
    # Filter license plate events
    filtered_plates = filter_license_plate_events(events_dicts)
    
    conn.close()
    
    # Return filtered results, or process them further
    return filtered_faces, filtered_plates


def get_all_events():
    """Retrieves all events from the database for debugging."""
    with sqlite3.connect('surveillance.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM events')
        events = cursor.fetchall()
        # print("All Events in Database:", events)  # Debug line
    return events


#Clear Events and DB
def clear_events():
    """Clears all events from the database."""
    with sqlite3.connect('surveillance.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM events')
        conn.commit()

def clear_database():
    conn = sqlite3.connect('surveillance.db')
    cursor = conn.cursor()
    
    # Delete all records from the events table
    cursor.execute('DELETE FROM events')
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print("All records cleared from the database.")