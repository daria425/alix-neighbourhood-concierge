import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
load_dotenv()
MONGO_URI=os.getenv("MONGO_URI")
DB_NAME=os.getenv("DB_NAME")

class DatabaseConnection:
    _instance=None
    def __new__(cls, *args, **kwargs):
        """Ensure only one instance of MongoDB exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        """Initialize MongoDB connection attributes."""
        self.client: AsyncIOMotorClient | None = None
        self.db: AsyncIOMotorDatabase | None = None

    async def connect(self):
        if self.client is None:
            try:
                self.client=AsyncIOMotorClient(MONGO_URI)
                self.db = self.client[DB_NAME]
                print("Connected to MongoDB")
            except Exception as e:
                print(f"error connecting to MongoDB:{e}")
                raise

    async def close(self):
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()
            self.client = None
            print("❌ Disconnected from MongoDB")

db_connection=DatabaseConnection()