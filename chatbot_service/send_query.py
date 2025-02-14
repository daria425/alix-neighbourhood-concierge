import requests
import os
import asyncio
from dotenv import load_dotenv
from uuid import uuid4
from session import Session
from datetime import datetime, timezone
from database_connection import db_connection
from database_service import SessionService

info_scraping_service_url=os.getenv("INFO_SCRAPING_SERVICE_URL")
load_dotenv()
request_body={
    "query":{
    "postcode":"N19QZ", 
    "params":{
        "miles":2
    },
    "page":1,
    },
    "user_id":"mock_user_id"
}

async def send_query(request_body, session_service: SessionService):
    await db_connection.connect()
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
    print(response)
    await db_connection.close()

asyncio.run(send_query(request_body, SessionService()))
