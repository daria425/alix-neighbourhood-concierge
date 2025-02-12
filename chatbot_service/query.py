from pydantic import BaseModel, ConfigDict

class Query(BaseModel):
    postcode: str
    model_config=ConfigDict(extra='allow')