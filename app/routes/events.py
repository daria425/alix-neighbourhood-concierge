from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.core.run_scraping_pipeline import run_scraping_pipeline
from app.models.scrape_request import ScrapeRequestModel
router=APIRouter()

@router.post("/bulk-import", status_code=201)
def bulk_import_events(request_body:ScrapeRequestModel):
    print('request recieved')
    query={
        "postcode":request_body.postcode, 
        "params":request_body.params
    }
    event_list=run_scraping_pipeline(query)
    return event_list

