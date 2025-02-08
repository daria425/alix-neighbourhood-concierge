from fastapi import APIRouter, Request
from app.schemas.pubsub_message import PubSubMessage
import base64
router=APIRouter()

@router.post("")
async def recieve_pubsub(pubsub_message: PubSubMessage):
    message=pubsub_message.message
    decoded_data=None
    if message.data:
        decoded_data=base64.b64decode(message.data).decode("utf-8")
        print(decoded_data)
    response={
                "message": "New data from PubSub recieved successfully"
            }

    return response
