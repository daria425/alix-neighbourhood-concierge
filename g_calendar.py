#TO-DO make this a class later and add logic around it
from dotenv import load_dotenv
import os
from googleapiclient.discovery import build
from google.oauth2 import service_account

load_dotenv()
keyfile_path=os.getenv("KEYFILE_PATH")

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
creds = service_account.Credentials.from_service_account_file(keyfile_path, scopes=SCOPES)
service = build("calendar", "v3", credentials=creds)
calendar_id = "c_9e4cbbe056f4dfdc8cfca43b7064555e89eff0449021acb20e1eb7a2cd3fa383@group.calendar.google.com"


events_result = service.events().list(calendarId=calendar_id, maxResults=10, singleEvents=True, orderBy="startTime").execute()
events = events_result.get("items", [])
print(events)