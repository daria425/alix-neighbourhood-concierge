from fastapi import APIRouter
from app.db.database_service import EventDataService
from app.core.run_scraping_pipeline import run_scraping_pipeline
from app.schemas.scrape_request import ScrapeRequestModel
router=APIRouter()

event_data_service=EventDataService()
@router.post("/bulk-import", status_code=201)
async def bulk_import_events(request_body:ScrapeRequestModel):
    print('request recieved')
    query={
        "postcode":request_body.postcode, 
        "params":request_body.params
    }
    event_list=await run_scraping_pipeline(query)
    message=await event_data_service.bulk_import_events(event_list)
    return message


