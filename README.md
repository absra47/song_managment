Simple FastAPI CRUD API
This repository contains a basic demonstration of a Create, Read, Update, and Delete (CRUD) API built with FastAPI. It uses an in-memory list to simulate a database, showcasing fundamental API operations.

Features
FastAPI Framework: Leverages FastAPI for building robust and high-performance APIs.
Pydantic Models: Utilizes Pydantic for data validation and serialization/deserialization of request and response bodies.
In-Memory "Database": A simple Python list acts as a temporary data store for demonstration purposes.
CRUD Operations:
GET /items: Retrieve all items.
POST /items: Create a new item.
PUT /items/{item_id}: Update an existing item by its ID.
DELETE /items/{item_id}: Delete an item by its ID.
HTTP Status Codes: Correctly uses HTTP status codes (e.g., 201 Created, 204 No Content, 404 Not Found).
Error Handling: Implements basic error handling for non-existent items using HTTPException.
Installation
Clone the repository:

Bash

git clone <repository_url>
cd <repository_name>
Create a virtual environment (recommended):

Bash

python -m venv venv
source venv/bin/activate # On Windows, use `venv\Scripts\activate`
Install the dependencies:

Bash

pip install "fastapi[all]"
How to Run
Start the FastAPI application:

Bash

uvicorn main:app --reload
(Assuming your code is in a file named main.py)

The --reload flag will automatically restart the server whenever you make changes to the code.

Access the API documentation:

Once the server is running, you can access the interactive API documentation (powered by Swagger UI) at:
http://127.0.0.1:8000/docs

Alternatively, you can view the ReDoc documentation at:
http://127.0.0.1:8000/redoc

API Endpoints
Here's a quick overview of the available endpoints and how to interact with them:

Get All Items
URL: /items
Method: GET
Response: 200 OK and a list of Item objects.
JSON

[
{
"id": 0,
"name": "Laptop",
"price": 1200.0
},
{
"id": 1,
"name": "Mouse",
"price": 25.0
}
]
Create an Item
URL: /items
Method: POST
Request Body: Item object (JSON)
Response: 201 Created and the created Item object.
Example Request Body:

JSON

{
"id": 0,
"name": "Laptop",
"price": 1200.0
}
Example Response:

JSON

{
"id": 0,
"name": "Laptop",
"price": 1200.0
}
Update an Item
URL: /items/{item_id}
Method: PUT
Path Parameter: item_id (integer)
Request Body: Item object (JSON)
Response: 200 OK and the updated Item object.
Example Request Body (for PUT /items/0):

JSON

{
"id": 0,
"name": "Gaming Laptop",
"price": 1500.0
}
Example Response:

JSON

{
"id": 0,
"name": "Gaming Laptop",
"price": 1500.0
}
Error Response (Item Not Found):

JSON

{
"detail": "Item not found"
}
Delete an Item
URL: /items/{item_id}
Method: DELETE
Path Parameter: item_id (integer)
Response: 204 No Content (no response body).
Error Response (Item Not Found):

JSON

{
"detail": "Item not found"
}
