from pydantic import BaseModel, Field
from typing import Dict

class ScrapeRequestQuery(BaseModel):
    postcode: str = Field(..., description="Postcode of the search area")
    params: Dict[str, int] = Field(..., description="Additional query parameters")
    page:int


class ScrapeRequestModel(BaseModel):
    query: ScrapeRequestQuery
    session_id:str