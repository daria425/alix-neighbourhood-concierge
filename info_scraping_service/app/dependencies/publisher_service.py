from google.cloud import pubsub_v1
from typing import List
import json
import os
import logging
from dotenv import load_dotenv
load_dotenv()
project_id=os.getenv("GOOGLE_PROJECT_ID")
class PublisherService:
    project_id=project_id
    def __init__(self, topic_name):
        self.publisher=pubsub_v1.PublisherClient()
        self.topic_name=topic_name
        self.topic_path=f"projects/{self.project_id}/topics/{self.topic_name}"


    def publish_events(self, event_dicts: List[dict]):
        try:
            if len(event_dicts)==0:
                return {"message": f"No new messages publish to PubSub", "published_message_id":None}
            published_message=json.dumps({"events":event_dicts}).encode("utf-8")
            future=self.publisher.publish(self.topic_path, published_message)
            published_message_id=future.result()
            return {"message": f"Published {len(event_dicts)} messages to PubSub", "published_message_id":published_message_id}
        except Exception as e:
            logging.error(f"An error in PublisherService occurred: {e}")
            return {"message": f"Error publishing to PubSub:{e}", "published_message_id":None}




