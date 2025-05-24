from typing import List, Optional, Generator
from fastapi import FastAPI, HTTPException, status, Depends,Query
from sqlalchemy.orm import Session

# Import your SQLAlchemy ORM models, Pydantic schemas, and database setup
# Note: These are absolute imports because main.py is the top-level script.
import models
import schemas
from database import SessionLocal, create_db_and_tables # No need to import 'engine' here
import crud 

# Initialize FastAPI application with metadata
app = FastAPI(
    title="Music Catalog API (Persistent Data)",
    description="A CRUD API for managing a music catalog with persistent SQLite storage using SQLAlchemy.",
    version="2.0.0", # Updated version for database integration
)

# --- Database Dependency ---
# This function provides a database session for each request.
# It ensures the session is properly closed after the request is finished.
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal() # Get a new session from the session factory
    try:
        yield db # Yield the session to the endpoint function
    finally:
        db.close() # Close the session after the request is processed

# --- Application Startup Event ---
# This decorator runs the 'on_startup' function when the FastAPI application starts up.
# It's used to create database tables if they don't already exist.
@app.on_event("startup")
def on_startup():
    create_db_and_tables() # Call the utility function to create tables

# --- API Endpoints (now using database sessions) ---

# CREATE Operation: Add a new song
@app.post("/songs/", response_model=schemas.Song, status_code=status.HTTP_201_CREATED, summary="Add a new song to the catalog")
async def create_song_endpoint(song_data: schemas.SongCreate, db: Session = Depends(get_db)):
    """
    Creates a new song in the catalog.
    - **id**: Optional. If not provided or 0, a new unique ID will be assigned by the database.
    - **title**: The title of the song.
    - **artist**: The artist of the song.
    - **album**: The album the song belongs to.
    - **genre**: The genre of the song.
    - **release_year**: The year the song was released.
    Raises:
    - `400 Bad Request`: If a song with the provided ID already exists.
    """
    new_song = crud.create_new_song(db=db, song_data=song_data)
    if new_song is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Song with ID {song_data.id} already exists. Please use a different ID or omit it for auto-assignment."
        )
    return new_song

# READ Operation: Retrieve all songs
@app.get("/songs/", response_model=List[schemas.Song], summary="Retrieve all songs in the catalog")
async def read_all_songs_endpoint(db: Session = Depends(get_db)):
    """
    Retrieves a list of all songs currently in the catalog.
    """
    return crud.get_all_songs(db=db)

# READ Operation: Retrieve a single song by ID
@app.get("/songs/{song_id}", response_model=schemas.Song, summary="Retrieve a single song by its ID")
async def read_song_by_id_endpoint(song_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single song by its unique ID.
    Raises:
    - `404 Not Found`: If the song with the given ID is not found.
    """
    song = crud.get_song_by_id(db=db, song_id=song_id)
    if song is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Song with ID {song_id} not found")
    return song

# UPDATE Operation: Fully replace an existing song by ID
@app.put("/songs/{song_id}", response_model=schemas.Song, summary="Fully update an existing song by ID")
async def update_song_endpoint(song_id: int, updated_song_data: schemas.Song, db: Session = Depends(get_db)):
    """
    Updates an existing song identified by its ID with new data.
    This performs a full replacement of the song's data.
    - **song_id**: The ID of the song to update (from URL path).
    - **updated_song_data**: The complete new song data.
    Raises:
    - `404 Not Found`: If the song is not found.
    - `400 Bad Request`: If the ID in the URL does not match the ID in the request body.
    """
    # Ensure the ID in the URL path matches the ID in the request body for a PUT operation
    if updated_song_data.id != song_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Song ID in URL ({song_id}) does not match ID in request body ({updated_song_data.id}). For a PUT operation, these must match."
        )

    updated_song = crud.update_existing_song(db=db, song_id=song_id, updated_song_data=updated_song_data)
    if updated_song is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Song with ID {song_id} not found")
    return updated_song

# UPDATE Operation: Partially update an existing song by ID (PATCH)
@app.patch("/songs/{song_id}", response_model=schemas.Song, summary="Partially update an existing song by ID")
async def patch_song_endpoint(song_id: int, song_update_data: schemas.SongUpdate, db: Session = Depends(get_db)):
    """
    Partially updates an existing song identified by its ID.
    Only the fields provided in the request body will be updated.
    - **song_id**: The ID of the song to update.
    - **song_update_data**: The partial song data to apply.
    Raises:
    - `404 Not Found`: If the song is not found.
    """
    updated_song = crud.patch_existing_song(db=db, song_id=song_id, song_update_data=song_update_data)
    if updated_song is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Song with ID {song_id} not found")
    return updated_song

# DELETE Operation: Remove a song by ID
@app.delete("/songs/{song_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a song by its ID")
async def delete_song_endpoint(song_id: int, db: Session = Depends(get_db)):
    """
    Deletes a song from the catalog by its unique ID.
    Raises:
    - `404 Not Found`: If the song is not found.
    Returns:
    - `204 No Content`: On successful deletion.
    """
    deleted = crud.delete_song_by_id(db=db, song_id=song_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Song with ID {song_id} not found")
    return {} # Return empty dict for 204 No Content

# --- New Search Endpoint ---
@app.get("/songs/search/", response_model=List[schemas.Song], summary="Search songs by criteria")
async def search_songs_endpoint(
    title: Optional[str] = Query(None, description="Partial or exact match for song title (case-insensitive)"),
    artist: Optional[str] = Query(None, description="Partial or exact match for artist name (case-insensitive)"),
    album: Optional[str] = Query(None, description="Partial or exact match for album title (case-insensitive)"),
    genre: Optional[str] = Query(None, description="Partial or exact match for genre (case-insensitive)"),
    release_year: Optional[int] = Query(None, description="Exact match for release year"),
    db: Session = Depends(get_db)
):
    """
    Searches for songs based on optional criteria.
    - **artist**: Filter by artist name (case-insensitive, partial match).
    - **album**: Filter by album title (case-insensitive, partial match).
    - **genre**: Filter by genre (case-insensitive, partial match).
    - **release_year**: Filter by exact release year.
    """
    songs = crud.search_songs(
        db=db,
        title=title,  
        artist=artist,
        album=album,
        genre=genre,
        release_year=release_year
    )
    return songs
