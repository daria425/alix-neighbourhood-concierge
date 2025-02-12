from fastapi import APIRouter, Depends
from app.dependencies.publisher_service import PublisherService
from app.core.run_scraping_pipeline import run_scraping_pipeline
from app.schemas.scrape_request import ScrapeRequestModel
import os
from dotenv import load_dotenv

load_dotenv()
gcs_bucket_name=os.getenv("GCS_BUCKET_NAME")
router=APIRouter()

def get_publisher_service():
    return PublisherService("enrichment-topic")

@router.post("/bulk-import")
async def bulk_import_events(request_body:ScrapeRequestModel, publisher_service: PublisherService=Depends(get_publisher_service))->dict:
    print('request recieved')
    query={
        "postcode":request_body.postcode, 
        "params":request_body.params
    }
    event_list=await run_scraping_pipeline(query)
    event_dicts = [
            {**event.model_dump(by_alias=True)} for event in event_list
        ]
    publisher_response=publisher_service.publish_events(event_dicts)
    pubsub_message=publisher_response['message']
    return {
     
        "pubsub_message":pubsub_message

    }


