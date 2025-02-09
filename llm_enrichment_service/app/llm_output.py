from pydantic import BaseModel, Field
from typing import Optional

class LLM_Output(BaseModel):
    tag:str=Field(...)
    event_name:str=Field(...)
    description:Optional[str]=None
    location:Optional[str]=None
    cost: Optional[str]=None
    booking_details:Optional[str]=None
    url:str=Field(...)
    is_within_2_weeks: Optional[bool]=None
    