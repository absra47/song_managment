from typing import Optional
from pydantic import BaseModel

# Base Song model: defines the complete structure of a song
class Song(BaseModel):
    id: int
    title: str
    artist: str
    album: str
    genre: str
    release_year: int

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
