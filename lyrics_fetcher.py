import requests
from typing import Optional
from cachetools import TTLCache # Import Time-To-Live Cache
import logging

# Configure logging for better visibility
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Configuration ---
LYRICS_API_BASE_URL = "https://api.lyrics.ovh/v1" # Base URL for the external lyrics API
CACHE_TTL_SECONDS = 60 * 10 # Cache Time-To-Live: 10 minutes (60 seconds * 10)
CACHE_MAX_SIZE = 500        # Maximum number of items to store in the cache

# --- In-memory Cache Initialization ---
# TTLCache: A dictionary-like cache with a time-to-live (TTL) for each item.
# Items are automatically removed after their TTL expires.
lyrics_cache = TTLCache(maxsize=CACHE_MAX_SIZE, ttl=CACHE_TTL_SECONDS)

# --- Lyrics Fetching Function ---
def fetch_lyrics(artist: str, title: str) -> Optional[str]:
    """
    Fetches lyrics for a given song and artist from an external API,
    with results being cached for a specified duration.

    Args:
        artist (str): The artist's name.
        title (str): The song's title.

    Returns:
        Optional[str]: The lyrics string if found, otherwise None.
    """
    # Normalize artist and title for consistent caching and API calls
    # Convert to lowercase and remove leading/trailing whitespace
    normalized_artist = artist.strip().lower()
    normalized_title = title.strip().lower()

    # Create a cache key from normalized artist and title
    cache_key = f"{normalized_artist}-{normalized_title}"

    # 1. Check Cache First
    if cache_key in lyrics_cache:
        lyrics = lyrics_cache[cache_key]
        logger.info(f"Lyrics for '{title}' by '{artist}' found in cache.")
        return lyrics

    # 2. If Not in Cache, Fetch from External API
    logger.info(f"Fetching lyrics for '{title}' by '{artist}' from external API.")
    try:
        # Construct the API URL
        # URL format: https://api.lyrics.ovh/v1/{artist}/{title}
        # Encode artist and title to handle special characters in URLs
        api_url = f"{LYRICS_API_BASE_URL}/{requests.utils.quote(artist)}/{requests.utils.quote(title)}"
        
        response = requests.get(api_url, timeout=5) # Add a timeout to prevent hanging
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        data = response.json()

        # lyrics.ovh returns a 'lyrics' key if found, or an 'error' key if not found.
        if 'lyrics' in data:
            lyrics = data['lyrics']
            lyrics_cache[cache_key] = lyrics # Store lyrics in cache
            logger.info(f"Successfully fetched and cached lyrics for '{title}' by '{artist}'.")
            return lyrics
        elif 'error' in data:
            logger.warning(f"Lyrics not found for '{title}' by '{artist}': {data['error']}")
            return None # Lyrics not found for this song
        else:
            logger.error(f"Unexpected response format from lyrics API for '{title}' by '{artist}': {data}")
            return None

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            logger.warning(f"Lyrics not found (404) for '{title}' by '{artist}'.")
        else:
            logger.error(f"HTTP error fetching lyrics for '{title}' by '{artist}': {e}")
        return None
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error fetching lyrics for '{title}' by '{artist}': {e}")
        return None
    except requests.exceptions.Timeout as e:
        logger.error(f"Timeout fetching lyrics for '{title}' by '{artist}': {e}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"An unexpected request error occurred fetching lyrics for '{title}' by '{artist}': {e}")
        return None
    except ValueError as e: # For JSON decoding errors
        logger.error(f"JSON decoding error for lyrics API response for '{title}' by '{artist}': {e}")
        return None

