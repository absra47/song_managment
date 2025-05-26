# Music Catalog API

This is a FastAPI application designed to manage a personal music collection. It allows you to perform **Create, Read, Update, and Delete (CRUD)** operations on songs, now with **persistent data storage**, **advanced search capabilities**, and **external lyrics fetching**.

---

## 🚀 Stage 2: Persistent Data & Enhanced Search (Completed!)

This stage significantly elevates the API from an in-memory demonstration to a robust application with durable data storage and powerful filtering.

### ✨ Key Enhancements:

- **Persistent Data Storage:** Song records are now stored reliably in an **SQLite database** (`sql_app.db`) using **SQLAlchemy ORM**. Your data will no longer be lost when the server restarts!
- **Comprehensive Song Search:**
  - A new endpoint `GET /songs/search/` allows filtering by:
    - `title` (case-insensitive, partial match)
    - `artist` (case-insensitive, partial match)
    - `album` (case-insensitive, partial match)
    - `genre` (case-insensitive, partial match)
    - `release_year` (exact match)
  - Includes **pagination** via `skip` and `limit` query parameters for efficient result handling.
- **Full CRUD Operations:** All existing Create, Read, Update, and Delete operations now interact directly with the persistent database, ensuring data integrity.

---

## 🎤 Stage 3: External Integration - Lyrics Fetcher (Completed!)

This stage introduces the ability to fetch song lyrics from an external API, enhancing the utility of the music catalog. A robust caching mechanism is implemented to improve performance and reduce external API calls.

### ✨ Key Enhancements:

- **External Lyrics Fetching:**
  - New endpoint: `GET /lyrics`
  - Fetches lyrics for songs by title and artist from `lyrics.ovh`.
  - Handles various API response scenarios, including songs not found.
- **In-Memory Caching:** Lyrics results are cached for **10 minutes** using `cachetools` to reduce redundant external API calls and improve response times.
- **Graceful Error Handling:** Clear error responses are provided when lyrics cannot be found or if there are issues with the external API.

---

## 💡 Features

- **FastAPI Framework**: Built using FastAPI for creating robust and high-performance web APIs.
- **Pydantic Models**: Leverages Pydantic for powerful data validation and seamless serialization/deserialization of JSON request and response bodies.
- **SQLAlchemy ORM**: Utilizes SQLAlchemy for seamless interaction with the SQLite database, mapping Python objects to database tables.
- **Persistent Data**: Song data is stored in `sql_app.db` (SQLite), ensuring data is saved across application restarts.
- **Comprehensive CRUD Operations**:
  - `POST /songs`: Add a new song.
  - `GET /songs`: Retrieve all songs.
  - `GET /songs/{song_id}`: Fetch a specific song by its unique ID.
  - `PUT /songs/{song_id}`: Fully replace an existing song's data.
  - `PATCH /songs/{song_id}`: Partially update an existing song's attributes.
  - `DELETE /songs/{song_id}`: Remove a song from the catalog.
- **Advanced Search Functionality**: Search songs by multiple criteria with `GET /songs/search/`.
- **Pagination**: Control the number of results and offset using `skip` and `limit` parameters in search and retrieval.
- **External Lyrics Integration**: Fetch song lyrics from `lyrics.ovh` via a dedicated endpoint.
- **In-Memory Caching**: Improve performance by caching lyrics results for 10 minutes.
- **HTTP Status Codes**: Uses appropriate HTTP status codes (e.g., `201 Created`, `200 OK`, `204 No Content`, `400 Bad Request`, `404 Not Found`) for clear communication with clients.
- **Error Handling**: Implements basic error handling using `HTTPException` for scenarios like songs not found or invalid requests.

---

## 🛠️ Setup and Installation

Follow these steps to get the project up and running on your local machine.

### Prerequisites

- **Python 3.12+** (or the specific Python version you used for `venv` creation)
- `pip` (Python package installer)

### 1. Clone the Repository

If you haven't already, clone the project repository:

```bash
git clone https://github.com/absra47/song_managment.git  # Replace with your actual repository URL
cd song_managment # Or adjust to your project's root directory name
```

### 2. Create and Activate Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies:

```bash
python3.12 -m venv venv # Creates a virtual environment named 'venv'
source venv/bin/activate # Activates the virtual environment
# On Windows, use `.\venv\Scripts\activate.bat` (Command Prompt) or `.\venv\Scripts\activate.ps1` (PowerShell)
```

### 3. Install Dependencies

Install all the necessary Python packages. These are listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

_(If you don't have `requirements.txt` generated yet, ensure you install `requests` and `cachetools` along with the others):_

```bash
pip install fastapi "uvicorn[standard]" sqlalchemy python-dotenv requests cachetools
```

### 4. Database Setup

The application uses an SQLite database, which will be automatically created on startup.

- **Environment Variables:** Create a new file named **`.env`** in the root of your project directory (the same level as `main.py`).
- Add the following line to it:
  ```
  DATABASE_URL="sqlite:///./sql_app.db"
  ```
  This line tells the application the connection string for your SQLite database file.

---

## 🚀 How to Run

Once setup is complete, you can start the FastAPI server:

1.  **Ensure your virtual environment is activated.**
2.  **Run the application:**

    ```bash
    uvicorn main:app --reload
    ```

    The `--reload` flag is useful during development, as it automatically restarts the server whenever you save changes to your code.

3.  **Access the API Documentation:**
    Once the server is running, you can interact with your API through the interactive documentation (powered by **Swagger UI**) at:
    `http://127.0.0.1:8000/docs`

    Alternatively, you can view the ReDoc documentation at:
    `http://127.0.0.1:8000/redoc`

---

## 📚 API Endpoints and Usage

Here's a quick overview of the available endpoints and how to interact with your music catalog. For detailed examples, refer to the interactive documentation (Swagger UI).

### 1. Create a Song

- **URL**: `/songs/`
- **Method**: `POST`
- **Description**: Adds a new song record to the database. The `id` is auto-generated.
- **Example Body:**
  ```json
  {
    "title": "Bohemian Rhapsody",
    "artist": "Queen",
    "album": "A Night at the Opera",
    "genre": "Rock",
    "release_year": 1975
  }
  ```

### 2. Get All Songs

- **URL**: `/songs/`
- **Method**: `GET`
- **Description**: Retrieves a list of all songs stored in the database.
- **Example:** `http://127.0.0.1:8000/songs/`

### 3. Get a Song by ID

- **URL**: `/songs/{song_id}`
- **Method**: `GET`
- **Path Parameter**: `song_id` (integer)
- **Description**: Fetches a specific song by its unique ID.
- **Example:** `http://127.0.0.1:8000/songs/1`

### 4. Search Songs

- **URL**: `/songs/search/`
- **Method**: `GET`
- **Description**: Searches for songs based on optional criteria.
- **Query Parameters**: `title`, `artist`, `album`, `genre`, `release_year`, `skip`, `limit`.
- **Examples:**
  - Search by artist and year: `http://127.0.0.1:8000/songs/search?artist=Drake&release_year=2020`
  - Search by title and genre: `http://127.0.0.1:8000/songs/search?title=Bohemian&genre=Rock`
  - Get the next 10 results after the first 20 for 'Pop' songs: `http://17.0.0.1:8000/songs/search?genre=Pop&skip=20&limit=10`

### 5. Update a Song (Full Replacement)

- **URL**: `/songs/{song_id}`
- **Method**: `PUT`
- **Path Parameter**: `song_id` (integer)
- **Description**: Fully replaces an existing song's data. Requires all fields in the request body.
- **Example Request Body (for PUT /songs/1):**
  ```json
  {
    "id": 1,
    "title": "Bohemian Rhapsody (Remastered)",
    "artist": "Queen",
    "album": "A Night at the Opera (Deluxe Edition)",
    "genre": "Classic Rock",
    "release_year": 1975
  }
  ```

### 6. Partially Update a Song

- **URL**: `/songs/{song_id}`
- **Method**: `PATCH`
- **Path Parameter**: `song_id` (integer)
- **Description**: Partially updates an existing song's attributes. Provide only the fields you wish to change.
- **Example Request Body (for PATCH /songs/2):**
  ```json
  {
    "genre": "Funk/Pop",
    "release_year": 1983
  }
  ```

### 7. Delete a Song

- **URL**: `/songs/{song_id}`
- **Method**: `DELETE`
- **Path Parameter**: `song_id` (integer)
- **Description**: Removes a song from the catalog.
- **Response**: `204 No Content` on success.

### 8. Fetch Song Lyrics

- **URL**: `/lyrics`
- **Method**: `GET`
- **Description**: Fetches lyrics for a given song and artist. Results are cached for 10 minutes.
- **Query Parameters**:
  - `song`: The title of the song (required).
  - `artist`: The artist of the song (required).
- **Examples:**
  - Fetch lyrics for "Imagine" by "John Lennon": `http://127.0.0.1:8000/lyrics?song=Imagine&artist=John%20Lennon`
  - Fetch lyrics for "Bohemian Rhapsody" by "Queen": `http://127.0.0.1:8000/lyrics?song=Bohemian%20Rhapsody&artist=Queen`

---

## 👩‍💻 Development

### Project Structure

```
.
├── main.py             # FastAPI application setup and API endpoints
├── crud.py             # CRUD (Create, Read, Update, Delete) operations using SQLAlchemy
├── models.py           # SQLAlchemy ORM models (defines database tables)
├── schemas.py          # Pydantic models for request/response data validation
├── database.py         # SQLAlchemy database connection and session management
├── lyrics_fetcher.py   # Logic for fetching and caching song lyrics
├── .env                # Environment variables (e.g., DATABASE_URL)
├── requirements.txt    # Project dependencies
└── README.md           # This documentation file
```

```

```
