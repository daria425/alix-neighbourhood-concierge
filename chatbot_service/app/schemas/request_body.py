from pydantic import BaseModel, ConfigDict

class RequestQuery(BaseModel):
    postcode: str
    params:dict
    page:int
    model_config=ConfigDict(extra='allow')
class RequestBody(BaseModel):
    query: RequestQuery
    user_id:str