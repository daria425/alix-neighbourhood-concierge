import logging
from app.db.database_connection import db_connection
from app.schemas.llm_output import LLM_Output
# from dotenv import load_dotenv
# load_dotenv()


class DatabaseService:
    def __init__(self, collection_name:str):
        self.collection_name=collection_name
        self.collection=None
    
    async def init_collection(self):
        if db_connection.db is None:
            raise RuntimeError("Database connection is not initialized. Call `connect()` first.")
        self.collection=db_connection.db[self.collection_name]


class EventDataService(DatabaseService):
    def __init__(self):
        super().__init__("events")

    async def get_events(self):
        if self.collection is None:
            await self.init_collection()
        try:
            events=self.collection.find({})
            events=await events.to_list()
            return events
        except Exception as e:
            logging.error(f"An error occurred getting events:{e}")
            return []

    async def get_paginated_events(self, session_id:str, page:int, page_size:int=10):
        if self.collection is None:
            await self.init_collection()
        skip=(page-1)*page_size
        try:
            cursor=self.collection.find({"session_id":session_id}).sort("event_id", 1).skip(skip).limit(page_size)
            events=await cursor.to_list()
            return events
        except Exception as e:
            logging.error(f"Error finding events:{e}")
            return []

    async def update_event_with_llm_output(self, session_id:str, event_id:str, llm_output:LLM_Output):
        if self.collection is None:
            await self.init_collection()
        try:
            logging.info("Updating event...")
            llm_output=llm_output.model_dump(by_alias=True)
            await self.collection.update_one({"_id":event_id, "session_id":session_id}, {"$set":{"llm_output": llm_output, "status":"completed"}})
        except Exception as e:
            logging.error(f"An error occurred updating events:{e}")



            