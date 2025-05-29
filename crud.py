from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_ # Imported for the search functionality

# Import both your SQLAlchemy ORM models and Pydantic schemas
# Note: These are absolute imports because crud.py is treated as a top-level module
# when imported by main.py in this flat project structure.
import models
import schemas
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# No more in-memory list (songs_db) or next_song_id here!
# All data operations will now go through the 'db' session.

# --- CRUD Functions using SQLAlchemy Session ---

def get_all_songs(db: Session, skip: int = 0, limit: int = 100) -> List[models.Song]:
    """
    Retrieves all songs from the database with optional skip and limit for pagination.
    :param db: The SQLAlchemy database session.
    :param skip: Number of records to skip (for pagination).
    :param limit: Maximum number of records to return (for pagination).
    :return: A list of SQLAlchemy Song ORM objects.
    """
    return db.query(models.Song).offset(skip).limit(limit).all()

def get_song_by_id(db: Session, song_id: int) -> Optional[models.Song]:
    """
    Retrieves a single song by its ID from the database.
    :param db: The SQLAlchemy database session.
    :param song_id: The unique ID of the song.
    :return: The SQLAlchemy Song ORM object if found, otherwise None.
    """
    return db.query(models.Song).filter(models.Song.id == song_id).first()

def create_new_song(db: Session, song_data: schemas.SongCreate) -> Optional[models.Song]:
    """
    Creates a new song and adds it to the database.
    Handles ID assignment (database auto-increment) and checks for duplicate IDs if provided.
    :param db: The SQLAlchemy database session.
    :param song_data: The Pydantic schema for creating a song.
    :return: The created SQLAlchemy Song ORM object, or None if a duplicate ID is found.
    """
    # If client provided an ID, check for duplicates in the database
    if song_data.id is not None and song_data.id != 0:
        existing_song = db.query(models.Song).filter(models.Song.id == song_data.id).first()
        if existing_song:
            return None # Indicate duplicate ID

    # Create the SQLAlchemy ORM model instance from the Pydantic schema data.
    # Use .dict() for Pydantic v1.x
    db_song = models.Song(**song_data.dict(exclude_unset=True))

    db.add(db_song)      # Add the new song object to the session
    db.commit()          # Commit the transaction to save changes to the database
    db.refresh(db_song)  # Refresh the object to get any database-generated values (like auto-incremented ID)
    return db_song

def update_existing_song(db: Session, song_id: int, updated_song_data: schemas.Song) -> Optional[models.Song]:
    """
    Updates an existing song by ID in the database (full replacement).
    :param db: The SQLAlchemy database session.
    :param song_id: The ID of the song to update.
    :param updated_song_data: The Pydantic schema with complete updated song data.
    :return: The updated SQLAlchemy Song ORM object if found, otherwise None.
    """
    db_song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if db_song is None:
        return None # Song not found

    # Update attributes of the existing ORM object.
    # Use .dict() for Pydantic v1.x
    update_data = updated_song_data.dict()
    for key, value in update_data.items():
        setattr(db_song, key, value)

    db.add(db_song)      # Add the modified object back to the session (it's already tracked, but good practice)
    db.commit()          # Commit the transaction
    db.refresh(db_song)  # Refresh to ensure all changes are loaded from the database
    return db_song

def patch_existing_song(db: Session, song_id: int, song_update_data: schemas.SongUpdate) -> Optional[models.Song]:
    """
    Partially updates an existing song by ID in the database.
    :param db: The SQLAlchemy database session.
    :param song_id: The ID of the song to partially update.
    :param song_update_data: The Pydantic schema with partial song data.
    :return: The updated SQLAlchemy Song ORM object if found, otherwise None.
    """
    db_song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if db_song is None:
        return None # Song not found

    # Convert the incoming partial update data to a dictionary, excluding unset fields.
    # Use .dict() for Pydantic v1.x
    update_data = song_update_data.dict(exclude_unset=True)

    # Apply updates to the attributes of the existing ORM object
    for key, value in update_data.items():
        setattr(db_song, key, value)

    db.add(db_song)      # Add the modified object back to the session
    db.commit()          # Commit the transaction
    db.refresh(db_song)  # Refresh to ensure all changes are loaded from the database
    return db_song

def delete_song_by_id(db: Session, song_id: int) -> bool:
    """
    Deletes a song by its ID from the database.
    :param db: The SQLAlchemy database session.
    :param song_id: The ID of the song to delete.
    :return: True if deleted, False if not found.
    """
    db_song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if db_song is None:
        return False # Song not found

    db.delete(db_song) # Mark the object for deletion
    db.commit()      # Commit the transaction
    return True

def search_songs(
    db: Session,
    title: Optional[str] = None,
    artist: Optional[str] = None,
    album: Optional[str] = None,
    genre: Optional[str] = None,
    release_year: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[models.Song]:
    """
    Searches for songs based on provided criteria.
    :param db: The SQLAlchemy database session.
    :param artist: Optional artist name to filter by (case-insensitive, partial match).
    :param album: Optional album title to filter by (case-insensitive, partial match).
    :param genre: Optional genre to filter by (case-insensitive, partial match).
    :param release_year: Optional exact release year to filter by.
    :param skip: Number of records to skip (for pagination).
    :param limit: Maximum number of records to return (for pagination).
    :return: A list of SQLAlchemy Song ORM objects matching the criteria.
    """
    query = db.query(models.Song)
    
    if title:
        query = query.filter(models.Song.title.ilike(f"%{title}%"))
    if artist:
        # .ilike() is for case-insensitive partial matching (SQL LIKE operator)
        query = query.filter(models.Song.artist.ilike(f"%{artist}%"))
    if album:
        query = query.filter(models.Song.album.ilike(f"%{album}%"))
    if genre:
        query = query.filter(models.Song.genre.ilike(f"%{genre}%"))
    if release_year:
        query = query.filter(models.Song.release_year == release_year)

    return query.offset(skip).limit(limit).all()

# --- NEW: Function to Update Song Metadata ---
def update_song_metadata(db: Session, song_id: int, metadata: Dict[str, Any]) -> Optional[models.Song]:
    """
    Updates the enriched metadata fields for a specific song in the database.

    Args:
        db (Session): The SQLAlchemy database session.
        song_id (int): The ID of the song to update.
        metadata (Dict[str, Any]): A dictionary containing the new metadata fields
                                    (e.g., {"bpm": 120, "mood": "Energetic"}).

    Returns:
        Optional[models.Song]: The updated Song ORM object if found, otherwise None.
    """
    db_song = db.query(models.Song).filter(models.Song.id == song_id).first()

    if db_song:
        # Loop through the metadata dictionary and update corresponding attributes
        for key, value in metadata.items():
            # Check if the key is a valid attribute of the Song model
            if hasattr(db_song, key):
                setattr(db_song, key, value)
            else:
                logger.warning(f"Attempted to set unknown metadata field '{key}' for song ID {song_id}.")
        
        db.add(db_song) # Add the modified object to the session
        db.commit()      # Commit the transaction to save changes
        db.refresh(db_song) # Refresh the object to get the latest state from the DB
        logger.info(f"Successfully updated metadata for song ID: {song_id}")
        return db_song
    else:
        logger.warning(f"Attempted to update metadata for non-existent song ID: {song_id}")
        return None
