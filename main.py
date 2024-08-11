from fastapi import FastAPI, HTTPException, Depends
from pymongo import MongoClient
import os

app = FastAPI()

# Get the MongoDB connection string from the environment variable
MONGO_URL = os.getenv("MONGO_URL")
if not MONGO_URL:
    raise ValueError("No MONGO_URL environment variable set")

# Connect to the MongoDB client
client = MongoClient(MONGO_URL)
db = client["moviesdb"]  # Access the movies database

@app.get("/")
def read_root():
    return {"message": "Welcome to the Movie API"}

# Endpoint to create a new movie
@app.post("/movies/")
def create_movie(movie: dict):
    movie_id = db["movies"].insert_one(movie).inserted_id
    return {"movie_id": str(movie_id)}

# Endpoint to get a movie by its ID
@app.get("/movies/{movie_id}")
def get_movie(movie_id: str):
    movie = db["movies"].find_one({"_id": movie_id})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

# Endpoint to get all movies
@app.get("/movies/")
def get_movies():
    movies = db["movies"].find()
    return list(movies)

# Endpoint to update a movie by its ID
@app.put("/movies/{movie_id}")
def update_movie(movie_id: str, movie: dict):
    result = db["movies"].update_one({"_id": movie_id}, {"$set": movie})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie updated successfully"}

# Endpoint to delete a movie by its ID
@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: str):
    result = db["movies"].delete_one({"_id": movie_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted successfully"}
