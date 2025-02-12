from pydantic import BaseModel, Field
from typing import Optional

class LLM_Output(BaseModel):
    tag:str=Field(...)
    event_name:str=Field(...)
    date_and_time:Optional[str]=None
    description:Optional[str]=None
    location:Optional[str]=None
    cost: Optional[str]=None
    booking_details:Optional[str]=None
    is_within_2_weeks: Optional[bool]=None
    