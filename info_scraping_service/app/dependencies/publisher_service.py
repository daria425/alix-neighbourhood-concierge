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


    def publish(self, pubsub_data):
        try:
            published_message=json.dumps({"pubsub_data":pubsub_data}).encode("utf-8")
            future=self.publisher.publish(self.topic_path, published_message)
            published_message_id=future.result()
            return {"message": f"Published session info to PubSub", "published_message_id":published_message_id, "status":201}
        except Exception as e:
            logging.error(f"An error in PublisherService occurred: {e}")
            return {"message": f"Error publishing to PubSub:{e}", "published_message_id":None, "status":500}




