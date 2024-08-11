from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import os

# Secret key to encode the JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Fetch the MONGO_URL from the environment variables
MONGO_URL = os.getenv("MONGO_URL")
if not MONGO_URL:
    raise ValueError("No MONGO_URL environment variable set")

# Create a MongoDB client
client = AsyncIOMotorClient(MONGO_URL)
db = client.get_database("moviesdb")

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    password: str

class Movie(BaseModel):
    title: str
    description: str

class MovieCreate(Movie):
    pass

class MovieInDB(Movie):
    id: str

# Utility functions for password handling
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user(db, username: str):
    user = await db["users"].find_one({"username": username})
    if user:
        return UserInDB(**user)

async def create_user(db, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    user_dict = {"username": user.username, "hashed_password": hashed_password}
    await db["users"].insert_one(user_dict)
    return UserInDB(**user_dict)

async def authenticate_user(db, username: str, password: str):
    user = await get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# FastAPI app
app = FastAPI()

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=User)
async def create_user_endpoint(user: UserCreate):
    existing_user = await get_user(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await create_user(db, user)

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/movies/", response_model=Movie)
async def create_movie(movie: MovieCreate, current_user: User = Depends(get_current_user)):
    movie_dict = movie.dict()
    result = await db["movies"].insert_one(movie_dict)
    movie_in_db = MovieInDB(id=str(result.inserted_id), **movie_dict)
    return movie_in_db

@app.get("/movies/", response_model=list[Movie])
async def read_movies(skip: int = 0, limit: int = 10, current_user: User = Depends(get_current_user)):
    movies = await db["movies"].find().skip(skip).limit(limit).to_list(length=limit)
    return movies

@app.get("/movies/{movie_id}", response_model=Movie)
async def read_movie(movie_id: str, current_user: User = Depends(get_current_user)):
    movie = await db["movies"].find_one({"_id": movie_id})
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return MovieInDB(id=str(movie["_id"]), **movie)

@app.put("/movies/{movie_id}", response_model=Movie)
async def update_movie(movie_id: str, movie: MovieCreate, current_user: User = Depends(get_current_user)):
    result = await db["movies"].update_one({"_id": movie_id}, {"$set": movie.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    return MovieInDB(id=movie_id, **movie.dict())

@app.delete("/movies/{movie_id}", response_model=dict)
async def delete_movie(movie_id: str, current_user: User = Depends(get_current_user)):
    result = await db["movies"].delete_one({"_id": movie_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"message": "Movie deleted successfully"}

@app.get("/")
async def root():
    return {"message": "Welcome to the Movie API"}
