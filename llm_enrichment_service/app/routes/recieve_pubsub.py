from fastapi import APIRouter, Request
from app.schemas.pubsub_message import PubSubMessage
router=APIRouter()

@router.post("")
async def recieve_pubsub(message: Request):
    print("message recieved", message)
    saved_message=await message.json()
    print("SAVED MESSAGE",saved_message)
    response={"message": f"Message recieved from PubSub successfully, message contents:{message}"}
    return response
