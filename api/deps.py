# app/deps.py
from fastapi import Depends, HTTPException
from .crud import get_movie

async def get_movie_by_id(id: str = None):
    movie = await get_movie(id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie
