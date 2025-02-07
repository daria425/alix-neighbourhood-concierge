from app.db.database_connection import db_connection
from app.models.event import Event
from typing import List

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


class EventDataService(DatabaseService):
    def __init__(self):
        super().__init__("events")
        
    async def bulk_import_events(self,event_list:List[Event])->dict:
        if not self.collection:
            await self.init_collection()
        new_event_ids=[event.event_id for event in event_list]
        existing_ids=await self.collection.distinct("event_id", {"event_id": {"$in": new_event_ids }})
        new_events=[event for event in event_list if event.event_id not in existing_ids]
        if not new_events:
                return {"message": "No new events to insert.", "event_dicts":[]}
        try: 
            event_dicts = [
            {**event.model_dump(by_alias=True), "_id": event.event_id} for event in new_events
        ]
            insert_result=await self.collection.insert_many(event_dicts)
            inserted_ids=insert_result.inserted_ids
            message=f"Successfully imported {len(inserted_ids)} events"
            return {"message":message, "event_dicts": event_dicts}
        except Exception as e:
            return {"message":f"Error importing events: {e}"}



