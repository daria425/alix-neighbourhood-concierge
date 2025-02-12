import logging
from database_connection import db_connection
from query import Query
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

    async def get_events(self, query:Query=None):
        if self.collection is None:
            await self.init_collection()
        projection={
            "title":1,
            "url":1, 
            "llm_output.tag":1, 
            "llm_output.description":1, 
            "llm_output.location":1, 
            "llm_output.cost":1, 
            "llm_output.booking_details":1, 
        }
        try:
            if query is not None:
                events=self.collection.find({"postcode": query.postcode}, projection)
            else:
                events=self.collection.find({}, projection)
            events=await events.to_list()
            return events
        except Exception as e:
            logging.error(f"An error occurred getting events:{e}")