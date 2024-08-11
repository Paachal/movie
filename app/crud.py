# app/crud.py
from .models import Movie
from .database import db
from bson import ObjectId

async def create_movie(movie_data: dict) -> Movie:
    movie = await db["movies"].insert_one(movie_data)
    new_movie = await db["movies"].find_one({"_id": movie.inserted_id})
    return Movie(**new_movie)

async def get_movie(id: str) -> Movie:
    movie = await db["movies"].find_one({"_id": ObjectId(id)})
    if movie:
        return Movie(**movie)
    return None

async def update_movie(id: str, movie_data: dict) -> Movie:
    await db["movies"].update_one({"_id": ObjectId(id)}, {"$set": movie_data})
    updated_movie = await db["movies"].find_one({"_id": ObjectId(id)})
    if updated_movie:
        return Movie(**updated_movie)
    return None

async def delete_movie(id: str):
    result = await db["movies"].delete_one({"_id": ObjectId(id)})
    return result.deleted_count
