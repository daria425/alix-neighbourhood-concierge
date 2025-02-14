from fastapi import APIRouter, Depends
from app.dependencies.publisher_service import PublisherService
from app.db.database_service import EventDataService
from app.core.run_scraping_pipeline import run_scraping_pipeline
from app.schemas.scrape_request import ScrapeRequestModel
import os, logging
from dotenv import load_dotenv
load_dotenv()
pubsub_topic_name=os.getenv("PUBSUB_TOPIC_NAME")
router=APIRouter()

def get_publisher_service():
    return PublisherService(pubsub_topic_name)

@router.post("/scrape")
async def scrape_events(request_body:ScrapeRequestModel, publisher_service: PublisherService=Depends(get_publisher_service), event_data_service: EventDataService=Depends())->dict:
    print('request recieved')
    query=request_body.query.model_dump(by_alias=True)
    event_list=await run_scraping_pipeline(query)
    event_dicts = [
            {**event.model_dump(by_alias=True), "_id":event.event_id, "session_id":request_body.session_id} for event in event_list
        ]
    database_import_message=await event_data_service.import_events(event_dicts)
    logging.info(f"Database message: {database_import_message['message']}")
    pubsub_data={
       "session_id":request_body.session_id, 
       "page": request_body.query.page 
    }
    publisher_response=publisher_service.publish(pubsub_data)
    pubsub_message=publisher_response['message'] # {"message": f"Published session info to PubSub", "published_message_id":published_message_id, "status":201}
    return {
        "pubsub_message":pubsub_message
    }


