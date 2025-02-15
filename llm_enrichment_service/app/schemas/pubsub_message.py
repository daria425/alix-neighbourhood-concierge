from pydantic import BaseModel
from typing import Optional

class PubSubMessageData(BaseModel):
    data: Optional[str]  # Base64-encoded data
    messageId: Optional[str]
    message_id: Optional[str] 
    publishTime: Optional[str]
    publish_time: Optional[str]

class PubSubMessage(BaseModel):
    message: PubSubMessageData
    subscription: str