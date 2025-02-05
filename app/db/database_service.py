from app.db.database_connection import db_connection
import logging
class DatabaseService:
    """Base class to manage MongoDB collection"""
    def __init__(self, collection_name:str):
        self.collection_name=collection_name
        self.collection=None
    async def init_collection(self):
        if db_connection.db is None:
            raise RuntimeError("Database connection is not initialized. Call `connect()` first.")
        self.collection=db_connection.db[self.collection_name]
        

class EventSearchConfigService(DatabaseService):
    def __init__(self):
        super().__init__("event_search_configurations")
    
    async def get_config(self,postcode:str)->dict|None:
        """Retrieve website search configurations for a specific postcode."""
        if not self.collection:
            await self.init_collection()
        try:
            config = await self.collection.find_one({"postcode": postcode})
            if config:
                return config.get("configurations", None)
            else:
                logging.warning(f"No configuration found for postcode {postcode}")
                return None
        except Exception as e:
            logging.error(f"An error occurred retrieving configuration for postcode {postcode}:{e}")
            return None


