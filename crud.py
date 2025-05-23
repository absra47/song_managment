from typing import List, Optional
# In crud.py (NEW - CORRECT)
from models import Song, SongCreate, SongUpdate # <--- CORRECT: Absolute import

# In-memory "database"
# This list will hold Song objects
songs_db: List[Song] = []
next_song_id = 1 # Simple counter for auto-incrementing IDs

# --- CRUD Functions ---

def get_all_songs() -> List[Song]:
    """Retrieves all songs from the database."""
    return songs_db

def get_song_by_id(song_id: int) -> Optional[Song]:
    """Retrieves a single song by its ID."""
    for song in songs_db:
        if song.id == song_id:
            return song
    return None # Return None if song is not found

def create_new_song(song_data: SongCreate) -> Optional[Song]:
  
    global next_song_id

    # Check for duplicate ID if provided by the client
    if song_data.id is not None and song_data.id != 0:
        for existing_song in songs_db:
            if existing_song.id == song_data.id:
                return None # Indicate duplicate ID
        # If ID is provided and unique, use it
        new_song_id = song_data.id
    else:
        # Assign a new auto-incrementing ID
        new_song_id = next_song_id

    # Create the Song object with the assigned/provided ID
    new_song = Song(
        id=new_song_id,
        title=song_data.title,
        artist=song_data.artist,
        album=song_data.album,
        genre=song_data.genre,
        release_year=song_data.release_year
    )

    songs_db.append(new_song)

    # Ensure next_song_id is always greater than the highest ID used so far
    max_existing_id = max([s.id for s in songs_db] + [0])
    next_song_id = max(next_song_id, max_existing_id + 1)

    return new_song

def update_existing_song(song_id: int, updated_song_data: Song) -> Optional[Song]:
    
    found_index = -1
    for index, song in enumerate(songs_db):
        if song.id == song_id:
            found_index = index
            break

    if found_index == -1:
        return None # Song not found

    # Replace the existing song with the updated data
    songs_db[found_index] = updated_song_data
    return songs_db[found_index]

# In crud.py
def patch_existing_song(song_id: int, song_update_data: SongUpdate) -> Optional[Song]:
    """
    Partially updates an existing song by ID.
    Returns the updated Song object or None if not found.
    """
    found_index = -1 # Initialize found_index

    # --- THIS IS THE MISSING LOOP ---
    for index, song in enumerate(songs_db):
        if song.id == song_id:
            found_index = index
            break
    # --- THIS IS THE MISSING LOOP ---

    if found_index == -1:
        return None # Song not found (because the loop didn't find it)

    current_song = songs_db[found_index] # Now found_index will be a valid index if song was found

    # 1. Convert the incoming partial update data to a dictionary, excluding unset fields
    update_data = song_update_data.dict(exclude_unset=True)

    # 2. Create a new Song instance by copying the current song and updating its attributes
    #    This is generally more robust for partial updates on Pydantic models.
    updated_song = current_song.copy(update=update_data)

    # 3. Replace the old song object in the database with the new, updated one
    songs_db[found_index] = updated_song

    return songs_db[found_index]
def delete_song_by_id(song_id: int) -> bool:
   
    global songs_db
    initial_len = len(songs_db)
    songs_db = [song for song in songs_db if song.id != song_id]

    return len(songs_db) < initial_len # True if an item was removed
