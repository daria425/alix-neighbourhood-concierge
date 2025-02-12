
from app.dependencies.cloud_storage_service import CloudStorageService
from app.db.database_service import EventDataService
from app.schemas.pubsub_message import PubSubMessage
from app.schemas.llm_output import LLM_Output
from typing import List
import logging
import asyncio
import json
import base64
from datetime import datetime

logging.basicConfig(level=logging.INFO) 

def create_prediction_content(event:dict)->List[dict]:
    content_line={
        "role":"user", 
        "parts":[
            {
                "text": f"""
    BEGIN ENTRY
    -----------
    {json.dumps(event)}
    -----------
    END ENTRY
    """
            }
        ]
    }
    return [content_line]
    
    


async def process_pubsub_message(pubsub_message: PubSubMessage, cloud_storage_service: CloudStorageService):
    message=pubsub_message.message
    pubsub_message_data=message.data
    if pubsub_message_data is not None:
        decoded_data=base64.b64decode(pubsub_message_data).decode("utf-8")
        decoded_data=json.loads(decoded_data)
        events=decoded_data.get("events", None)
        filename="event_batch.jsonl"
        # TO DO omg clean thissss
        if events:
            for event in events:
                logging.info(f"Processing event {event['title']}")
                content=create_prediction_content(event)
                json_line={
                    "request": {
                        "contents": content, 
                        "system_instruction": {
                            "parts":{
                                "text": """
You are an event information extraction assistant. Your task is to process content scraped from a webpage and accurately extract detailed event information based on the user-provided query. The goal is to identify key details about the event and organize them in a clear, concise format.
Key Guidelines:
Extract Key Event Details-Identify and extract the following details for each event:

Event Name or Title
Description or Purpose
Date and Time
Venue/Location (including address, if provided)
Organizer (if available)
"""
                            }
                        }, 
                        "tools":[
                            {
                                "function_declarations": [
                                    {
                                        "name":"get_event_data", 
                                        "description": "Extract and structure event information from a given entry", 
                                        "parameters":{
                                            "type": "object",
                "properties": {
                    "tag": {
                        "type": "string",
                        "nullable": False,
                        "description": "A category tag for the event, must be one from the provided list: Arts, Children's Channel, Community Support, Festive, Health & Sport, Music, Playtime, Skill & Professional Development, Social, Workshop",
                    },
                    "event_name": {
                        "type": "string",
                        "nullable": False,
                        "description": "Title or name of the event",
                    },
                    "description": {
                        "type": "string",
                        "nullable": True,
                        "description": "A 1-2 sentence description of the event based on the provided information in the entry or null",
                    },
                    "date_and_time": {
                        "type": "string",
                        "nullable": True,
                        "description": "Date and time when the event is scheduled to occur or null",
                    },
                    "location": {
                        "type": "string",
                        "nullable": True,
                        "description": "Venue or address where the event will take place or null",
                    },
                    "cost": {
                        "type": "string",
                        "nullable": True,
                        "description": "The cost of the event, if available or null",
                    },
                    "booking_details": {
                        "type": "string",
                        "nullable": True,
                        "description": "A link to book the event or get additional details, if available or null",
                    },
                    "is_within_2_weeks": {
                        "type": "boolean",
                        "nullable": False,
                        "description": f"True if date and time of event is within 2 weeks of {datetime.now().strftime('%d %b %Y')}. False otherwise",
                    },
                },
                "required": [
                    "tag",
                    "event_name",
                    "description",
                    "date_and_time",
                    "location",
                    "cost",
                    "booking_details",
                    "is_within_2_weeks",
                ],
                                        }
                                    }
                                ]
                            }
                        ], 
                        "tool_config":{
                            "function_calling_config":{
                                "mode":"any", "allowed_function_names": "get_event_data"
                            }
                        }
                    }
                }
                with open(filename, "a") as f:
                    f.write(json.dumps(json_line)+"\n")
            file_uri=cloud_storage_service.upload_file(filename)
            return file_uri
            







