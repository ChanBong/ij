import sqlite3
import json

def create_table():
    # Create a connection to the SQLite database (or create a new one if it doesn't exist)
    conn = sqlite3.connect('photo_database.db')

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create a table to store photo data if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS photo_data (
            photo_path TEXT PRIMARY KEY,
            thumbnail_photo_path TEXT,
            is_screenshot INTEGER,
            tags TEXT,
            part_of_which_album TEXT,
            face_ids TEXT,
            metadata_fields TEXT,
            summary TEXT
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def add_photo_data(data):
    # Create a connection to the SQLite database
    conn = sqlite3.connect('photo_database.db')

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Insert the provided data into the photo_data table
    cursor.execute('''
        INSERT INTO photo_data (
            photo_path, thumbnail_photo_path, is_screenshot, tags,
            part_of_which_album, face_ids, metadata_fields, summary
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['photo_path'],
        data['thumbnail_photo_path'],
        int(data['is_screenshot']),
        json.dumps(data['tags']),
        json.dumps(data['part_of_which_album']),
        json.dumps(data['face_ids']),
        json.dumps(data['metadata_fields']),
        data['summary']
    ))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def get_photo_data(photo_path):
    # Create a connection to the SQLite database
    conn = sqlite3.connect('photo_database.db')

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Retrieve data for the specified photo_path from the photo_data table
    cursor.execute('SELECT * FROM photo_data WHERE photo_path = ?', (photo_path,))
    result = cursor.fetchone()

    # Close the connection
    conn.close()

    # Return the loaded information or None if not found
    if result:
        columns = ['photo_path', 'thumbnail_photo_path', 'is_screenshot', 'tags',
                   'part_of_which_album', 'face_ids', 'metadata_fields', 'summary']
        data = dict(zip(columns, result))
        data['tags'] = json.loads(data['tags'])
        data['part_of_which_album'] = json.loads(data['part_of_which_album'])
        data['face_ids'] = json.loads(data['face_ids'])
        data['metadata_fields'] = json.loads(data['metadata_fields'])
        return data
    else:
        return None

def photo_path_exists(photo_path):
    # Create a connection to the SQLite database
    conn = sqlite3.connect('photo_database.db')

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Check if the specified photo_path exists in the photo_data table
    cursor.execute('SELECT COUNT(*) FROM photo_data WHERE photo_path = ?', (photo_path,))
    count = cursor.fetchone()[0]

    # Close the connection
    conn.close()

    # Return True if the photo_path exists, otherwise return False
    return count > 0


# Write a function to return the list of photos in the descending order ot CreateDate which a key in the metadata_fields dictionary
def get_photos_by_date():
    # Create a connection to the SQLite database
    conn = sqlite3.connect('photo_database.db')

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Retrieve the list of photos in the descending order of CreateDate
    cursor.execute('SELECT photo_path FROM photo_data ORDER BY metadata_fields->"CreateDate" DESC')
    result = cursor.fetchall()

    # Close the connection
    conn.close()

    # Return the list of photos
    return [row[0] for row in result]

print(get_photos_by_date())