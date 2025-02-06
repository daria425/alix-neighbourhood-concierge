from pydantic import BaseModel
from typing import Optional, List

class EventDetailSection(BaseModel):
    content: str 
    links:List[Optional[str]]

class EventDetails(BaseModel):
    event_id:str
    sections:Optional[List[EventDetailSection]]=[]

class Event(BaseModel):
    title: str
    url: str
    content: str
    event_id: str
    domain: str
    timestamp: str
    event_detail: Optional[EventDetails] = None
    errors:Optional[str]=None

