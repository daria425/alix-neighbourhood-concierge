from fastapi import APIRouter, Depends
from app.schemas.pubsub_message import PubSubMessage
from app.core.agent import EventInfoExtractionAgent
from app.db.database_service import EventDataService
import base64
import json
router=APIRouter()

@router.post("")
async def recieve_pubsub(pubsub_message: PubSubMessage, agent:EventInfoExtractionAgent=Depends(), event_data_service: EventDataService=Depends()):
    message=pubsub_message.message
    decoded_data=None
    if message.data:
        decoded_data=base64.b64decode(message.data).decode("utf-8")
        events=decoded_data.get("events", None)
        for event in events:
            event_str=f"""
BEGIN ENTRY
-----------
{json.dumps(event)}
-----------
END ENTRY
"""
        res=agent.run_task(contents=event_str)
        await event_data_service.update_event_with_llm_output(event['event_id'], res)


    response={
                "message": "New data from PubSub recieved successfully"
            }

    return response
