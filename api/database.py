
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise ValueError("No MONGO_URL environment variable set")

client = AsyncIOMotorClient(MONGO_URL)
db = client.get_database("moviesdb")
