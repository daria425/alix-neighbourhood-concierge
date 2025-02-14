import pandas as pd
from database_connection import db_connection
from database_service import EventDataService
import asyncio
headers=["Tags", "Event Name", "Date", "Location", "Cost", "Website"]

async def get_events():
    await db_connection.connect()
    event_service=EventDataService()
    events=await event_service.get_events()
    events=events[:2]
    df=pd.DataFrame(events)
    print(df, df.columns)

