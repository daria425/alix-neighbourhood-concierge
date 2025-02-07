from fastapi import APIRouter, Depends
from app.db.database_service import EventDataService
from app.dependencies.publisher_service import PublisherService
from app.core.run_scraping_pipeline import run_scraping_pipeline
from app.schemas.scrape_request import ScrapeRequestModel
router=APIRouter()

def get_publisher_service():
    return PublisherService("enrichment-topic")

@router.post("/bulk-import", status_code=201)
async def bulk_import_events(request_body:ScrapeRequestModel, event_data_service:EventDataService=Depends(), publisher_service: PublisherService=Depends(get_publisher_service)):
    print('request recieved')
    query={
        "postcode":request_body.postcode, 
        "params":request_body.params
    }
    event_list=await run_scraping_pipeline(query)
    insert_response=await event_data_service.bulk_import_events(event_list)
    event_dicts=insert_response['event_dicts']
    publisher_response=publisher_service.publish_events(event_dicts)
    insert_message=insert_response['message']
    pubsub_message=publisher_response['message']
    return {
        "insert_message":insert_message, 
        "pubsub_message":pubsub_message

    }


