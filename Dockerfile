# Use an official Python runtime as a parent image
FROM python:3.12-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Install system dependencies needed for some Python packages (like sqlite3-dev for pysqlite3)
# The -dev package for sqlite3 ensures the header files are present for building Python modules.
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    libsqlite3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's source code into the container at /app
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 8000

# Define environment variables (DB_URL needs to be accessible in the container)
ENV DATABASE_URL="sqlite:///./sql_app.db"

# Command to run the application using Uvicorn
# --host 0.0.0.0 makes the app accessible from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]