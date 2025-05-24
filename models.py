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

    # This __repr__ method is useful for debugging, helps in printing objects.
    def __repr__(self):
        return (f"<Song(id={self.id}, title='{self.title}', artist='{self.artist}', "
                f"album='{self.album}', genre='{self.genre}', release_year={self.release_year})>")
