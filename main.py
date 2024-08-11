from fastapi import FastAPI, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

# MongoDB connection
MONGO_URL = "your_mongodb_connection_string_here"
client = AsyncIOMotorClient(MONGO_URL)
db = client.moviesdb

# Pydantic models
class MovieBase(BaseModel):
    title: str
    director: str
    rating: float

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: str = Field(default_factory=str)

# Dependency to get the database
async def get_db():
    return db

# Create a new movie
@app.post("/movies/", response_model=Movie)
async def create_movie(movie: MovieCreate, db = Depends(get_db)):
    movie_dict = movie.dict()
    result = await db.movies.insert_one(movie_dict)
    movie_dict["_id"] = str(result.inserted_id)
    return Movie(**movie_dict)

# Read a movie by its ID
@app.get("/movies/{movie_id}", response_model=Movie)
async def read_movie(movie_id: str, db = Depends(get_db)):
    movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return Movie(id=str(movie["_id"]), **movie)

# Read all movies
@app.get("/movies/", response_model=List[Movie])
async def read_movies(skip: int = 0, limit: int = 10, db = Depends(get_db)):
    movies = await db.movies.find().skip(skip).limit(limit).to_list(length=limit)
    return [Movie(id=str(movie["_id"]), **movie) for movie in movies]


@app.put("/movies/{movie_id}", response_model=Movie)
async def update_movie(movie_id: str, movie: MovieCreate, db = Depends(get_db)):
    result = await db.movies.update_one({"_id": ObjectId(movie_id)}, {"$set": movie.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    updated_movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
    return Movie(id=str(updated_movie["_id"]), **updated_movie)

# Delete a movie
@app.delete("/movies/{movie_id}", response_model=Movie)
async def delete_movie(movie_id: str, db = Depends(get_db)):
    result = await db.movies.delete_one({"_id": ObjectId(movie_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted successfully"}
