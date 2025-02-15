from pydantic import BaseModel, Field
from typing import Optional

class LLM_Output(BaseModel):
    tag:Optional[str]=None
    event_name:Optional[str]=None
    date_and_time:Optional[str]=None
    description:Optional[str]=None
    location:Optional[str]=None
    cost: Optional[str]=None
    booking_details:Optional[str]=None
    is_within_2_weeks: Optional[bool]=None
    