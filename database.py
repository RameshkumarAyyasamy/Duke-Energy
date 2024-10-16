import sqlite3

def store_event(event_id, substation, snapshot_path, event_time):
    """Stores an event in the database."""
    conn = sqlite3.connect('surveillance.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS events
                      (id TEXT, substation TEXT, snapshot_path TEXT, event_time TEXT)''')
    # Store the timestamp in 'YYYYMMDD_HHMMSS' format
    event_time_str = event_time.strftime("%Y%m%d_%H%M%S")
    cursor.execute('INSERT INTO events (id, substation, snapshot_path, event_time) VALUES (?, ?, ?, ?)',
                   (event_id, substation, snapshot_path, event_time_str))
    conn.commit()
    conn.close()


def find_common_events():
    """Finds and returns common events from the database."""
    conn = sqlite3.connect('surveillance.db')
    cursor = conn.cursor()

    # Get all events
    cursor.execute('SELECT * FROM events')
    events = cursor.fetchall()

    # Optional: filter events for duplicates based on your criteria
    # For example, by IDs or by date. Here we can just return all.
    conn.close()
    return events


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