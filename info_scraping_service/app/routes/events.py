from fastapi import APIRouter, Depends
from app.dependencies.publisher_service import PublisherService
from app.db.database_service import SessionService, EventDataService
from uuid import uuid4
from app.core.run_scraping_pipeline import run_scraping_pipeline
from app.schemas.scrape_request import ScrapeRequestModel
from app.models.session import Session
import os, logging
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()
pubsub_topic_name=os.getenv("PUBSUB_TOPIC_NAME")
router=APIRouter()

def get_publisher_service():
    return PublisherService(pubsub_topic_name)

@router.post("/import")
async def get_events(request_body:ScrapeRequestModel, publisher_service: PublisherService=Depends(get_publisher_service), event_data_service: EventDataService=Depends(), session_data_service: SessionService=Depends())->dict:
    print('request recieved')
    query={
        "postcode":request_body.postcode, 
        "params":request_body.params
    }
    event_list=await run_scraping_pipeline(query)
    session_id=str(uuid4())
    session=Session(session_id=session_id, query=query, status="in_progress", created_at=datetime.now(timezone.utc))
    event_dicts = [
            {**event.model_dump(by_alias=True), "_id":event.event_id, "session_id":session_id} for event in event_list
        ]
    database_import_message=await event_data_service.import_events(event_dicts)
    session_message=await session_data_service.create_session(session)
    logging.info(f"Database messages: {session_message['message']}, {database_import_message['message']}")
    pubsub_data={
       "session_id":session_id, 
       "page": request_body.page 
    }
    publisher_response=publisher_service.publish(pubsub_data)
    pubsub_message=publisher_response['message']
    return {
        "pubsub_message":pubsub_message
    }


