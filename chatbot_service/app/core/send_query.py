import requests
import os
from dotenv import load_dotenv
from uuid import uuid4
from app.models.session import Session
from datetime import datetime, timezone
from app.db.database_service import SessionService

info_scraping_service_url=os.getenv("INFO_SCRAPING_SERVICE_URL")
load_dotenv()


async def send_query(request_body, session_service: SessionService):
    request_path="/events/scrape"
    request_base_url=info_scraping_service_url
    session=await session_service.find_user_session(request_body['user_id'])
    if session is None:
        session=Session(user_id=request_body['user_id'], session_id=str(uuid4()), query=request_body['query'], status="in_progress", created_at=datetime.now(timezone.utc))
        await session_service.create_session(session)
    json_data={
        "session_id":session.session_id, 
        "query":request_body['query']
    }
    response=requests.post(url=f"{request_base_url}{request_path}", json=json_data)
    response=response.json() 
    print(response)
    # Start polling here
