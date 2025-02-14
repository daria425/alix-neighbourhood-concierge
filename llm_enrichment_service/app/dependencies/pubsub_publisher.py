from google.cloud import pubsub_v1
from dotenv import load_dotenv
import os, json, logging
load_dotenv()
project_id=os.getenv("GOOGLE_PROJECT_ID")
class PubSubPublisher():
    def __init__(self, topic_name):
        self.publisher=pubsub_v1.PublisherClient()
        self.topic_path=f"projects/{project_id}/topics/{topic_name}"

    def publish_events(self, processed_messages, session_id):
        try:
            published_message=json.dumps({"processed_messages":processed_messages, "session_id":session_id}).encode("utf-8")
            future=self.publisher.publish(self.topic_path, published_message)
            published_message_id=future.result()
            return {"message": f"Published session info to PubSub", "published_message_id":published_message_id, "status":201}
        except Exception as e:
            logging.error(f"An error in PublisherService occurred: {e}")
            return {"message": f"Error publishing to PubSub:{e}", "published_message_id":None, "status":500}