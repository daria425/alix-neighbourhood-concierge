from google.cloud import storage
import logging


class CloudStorageService:
    def __init__(self, project_id, bucket_name):
        self.client=storage.Client(project=project_id)
        self.bucket=self.client.bucket(bucket_name)
    
    def upload_file(self, filename:str, content_type:str="application/json")->str:
        blob=self.bucket.blob(filename)
        try: 
            blob.upload_from_filename(filename, content_type=content_type)
            return f"gs://{self.bucket.name}/{filename}"
        except Exception as e:
            logging.error(f"Error uploading to GCS: {e}")
            return None
            