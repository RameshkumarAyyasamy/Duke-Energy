from datetime import datetime
from database import find_common_events
import hashlib
from PIL import Image
import imagehash

def compute_image_hash(image_path):
    """Compute the perceptual hash of an image for comparison."""
    with Image.open(image_path) as img:
        # Convert image to RGB for consistency
        img = img.convert("RGB")
        # Compute perceptual hash (phash)
        img_hash = imagehash.phash(img)  # Perceptual hash
        print("line:16", img_hash)
        return img_hash  # Return as an imagehash object for comparison

def compare_image_hashes(hash1, hash2, threshold=0.5):
    """Compare two image hashes and return similarity percentage."""
    # Calculate the number of differing bits
    difference = hash1 - hash2
    # Get the maximum possible difference
    max_difference = len(hash1.hash) * hash1.hash.shape[0]  # Total bits in hash
    # Calculate the similarity percentage
    similarity = 1 - (difference / max_difference)
    return similarity

def check_event(event_id, timestamp, substation_id, snapshot_path):
    """Check if the event is a duplicate or a threat based on event details."""
    
    # Ensure timestamp is a datetime object
    if isinstance(timestamp, str):
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

    # Retrieve existing events from the database
    existing_events = find_common_events()  # This should return all events for comparison

    # Compute the hash for the new image
    new_image_hash = compute_image_hash(snapshot_path)

    for existing_event in existing_events:
        existing_time = datetime.strptime(existing_event[3], "%Y%m%d_%H%M%S")  # Adjust according to your format
        existing_substation = existing_event[1]
        existing_image_path = existing_event[2]
        
        # Compute the hash for the existing image
        existing_image_hash = compute_image_hash(existing_image_path)

        # Compare hashes to get similarity
        similarity = compare_image_hashes(new_image_hash, existing_image_hash)

        # Check if it's a duplicate (similar image hash in the same substation)
        if similarity >= 0.5 and substation_id == existing_substation:
            return "Duplicate"  # Similar image and same substation indicates a duplicate
        
        # Check if it's a threat (similar image hash but from different substations)
        if similarity >= 0.5 and substation_id != existing_substation:
            return "Threat"  # Similar image from a different substation indicates a threat

    return "No duplicate or threat found"  # Neither a duplicate nor a threat
