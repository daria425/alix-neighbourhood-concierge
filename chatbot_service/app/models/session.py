from pydantic import BaseModel, Field
from datetime import datetime

class Session(BaseModel):
    user_id:str
    session_id:str
    query:dict
    status: str=Field(default="in_progress")
    created_at: datetime