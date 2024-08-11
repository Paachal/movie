
from pydantic import BaseModel
from typing import Optional

class MovieCreate(BaseModel):
    title: str
    description: str
    rating: float
    year: int

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    year: Optional[int] = None
