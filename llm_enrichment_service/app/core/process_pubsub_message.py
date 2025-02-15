from app.core.agent import EventInfoExtractionAgent
from app.db.database_service import EventDataService
from app.schemas.pubsub_message import PubSubMessage
from app.schemas.llm_output import LLM_Output
import logging
import json
import base64

logging.basicConfig(level=logging.INFO) 

async def process_events(event_data_service: EventDataService, agent: EventInfoExtractionAgent, session_id:str, page:int=1):
    events=await event_data_service.get_paginated_events(session_id, page)
    for event in events:
            event_str=f"""
            BEGIN ENTRY
            -----------
            {json.dumps(event)}
            -----------
            END ENTRY
            """
            llm_output=agent.run_task(contents=event_str)
            logging.info(f"LLM output: {llm_output}")
            llm_output = LLM_Output(**(llm_output or {}))  
            await event_data_service.update_event_with_llm_output(event['event_id'], session_id, llm_output)

async def process_pubsub_message(pubsub_message: PubSubMessage, event_data_service: EventDataService, agent: EventInfoExtractionAgent):
    message=pubsub_message.message
    pubsub_message_data=message.data
    if pubsub_message_data is not None:
        decoded_data=base64.b64decode(pubsub_message_data).decode("utf-8")
        decoded_data=json.loads(decoded_data)
        pubsub_data=decoded_data.get("pubsub_data", None)
        session_id=pubsub_data['session_id']
        page=pubsub_data['page']
        await process_events(event_data_service, agent, session_id, page)
        logging.info("Event processing done")


