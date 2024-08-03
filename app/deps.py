from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db
from .auth import get_current_user
from .models import User

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
