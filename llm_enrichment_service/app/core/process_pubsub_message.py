
from app.dependencies.cloud_storage_service import CloudStorageService

from app.schemas.pubsub_message import PubSubMessage
from app.core.agent import EventInfoExtractionAgent
from typing import List
import logging
import json
import base64

logging.basicConfig(level=logging.INFO) 

CHUNK_SIZE=20

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
    
    


async def process_pubsub_message(pubsub_message: PubSubMessage, cloud_storage_service: CloudStorageService, agent: EventInfoExtractionAgent):
    message=pubsub_message.message
    pubsub_message_data=message.data
    if pubsub_message_data is not None:
        decoded_data=base64.b64decode(pubsub_message_data).decode("utf-8")
        decoded_data=json.loads(decoded_data)
        events=decoded_data.get("events", [])
     
        file_uris=[]
        for i in range(0,len(events), CHUNK_SIZE):
                chunk=events[i:i+CHUNK_SIZE]
                filename=f"event_batch_i_{i // CHUNK_SIZE}.jsonl"
                with open(filename, "w") as f:
                     for event in chunk:
                          logging.info(f"Processing event {event['title']}")
                          content=create_prediction_content(event)
                          json_line=agent.create_batch_input_dataset(content=content)
                          f.write(json.dumps(json_line)+"\n")
                file_uri=cloud_storage_service.upload_file(filename)
                file_uris.append(file_uri)
                logging.info(f"Uploaded {filename} -> {file_uri}")
        return file_uris




            
            







