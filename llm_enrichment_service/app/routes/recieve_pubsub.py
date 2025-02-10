from fastapi import APIRouter, BackgroundTasks, Depends
from app.schemas.pubsub_message import PubSubMessage
from app.core.agent import EventInfoExtractionAgent
from app.db.database_service import EventDataService
from app.core.process_pubsub_message import process_pubsub_message
router=APIRouter()

@router.post("")
async def recieve_pubsub(pubsub_message: PubSubMessage, background_tasks: BackgroundTasks, event_data_service: EventDataService=Depends(), agent: EventInfoExtractionAgent=Depends()):
    background_tasks.add_task(process_pubsub_message, pubsub_message, event_data_service, agent)
    response={
                "message": "New data from PubSub recieved successfully"
            }

    return response
