from typing import List, Optional
from fastapi import FastAPI, HTTPException, status

# In main.py
import crud 
from models import Song, SongCreate, SongUpdate 

# Initialize FastAPI application with metadata for Swagger UI
app = FastAPI(
    title="Music Catalog API",
    description="A simple CRUD API for managing a music catalog using in-memory storage.",
    version="1.0.0",
)

# --- API Endpoints ---

# CREATE Operation: Add a new song
@app.post("/songs/", response_model=Song, status_code=status.HTTP_201_CREATED, summary="Add a new song to the catalog")
async def create_song_endpoint(song_data: SongCreate):
  
    new_song = crud.create_new_song(song_data)
    if new_song is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Song with ID {song_data.id} already exists. Please use a different ID or omit it for auto-assignment."
        )
    return new_song

# READ Operation: Retrieve all songs
@app.get("/songs/", response_model=List[Song], summary="Retrieve all songs in the catalog")
async def read_all_songs_endpoint():
    """
    Retrieves a list of all songs currently in the catalog.
    """
    return crud.get_all_songs()

# READ Operation: Retrieve a single song by ID
@app.get("/songs/{song_id}", response_model=Song, summary="Retrieve a single song by its ID")
async def read_song_by_id_endpoint(song_id: int):
 
    song = crud.get_song_by_id(song_id)
    if song is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Song with ID {song_id} not found")
    return song

# UPDATE Operation: Fully replace an existing song by ID
@app.put("/songs/{song_id}", response_model=Song, summary="Fully update an existing song by ID")
async def update_song_endpoint(song_id: int, updated_song_data: Song):
  
    # Ensure the ID in the URL path matches the ID in the request body for a PUT operation
    if updated_song_data.id != song_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Song ID in URL ({song_id}) does not match ID in request body ({updated_song_data.id}). For a PUT operation, these must match."
        )

    updated_song = crud.update_existing_song(song_id, updated_song_data)
    if updated_song is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Song with ID {song_id} not found")
    return updated_song

# UPDATE Operation: Partially update an existing song by ID (PATCH)
@app.patch("/songs/{song_id}", response_model=Song, summary="Partially update an existing song by ID")
async def patch_song_endpoint(song_id: int, song_update_data: SongUpdate):
   
    updated_song = crud.patch_existing_song(song_id, song_update_data)
    if updated_song is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Song with ID {song_id} not found")
    return updated_song


# DELETE Operation: Remove a song by ID
@app.delete("/songs/{song_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a song by its ID")
async def delete_song_endpoint(song_id: int):
   
    deleted = crud.delete_song_by_id(song_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Song with ID {song_id} not found")
    return {} # Return empty dict for 204 No Content
