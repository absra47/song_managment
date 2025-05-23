# Music Catalog API

This repository showcases a simple **Create, Read, Update, and Delete (CRUD)** API built with **FastAPI**. It's designed to manage a collection of songs, using an in-memory list to simulate a database. This project is perfect for understanding fundamental API operations and project structure.

## Features

- **FastAPI Framework**: Built using FastAPI for creating robust and high-performance web APIs.
- **Pydantic Models**: Leverages Pydantic for powerful data validation and seamless serialization/deserialization of JSON request and response bodies, ensuring your data is always in the correct format.
- **In-Memory "Database"**: A straightforward Python list serves as a temporary data store for demonstration purposes. All data is reset when the server restarts.
- **CRUD Operations**: Provides a full suite of API endpoints for managing your song catalog:
  - `POST /songs`: Add a new song.
  - `GET /songs`: Retrieve all songs.
  - `GET /songs/{song_id}`: Fetch a specific song by its unique ID.
  - `PUT /songs/{song_id}`: Fully replace an existing song's data.
  - `PATCH /songs/{song_id}`: Partially update an existing song's attributes.
  - `DELETE /songs/{song_id}`: Remove a song from the catalog.
- **HTTP Status Codes**: Uses appropriate HTTP status codes (e.g., `201 Created`, `200 OK`, `204 No Content`, `400 Bad Request`, `404 Not Found`) for clear communication with clients.
- **Error Handling**: Implements basic error handling to provide meaningful responses for scenarios like songs not found or invalid requests using `HTTPException`.

---

## Installation

Getting this API up and running on your local machine is straightforward:

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Create a virtual environment** (highly recommended to manage project dependencies):

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate # On Windows, use `.\.venv\Scripts\activate.ps1` (PowerShell) or `.\.venv\Scripts\activate.bat` (Command Prompt)
    ```

3.  **Install the dependencies:**
    ```bash
    pip install fastapi uvicorn pydantic
    ```
    - _(Note: `fastapi[all]` is often used, but explicitly listing `fastapi`, `uvicorn`, and `pydantic` can be clearer for minimal setups.)_

---

## How to Run

1.  **Start the FastAPI application:**
    Ensure your virtual environment is activated, then run:

    ```bash
    uvicorn main:app --reload
    ```

    (This assumes your main application file is named `main.py` and your FastAPI app instance is named `app` within it.)

    The `--reload` flag is super handy during development, as it automatically restarts the server whenever you save changes to your code.

2.  **Access the API Documentation:**
    Once the server is running, you can interact with your API through the interactive documentation (powered by **Swagger UI**) at:
    `http://127.0.0.1:8000/docs`

    Alternatively, you can view the ReDoc documentation at:
    `http://127.0.0.1:8000/redoc`

---

## API Endpoints

Here's a quick overview of the available endpoints and how to interact with your music catalog:

### 1. Create a Song

- **URL**: `/songs/`
- **Method**: `POST`
- **Request Body**: A `Song` object (JSON) with `title`, `artist`, `album`, `genre`, and `release_year`. The `id` is optional; if omitted or `0`, the server will auto-assign one.
- **Response**: `201 Created` and the full `Song` object that was created.

**Example Request Body:**

```json
{
  "title": "Bohemian Rhapsody",
  "artist": "Queen",
  "album": "A Night at the Opera",
  "genre": "Rock",
  "release_year": 1975
}
```

**Example Response:**

```json
{
  "id": 1,
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
- **Response**: `200 OK` and a list of `Song` objects.

**Example Response:**

```json
[
  {
    "id": 1,
    "title": "Bohemian Rhapsody",
    "artist": "Queen",
    "album": "A Night at the Opera",
    "genre": "Rock",
    "release_year": 1975
  },
  {
    "id": 2,
    "title": "Billie Jean",
    "artist": "Michael Jackson",
    "album": "Thriller",
    "genre": "Pop",
    "release_year": 1982
  }
]
```

### 3. Get a Song by ID

- **URL**: `/songs/{song_id}`
- **Method**: `GET`
- **Path Parameter**: `song_id` (integer)
- **Response**: `200 OK` and the `Song` object.

**Example Response (for GET /songs/1):**

```json
{
  "id": 1,
  "title": "Bohemian Rhapsody",
  "artist": "Queen",
  "album": "A Night at the Opera",
  "genre": "Rock",
  "release_year": 1975
}
```

**Error Response (Song Not Found):**

```json
{
  "detail": "Song with ID 999 not found"
}
```

### 4. Update a Song (Full Replacement)

- **URL**: `/songs/{song_id}`
- **Method**: `PUT`
- **Path Parameter**: `song_id` (integer)
- **Request Body**: A complete `Song` object (JSON) with all fields. The `id` in the body **must** match the `song_id` in the URL.
- **Response**: `200 OK` and the updated `Song` object.

**Example Request Body (for PUT /songs/1):**

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

**Example Response:**

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

### 5. Partially Update a Song

- **URL**: `/songs/{song_id}`
- **Method**: `PATCH`
- **Path Parameter**: `song_id` (integer)
- **Request Body**: A partial `SongUpdate` object (JSON) containing only the fields you wish to change.
- **Response**: `200 OK` and the updated `Song` object.

**Example Request Body (for PATCH /songs/2):**

```json
{
  "genre": "Funk/Pop",
  "release_year": 1983
}
```

**Example Response (assuming original ID 2 was 'Billie Jean', artist 'Michael Jackson'):**

```json
{
  "id": 2,
  "title": "Billie Jean",
  "artist": "Michael Jackson",
  "album": "Thriller",
  "genre": "Funk/Pop",
  "release_year": 1983
}
```

### 6. Delete a Song

- **URL**: `/songs/{song_id}`
- **Method**: `DELETE`
- **Path Parameter**: `song_id` (integer)
- **Response**: `204 No Content` (meaning success, but no response body).

**Error Response (Song Not Found):**

```json
{
  "detail": "Song with ID 999 not found"
}
```

---
