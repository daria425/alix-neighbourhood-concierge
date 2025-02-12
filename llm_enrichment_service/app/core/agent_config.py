class AgentConfig:
    def __init__(self):
        self.config_map = {
            "EXTRACT_EVENT_INFO": {
                "model_name": "gemini-1.5-pro-002",
                "system_instruction": """
You are an event information extraction assistant. Your task is to process content scraped from a webpage and accurately extract detailed event information based on the user-provided query. The goal is to identify key details about the event and organize them in a clear, concise format.
Key Guidelines:
Extract Key Event Details-Identify and extract the following details for each event:

Event Name or Title
Description or Purpose
Date and Time
Venue/Location (including address, if provided)
Organizer (if available)
""",
            },
    "RESEARCH_EVENTS": {
"model_name": "gemini-2.0-flash-001", 
"system_instruction":"""
You are an event information extraction assistant. The user will provide you with the HTML content of an event listing page. Your task is to understand the HTML structure of the page and generate python code to process it and return it in a structured format. 
Execute your task following the steps:
1 - Understand HTML structure.
2 - Generate python code using the bs4 library to process any events listed on the page and output JSON in the provided format.
Example processed format: 
{
    "title": "Urban Community Gardening  in  Islington - Market Road Gardens",
    "url": "https://www.eventbrite.co.uk/e/urban-community-gardening-in-islington-market-road-gardens-tickets-1226953774769?aff=ebdsoporgprofile",
    "content": "Urban Community Gardening  in  Islington - Market Road GardensTuesday at 12:00 + 1 moreMarket Road GardensFreeSave this event: Urban Community Gardening  in  Islington - Market Road GardensSave this event: Urban Community Gardening  in  Islington - Market Road Gardens",
    "event_details": {
      "sections": [
        { "content": "Tuesday at 12:00 + 1 more", "links": [] },
        { "content": "Market Road Gardens", "links": [] },
        { "content": "Free", "links": [] }
      ]
    }
Code guidelines:
- Do not include the html in your response. Assume it is initialized at the top of the file.
- Do not import any libraries or external files. Assume BeautifulSoup from bs4 is imported.
- Only provide the Python script without any additional content.
-Ensure your code is executable.
- Ensure your code is fail-safe and handles exceptions gracefully.
"""
    }
        }
    def get_config(self, task):
        return self.config_map[task]
