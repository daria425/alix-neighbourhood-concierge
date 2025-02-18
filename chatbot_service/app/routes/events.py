from fastapi import APIRouter, Depends,Query
from app.core.send_query import send_query
from app.db.database_service import SessionService, EventDataService
from app.schemas.request_body import RequestBody
router=APIRouter()

@router.post("/start")
async def start_scraping(request_body: RequestBody, session_service: SessionService=Depends()):
    request_body=request_body.model_dump(by_alias=True)
    session_id=await send_query(request_body, session_service)
    return session_id


@router.get("/status")
async def get_processing_status(session_id:str, page:int, page_size:int, event_data_service:EventDataService=Depends()): #page & page size to be included in query
    #Update this to incl page size and page
    processed_events=await event_data_service.get_processed_events_by_session(session_id)
    all_processed=all(event["status"] == "completed" for event in processed_events)
    return {
        "session_id": session_id,
        "all_processed": all_processed,
        "remaining_count": sum(1 for event in processed_events if event["status"] != "completed"),
        "events": processed_events
    }
