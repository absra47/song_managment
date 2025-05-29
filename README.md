Music Catalog API
This is a FastAPI application designed to manage a personal music collection. It allows you to perform Create, Read, Update, and Delete (CRUD) operations on songs, now with persistent data storage, advanced search capabilities, external lyrics fetching, and asynchronous metadata enrichment.

🚀 Project Stages Completed
Stage 1: Basic CRUD API (Completed!)
Initial setup with FastAPI and in-memory storage.

Implemented core CRUD operations for songs.

Stage 2: Persistent Data & Enhanced Search (Completed!)
Elevated the API from an in-memory demonstration to a robust application with durable data storage.

Integrated SQLite database and SQLAlchemy ORM for persistent storage.

Introduced a comprehensive song search endpoint (GET /songs/search/) with filtering by title, artist, album, genre, release_year.

Added pagination (skip, limit) to search results.

Stage 3: External Integration - Lyrics Fetcher (Completed!)
Introduced the ability to fetch song lyrics from an external API (lyrics.ovh).

Implemented an in-memory TTL cache (cachetools) for lyrics results to improve performance and reduce external API calls.

Ensured graceful handling of external API responses and clear error messages.

Stage 4: Scalable Architecture - Metadata Enrichment (Completed!)
Implemented an asynchronous service to enrich song data with additional metadata (e.g., BPM, mood, enriched genre).

Added an endpoint (POST /enrich-metadata) that triggers a background task (using FastAPI's BackgroundTasks) to call a mock external service.

Enriched metadata is stored persistently in the database.

The main song retrieval endpoints (GET /songs/, GET /songs/{song_id}) now return the enriched metadata.

Pagination has been added to the main GET /songs/ endpoint.

💡 Features
FastAPI Framework: Robust and high-performance web APIs.

Pydantic Models: Data validation and serialization/deserialization.

SQLAlchemy ORM: Seamless interaction with SQLite database.

Persistent Data: Song data stored in sql_app.db (SQLite).

Comprehensive CRUD Operations: POST, GET, PUT, PATCH, DELETE for songs.

Advanced Search Functionality: Filter songs by title, artist, album, genre, release_year.

Pagination: Control results with skip and limit parameters.

External Lyrics Integration: Fetch lyrics from lyrics.ovh.

In-Memory Caching: Cache lyrics results for 10 minutes.

Asynchronous Metadata Enrichment: Background tasks for non-blocking data enrichment.

Enriched Metadata: Store and retrieve bpm, mood, enriched_genre for songs.

HTTP Status Codes: Appropriate responses for clear communication.

Error Handling: Meaningful responses for various scenarios.

🛠️ Setup and Installation
Follow these steps to get the project up and running on your local machine.

Prerequisites
Python 3.12+ (or the specific Python version you used for venv creation)

pip (Python package installer)

(Optional, but recommended for database inspection) DB Browser for SQLite: https://sqlitebrowser.org/dl/

1. Clone the Repository
   If you haven't already, clone the project repository:

git clone https://github.com/absra47/song_managment.git
cd song_managment # Or adjust to your project's root directory name

2. Create and Activate Virtual Environment
   It's highly recommended to use a virtual environment to manage dependencies:

python3.12 -m venv venv # Creates a virtual environment named 'venv'
source venv/bin/activate # Activates the virtual environment

# On Windows, use `.\venv\Scripts\activate.bat` (Command Prompt) or `.\venv\Scripts\activate.ps1` (PowerShell)

3. Install Dependencies
   Install all the necessary Python packages. These are listed in requirements.txt:

pip install -r requirements.txt

(If you don't have requirements.txt generated yet, you can run: pip install fastapi "uvicorn[standard]" sqlalchemy python-dotenv requests cachetools)

4. Database Setup
   The application uses an SQLite database. It will be created automatically on startup.

Environment Variables: Create a new file named .env in the root of your project directory (the same level as main.py).

Add the following line to it:

DATABASE_URL="sqlite:///./sql_app.db"

This line tells the application the connection string for your SQLite database file.

🚀 How to Run
Once setup is complete, you can start the FastAPI server:

Ensure your virtual environment is activated.

Run the application:

uvicorn main:app --reload

The --reload flag is useful during development, as it automatically restarts the server whenever you save changes to your code.

Access the API Documentation:
Once the server is running, you can interact with your API through the interactive documentation (powered by Swagger UI) at:
http://127.0.0.1:8000/docs

Alternatively, you can view the ReDoc documentation at:
http://127.0.0.1:8000/redoc

📚 API Endpoints and Usage
Here's a quick overview of the available endpoints and how to interact with your music catalog. For detailed examples, refer to the interactive documentation (Swagger UI).

1. Create a Song
   URL: /songs/

Method: POST

Description: Adds a new song record to the database. The id is auto-generated.

Example Body:

{
"title": "Bohemian Rhapsody",
"artist": "Queen",
"album": "A Night at the Opera",
"genre": "Rock",
"release_year": 1975
}

2. Get All Songs
   URL: /songs/

Method: GET

Description: Retrieves a list of all songs stored in the database. Supports pagination.

Query Parameters:

skip: Number of records to skip (for pagination, default 0).

limit: Maximum number of records to return (for pagination, default 100).

Example: http://127.0.0.1:8000/songs/?skip=0&limit=10

3. Get a Song by ID
   URL: /songs/{song_id}

Method: GET

Path Parameter: song_id (integer)

Description: Fetches a specific song by its unique ID, including any enriched metadata.

Example: http://127.0.0.1:8000/songs/1

4. Search Songs
   URL: /songs/search/

Method: GET

Description: Searches for songs based on optional criteria.

Query Parameters: title, artist, album, genre, release_year, skip, limit.

Examples:

Search by artist and year: http://127.0.0.1:8000/songs/search?artist=Drake&release_year=2020

Search by title and genre: http://127.0.0.1:8000/songs/search?title=Bohemian&genre=Rock

5. Update a Song (Full Replacement)
   URL: /songs/{song_id}

Method: PUT

Path Parameter: song_id (integer)

Description: Fully replaces an existing song's data. Requires all fields in the request body (including optional metadata fields if you want to clear them or set them manually).

Example Request Body (for PUT /songs/1):

{
"id": 1,
"title": "Bohemian Rhapsody (Remastered)",
"artist": "Queen",
"album": "A Night at the Opera (Deluxe Edition)",
"genre": "Classic Rock",
"release_year": 1975,
"bpm": 144,
"mood": "Epic",
"enriched_genre": "Progressive Rock"
}

6. Partially Update a Song
   URL: /songs/{song_id}

Method: PATCH

Path Parameter: song_id (integer)

Description: Partially updates an existing song's attributes. Provide only the fields you wish to change.

Example Request Body (for PATCH /songs/2):

{
"genre": "Funk/Pop",
"release_year": 1983,
"mood": "Groovy"
}

7. Delete a Song
   URL: /songs/{song_id}

Method: DELETE

Path Parameter: song_id (integer)

Description: Removes a song from the catalog.

Response: 204 No Content on success.

8. Fetch Song Lyrics
   URL: /lyrics

Method: GET

Description: Fetches lyrics for a given song and artist. Results are cached for 10 minutes.

Query Parameters: song, artist.

Examples:

http://127.0.0.1:8000/lyrics?song=Imagine&artist=John%20Lennon

9. Trigger Metadata Enrichment
   URL: /enrich-metadata

Method: POST

Description: Triggers an asynchronous background task to fetch and enrich metadata (BPM, mood, enriched genre) for a specified song. The API responds immediately.

Request Body:

{
"song_id": 1
}

Response: 202 Accepted and a message indicating the task was queued. Check server logs for enrichment progress.

👩‍💻 Development
Project Structure
.
├── main.py # FastAPI application setup and API endpoints
├── crud.py # CRUD (Create, Read, Update, Delete) operations using SQLAlchemy
├── models.py # SQLAlchemy ORM models (defines database tables)
├── schemas.py # Pydantic models for request/response data validation
├── database.py # SQLAlchemy database connection and session management
├── lyrics_fetcher.py # Logic for fetching and caching song lyrics
├── mock_enrichment_service.py # Mock external service for metadata enrichment
├── .env # Environment variables (e.g., DATABASE_URL)
├── requirements.txt # Project dependencies
└── README.md # This documentation file
