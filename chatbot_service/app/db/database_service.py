import logging
from app.db.database_connection import db_connection
from app.models.session import Session
class DatabaseService:
    def __init__(self, collection_name:str):
        self.collection_name=collection_name
        self.collection=None
    
    async def init_collection(self):
        if db_connection.db is None:
            raise RuntimeError("Database connection is not initialized. Call `connect()` first.")
        self.collection=db_connection.db[self.collection_name]


class SessionService(DatabaseService):
    def __init__(self):
        super().__init__("sessions")
    
    async def create_session(self, session:Session)->dict:
        if self.collection is None:
            await self.init_collection()
        try:
            session={**session.model_dump(by_alias=True), "_id":session.session_id}
            await self.collection.insert_one(session)
            return {"status": "success", "message": "Session created"}
        except Exception as e:
            logging.error(f"Error creating session: {e}")
            return {"status": "error", "message": f"Error creating session: {str(e)}"}
    async def find_user_session(self, user_id:str):
        if self.collection is None:
            await self.init_collection()
        try:
            user_session=await self.collection.find_one({"user_id": user_id})
            if user_session is not None:
                return Session(**user_session)
            else:
                return None
        except Exception as e:
            logging.error(f"Error finding user session: {e}")
            return None
        
class EventDataService(DatabaseService):
    def __init__(self):
        super().__init__("sessions")
    
    async def get_processed_events_by_session(self, session_id):
        if self.collection is None:
            await self.init_collection()
        processed_event_cursor=self.collection.find({"session_id":session_id})
        processed_events=await processed_event_cursor.to_list()
        return processed_events




