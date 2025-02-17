from fastapi import APIRouter, BackgroundTasks, Depends, Response
from app.schemas.pubsub_message import PubSubMessage
from app.core.agent import EventInfoExtractionAgent
from app.db.database_service import EventDataService
from dotenv import load_dotenv
import os, logging
from app.core.process_pubsub_message import process_pubsub_message
load_dotenv()
pubsub_topic_name=os.getenv("PUBSUB_TOPIC_NAME")

router=APIRouter()

@router.post("")
async def recieve_pubsub(pubsub_message: PubSubMessage, background_tasks: BackgroundTasks, event_data_service: EventDataService=Depends(), agent: EventInfoExtractionAgent=Depends()):
    background_tasks.add_task(process_pubsub_message, pubsub_message, event_data_service, agent) # Client will poll for completion of background task
    logging.info("New data from PubSub recieved successfully and pushed forward") # Response sent to pubsub push service
    return Response(status_code=200)
