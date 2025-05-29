from sqlalchemy import Column, Integer, String
from database import Base # Import Base directly from database.py

# Define the SQLAlchemy ORM model for the 'songs' table
class Song(Base):
    __tablename__ = "songs" # Name of the table in the database

    id = Column(Integer, primary_key=True, index=True) # Primary key, indexed for quick lookups
    title = Column(String, index=True)
    artist = Column(String, index=True)
    album = Column(String, index=True)
    genre = Column(String)
    release_year = Column(Integer)

     # --- NEW: Enriched Metadata Fields ---
    # These fields are optional as not all songs will immediately have enriched data
    bpm = Column(Integer, nullable=True, default=None) # Beats Per Minute
    mood = Column(String, nullable=True, default=None) # e.g., "Energetic", "Relaxed"
    enriched_genre = Column(String, nullable=True, default=None) # e.g., "Pop-Rock", "Electro-Funk"
    # You can add more fields as needed, like 'instrumentation', 'vocal_type', etc.


    # This __repr__ method is useful for debugging, helps in printing objects.
    def __repr__(self):
        return (f"<Song(id={self.id}, title='{self.title}', artist='{self.artist}', "
                f"album='{self.album}', genre='{self.genre}', release_year={self.release_year})>")
