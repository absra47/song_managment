import asyncio
import random
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Mock data for enrichment based on song title/artist
MOCK_METADATA_DB = {
    ("bohemian rhapsody", "queen"): {
        "bpm": 144,
        "mood": "Epic",
        "enriched_genre": "Progressive Rock"
    },
    ("imagine", "john lennon"): {
        "bpm": 75,
        "mood": "Peaceful",
        "enriched_genre": "Soft Rock"
    },
    ("shape of my heart", "sting"): {
        "bpm": 90,
        "mood": "Melancholic",
        "enriched_genre": "Acoustic Pop"
    },
    ("billie jean", "michael jackson"): {
        "bpm": 117,
        "mood": "Funky",
        "enriched_genre": "Pop/R&B"
    }
    # Add more mock data as needed for testing
}

async def fetch_mock_metadata(song_id: int, title: str, artist: str) -> Optional[Dict[str, Any]]:
    """
    Simulates fetching enriched metadata from an external service.
    Introduces a random delay to mimic network latency.

    Args:
        song_id (int): The ID of the song.
        title (str): The title of the song.
        artist (str): The artist of the song.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing enriched metadata
                                   (e.g., bpm, mood, enriched_genre) or None if not found.
    """
    logger.info(f"Mock service: Fetching metadata for song_id={song_id}, title='{title}', artist='{artist}'")

    # Simulate network latency
    await asyncio.sleep(random.uniform(2, 5)) # Simulate 2-5 seconds delay

    # Normalize for lookup
    normalized_title = title.strip().lower()
    normalized_artist = artist.strip().lower()

    # Simulate finding metadata
    metadata = MOCK_METADATA_DB.get((normalized_title, normalized_artist))

    if metadata:
        logger.info(f"Mock service: Metadata found for '{title}' by '{artist}'.")
        return metadata
    else:
        logger.warning(f"Mock service: No mock metadata found for '{title}' by '{artist}'.")
        return None

