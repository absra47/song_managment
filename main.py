from typing import List, Optional, Generator
from fastapi import FastAPI, HTTPException, status, Depends, Query, BackgroundTasks # NEW: Import BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel

# Import your SQLAlchemy ORM models, Pydantic schemas, and database setup
import models
import schemas
from database import SessionLocal, create_db_and_tables # No need to import 'engine' here
import crud 
import lyrics_fetcher
import mock_enrichment_service # NEW: Import the mock enrichment service

# Configure logging for better visibility across modules
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



# Initialize FastAPI application with metadata
app = FastAPI(
    title="Music Catalog API (Persistent Data)",
    description="A CRUD API for managing a music catalog with persistent SQLite storage using SQLAlchemy.",
    version="2.0.0", # Updated version for database integration
)

 #Create the database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables() # Ensure tables exist, including new metadata columns

# --- Database Dependency ---
# This function provides a database session for each request.
# It ensures the session is properly closed after the request is finished.
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal() # Get a new session from the session factory
    try:
        yield db # Yield the session to the endpoint function
    finally:
        db.close() # Close the session after the request is processed
# --- NEW: Pydantic Schema for Lyrics Response ---
class LyricsResponse(BaseModel):
    title: str
    artist: str
    lyrics: str


# --- API Endpoints (now using database sessions) ---
# --- NEW: Background Task for Metadata Enrichment ---
async def enrich_song_metadata_task(song_id: int, db: Session):
    """
    Background task to fetch and store enriched metadata for a song.
    This function runs asynchronously in the background after the API response is sent.
    """
    logger.info(f"Background task started: Enriching metadata for song ID: {song_id}")
    
    # 1. Retrieve song details from the database
    song_from_db = crud.get_song_by_id(db, song_id)
    if not song_from_db:
        logger.error(f"Background task: Song with ID {song_id} not found in DB. Cannot enrich metadata.")
        return

    # 2. Call the mock external service to fetch metadata
    # Pass title and artist from the song retrieved from DB
    enriched_data = await mock_enrichment_service.fetch_mock_metadata(
        song_id=song_from_db.id,
        title=song_from_db.title,
        artist=song_from_db.artist
    )

    if enriched_data:
        # 3. Store the enriched metadata in the database
        updated_song = crud.update_song_metadata(db, song_id, enriched_data)
        if updated_song:
            logger.info(f"Background task: Successfully enriched and updated metadata for song ID: {song_id}")
        else:
            logger.error(f"Background task: Failed to update metadata for song ID: {song_id} in DB.")
    else:
        logger.warning(f"Background task: No metadata found from mock service for song ID: {song_id}")

# CREATE Operation: Add a new song
@app.post("/songs/", response_model=schemas.Song, status_code=status.HTTP_201_CREATED, summary="Add a new song to the catalog")
async def create_song_endpoint(song_data: schemas.SongCreate, db: Session = Depends(get_db)):
    new_song = crud.create_new_song(db=db, song_data=song_data)
    if new_song is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Song with ID {song_data.id} already exists. Please use a different ID or omit it for auto-assignment."
        )
    return new_song

# READ Operation: Retrieve all songs (with pagination)
@app.get("/songs/", response_model=List[schemas.Song], summary="Retrieve all songs in the catalog with pagination")
async def read_all_songs_endpoint(
    skip: int = Query(0, ge=0, description="Number of items to skip (for pagination)"),
    limit: int = Query(100, gt=0, le=1000, description="Maximum number of items to return (for pagination)"),
    db: Session = Depends(get_db)
):
    """
    Retrieves a list of all songs currently in the catalog, with optional pagination.
    """
    return crud.get_all_songs(db=db, skip=skip, limit=limit)

# READ Operation: Retrieve a single song by ID (will now include enriched metadata)
@app.get("/songs/{song_id}", response_model=schemas.Song, summary="Retrieve a single song by its ID")
async def read_song_by_id_endpoint(song_id: int, db: Session = Depends(get_db)):
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

# --- NEW: Lyrics Fetcher Endpoint ---
@app.get("/lyrics", response_model=LyricsResponse, summary="Fetch lyrics for a song")
async def get_lyrics_endpoint(
    song: str = Query(..., description="The title of the song."),
    artist: str = Query(..., description="The artist of the song.")
):
    """
    Fetches lyrics for a given song and artist from an external API.
    Results are cached for 10 minutes.

    Args:
        song (str): The title of the song.
        artist (str): The artist of the song.

    Returns:
        LyricsResponse: An object containing the song title, artist, and lyrics.

    Raises:
        HTTPException:
            - 404 Not Found: If lyrics cannot be found for the specified song and artist.
            - 500 Internal Server Error: If there's an issue with the external lyrics API or caching.
    """
    lyrics = lyrics_fetcher.fetch_lyrics(artist=artist, title=song)

    if lyrics is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lyrics not found for '{song}' by '{artist}'."
        )
    
    return LyricsResponse(title=song, artist=artist, lyrics=lyrics)

# --- NEW: Metadata Enrichment Endpoint ---
@app.post("/enrich-metadata", status_code=status.HTTP_202_ACCEPTED, summary="Trigger asynchronous metadata enrichment for a song")
async def enrich_metadata_endpoint(
    song_enrichment_request: schemas.SongEnrichmentRequest,
    background_tasks: BackgroundTasks, # FastAPI's dependency for background tasks
    db: Session = Depends(get_db)
):
    """
    Triggers an asynchronous background task to fetch and enrich metadata for a song.
    The API immediately returns a 202 Accepted response, and the enrichment
    process happens in the background.

    Args:
        song_enrichment_request (schemas.SongEnrichmentRequest): Contains the song_id to enrich.
        background_tasks (BackgroundTasks): FastAPI's dependency to add background tasks.
        db (Session): Database session.

    Returns:
        Dict: A message indicating the enrichment task has been queued.

    Raises:
        HTTPException: 404 Not Found if the song_id does not exist.
    """
    song_id = song_enrichment_request.song_id

    # Check if the song exists before queuing the background task
    existing_song = crud.get_song_by_id(db, song_id)
    if not existing_song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Song with ID {song_id} not found. Cannot queue enrichment."
        )

    # Add the enrichment task to FastAPI's background tasks.
    # We pass a new DB session to the background task to ensure it has its own session.
    # This is crucial because the main request's DB session will be closed after the response.
    background_tasks.add_task(enrich_song_metadata_task, song_id, SessionLocal())

    logger.info(f"Metadata enrichment task for song ID {song_id} queued.")
    return {"message": f"Metadata enrichment for song ID {song_id} has been queued."}

