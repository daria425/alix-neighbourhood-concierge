from app.core.agent import EventInfoExtractionAgent
from app.db.database_service import EventDataService
from app.schemas.pubsub_message import PubSubMessage
import json
import base64

async def process_event(event:dict, event_data_service: EventDataService, agent: EventInfoExtractionAgent):
    event_str=f"""
    BEGIN ENTRY
    -----------
    {json.dumps(event)}
    -----------
    END ENTRY
    """
    llm_output=agent.run_task(contents=event_str)
    if llm_output is not None:
        await event_data_service.update_event_with_llm_output(event['event_id'], llm_output)

async def process_pubsub_message(pubsub_message: PubSubMessage, event_data_service: EventDataService, agent: EventInfoExtractionAgent):
    message=pubsub_message.message
    pubsub_message_data=message.data
    if pubsub_message_data is not None:
        decoded_data=base64.b64decode(pubsub_message_data).decode("utf-8")
        decoded_data=json.loads(decoded_data)
        events=decoded_data.get("events", None)
        if events:
            for event in events:
                await process_event(event, event_data_service, agent)




