# app/routes.py
from fastapi import APIRouter, Depends
from .schemas import MovieCreate, MovieUpdate
from .crud import create_movie, get_movie, update_movie, delete_movie
from .deps import get_movie_by_id

router = APIRouter()

@router.post("/movies/", response_model=Movie)
async def create_new_movie(movie: MovieCreate):
    movie_data = movie.dict()
    return await create_movie(movie_data)

@router.get("/movies/{id}/", response_model=Movie)
async def read_movie(id: str, movie=Depends(get_movie_by_id)):
    return movie

@router.put("/movies/{id}/", response_model=Movie)
async def update_existing_movie(id: str, movie_update: MovieUpdate, movie=Depends(get_movie_by_id)):
    updated_data = movie_update.dict(exclude_unset=True)
    return await update_movie(id, updated_data)

@router.delete("/movies/{id}/")
async def delete_existing_movie(id: str, movie=Depends(get_movie_by_id)):
    delete_count = await delete_movie(id)
    if delete_count:
        return {"msg": "Movie deleted"}
    raise HTTPException(status_code=404, detail="Movie not found")
