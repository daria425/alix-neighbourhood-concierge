import logging
from app.db.database_connection import db_connection
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

    
    async def update_event_with_llm_output(self, event_id:str, llm_output:dict):
        if self.collection is None:
            await self.init_collection()
        try:
            await self.collection.update_one({"_id":event_id, "llm_output":{"$exists":False}}, {"$set":{"llm_output": llm_output}})
        except Exception as e:
            logging.error(f"An error occurred updating events:{e}")


            