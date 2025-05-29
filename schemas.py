from typing import Optional
from pydantic import BaseModel,ConfigDict

# Base Song model: defines the complete structure of a song
class Song(BaseModel):
    id: int
    title: str
    artist: str
    album: str
    genre: str
    release_year: int
    bpm: Optional[int] = None
    mood: Optional[str] = None
    enriched_genre: Optional[str] = None
    
 # --- Pydantic V2 Configuration ---
    model_config = ConfigDict(from_attributes=True) 
# Model for creating a song: 'id' is optional as it might be assigned by the server
class SongCreate(BaseModel):
    id: Optional[int] = None # Allow client to provide ID, or server generates
    title: str
    artist: str
    album: str
    genre: str
    release_year: int

# Model for updating a song: all fields are optional for partial updates (PATCH)
class SongUpdate(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    genre: Optional[str] = None
    release_year: Optional[int] = None

# --- NEW: Schema for Metadata Enrichment Request ---
class SongEnrichmentRequest(BaseModel):
    song_id: int
    # You might add other fields if the mock service needs them, e.g., title, artist
    # title: str
    # artist: str
