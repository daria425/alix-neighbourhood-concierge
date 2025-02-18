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
        if self.collection is None:
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


class EventDataService(DatabaseService):
    def __init__(self):
        super().__init__("events")
        
    async def import_events(self,event_dicts:dict)->dict:
        if self.collection is None:
            await self.init_collection()
        try: 
            insert_result=await self.collection.insert_many(event_dicts)
            inserted_ids=insert_result.inserted_ids
            return {"message":f"Successfully imported {len(inserted_ids)} events",  "status":"success", "event_ids":inserted_ids}
        except Exception as e:
            return {"message":f"Error importing events: {e}", "status":"error", "event_ids":[]}
        
    async def get_events(self, postcode:str):
        if self.collection is None:
            await self.init_collection()
        cursor=self.collection.find({"postcode":postcode})
        event_dicts=await cursor.to_list()
        message=f"Returning {len(event_dicts)} events from database"
        return {
            "message":message, "event_dicts":event_dicts, "status":"success", 
        }
    
    async def get_paginated_events(self, session_id:str, page:int, page_size:int=10):
        if self.collection is None:
            await self.init_collection()
        skip=(page-1)*page_size
        try:
            cursor=self.collection.find({"session_id":session_id}).skip(skip).limit(page_size)
            events=await cursor.to_list()
            return events
        except Exception as e:
            logging.error(f"Error finding events:{e}")
            return []


