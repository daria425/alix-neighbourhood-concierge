from pydantic import BaseModel, Field
from typing import Dict

class ScrapeRequestModel(BaseModel):
    postcode: str = Field(..., description="Postcode of the search area")
    params: Dict[str, int] = Field(..., description="Additional query parameters")
    page:int