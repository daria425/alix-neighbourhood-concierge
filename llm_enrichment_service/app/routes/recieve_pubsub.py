from fastapi import APIRouter, Depends
from app.schemas.pubsub_message import PubSubMessage
from app.core.agent import EventInfoExtractionAgent
from app.dependencies.cloud_storage_service import CloudStorageService
from app.core.process_pubsub_message import process_pubsub_message
from app.dependencies.cloud_storage_service import CloudStorageService
from dotenv import load_dotenv
import vertexai
import os
load_dotenv()
gcs_bucket_name=os.getenv("GCS_BUCKET_NAME")
project_id=os.getenv("GOOGLE_PROJECT_ID")
location=os.getenv("GOOGLE_PROJECT_LOCATION")
vertexai.init(project=project_id, location=location)

router=APIRouter()

def get_cloud_storage_service():
    return CloudStorageService(project_id=project_id, bucket_name=gcs_bucket_name)
@router.post("")
async def recieve_pubsub(pubsub_message: PubSubMessage, agent: EventInfoExtractionAgent=Depends(), cloud_storage_service: CloudStorageService=Depends(get_cloud_storage_service)):
    gcs_uris=await process_pubsub_message(pubsub_message, cloud_storage_service, agent)
    print(gcs_uris)
    output_uri_prefix=f"gs://{gcs_bucket_name}/"
    print("SENDING TO THIS BUCKET", output_uri_prefix)
    batch_prediction_info=agent.create_batch_prediction_job(input_dataset=gcs_uris[0], output_uri_prefix=output_uri_prefix)
    response={
                "message": "New data from PubSub recieved successfully and uploaded to GCS"
            }

    return response
