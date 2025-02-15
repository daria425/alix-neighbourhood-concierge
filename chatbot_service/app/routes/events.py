from fastapi import APIRouter, Depends
from app.core.send_query import send_query
from app.db.database_service import SessionService
from app.schemas.request_body import RequestBody
router=APIRouter()

@router.post("/start")
async def start_scraping(request_body: RequestBody, session_service: SessionService=Depends()):
    request_body=request_body.model_dump(by_alias=True)
    session_id=await send_query(request_body, session_service)
    return session_id

