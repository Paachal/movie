from motor.motor_asyncio import AsyncIOMotorClient
import os

# Fetch the MONGO_URL from the environment variables
MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise ValueError("No MONGO_URL environment variable set")

# Create a MongoDB client
client = AsyncIOMotorClient(MONGO_URL)

# Get the database instance
db = client.get_database("moviesdb")

