from google.cloud import pubsub_v1
from dotenv import load_dotenv
import os, json, logging
load_dotenv()
project_id=os.getenv("GOOGLE_PROJECT_ID")
class SubscriptionService:
    def __init__(self, subscription_name):
        self.subscriber=pubsub_v1.SubscriberClient()
        self.subscription_name=f"projects/{project_id}/subscriptions/{subscription_name}"
    def callback(pubsub_message):
        try:
            processed_events=json.loads(pubsub_message.data)
            print(processed_events)
            return processed_events
        except Exception as e:
            logging.error(f"Error in subscription service: {e}")
        finally: 
            pubsub_message.ack()

    def start_pull_subscription(self):
        try:
            future= self.subscriber.subscribe(self.subscription_name, self.callback)
            logging.info(f"Subscribed to {self.subscription_name}")
            future.result()
        except Exception as e:
            logging.error(f"Error starting subscription: {e}")



