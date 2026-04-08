from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import certifi
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGO_DB_CONNECTION_URL")
DB_NAME = os.getenv("DB_NAME")

client = AsyncIOMotorClient(MONGODB_URL, tlsCAFile=certifi.where())
db = client[DB_NAME]