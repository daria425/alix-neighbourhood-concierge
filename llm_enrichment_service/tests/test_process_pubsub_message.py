import sys
import json
import pytest
import base64
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.schemas.pubsub_message import PubSubMessage
from app.core.process_pubsub_message import process_pubsub_message
@pytest.mark.asyncio
async def test_process_pubsub_message():
    events=[
    {
    "domain": "eventbrite.co.uk",
    "title": "Practical Support for non-UK Rough Sleepers",
    "url": "https://www.eventbrite.co.uk/e/practical-support-for-non-uk-rough-sleepers-tickets-1132230685459?aff=ebdsoporgprofile",
    "content": "Practical Support for non-UK Rough SleepersWed, 12 Feb, 11:30 GMT+2FreeSave this event: Practical Support for non-UK Rough SleepersSave this event: Practical Support for non-UK Rough Sleepers",
    "timestamp": "2025-02-02T22:52:17.387671+00:00Z",
    "event_id": "6cc23a9b097bb31ed7e08499e2f7050e",
    "event_details": {
      "event_id": "6cc23a9b097bb31ed7e08499e2f7050e",
      "sections": [
        { "content": "Wed, 12 Feb, 11:30 GMT+2", "links": [] },
        { "content": "Free", "links": [] }
      ]
    }
  }

]
    mock_event_data_service=AsyncMock()
    mock_agent=MagicMock()
    mock_agent.run_task.return_value="Mocked llm output"
    event_list=base64.b64encode((json.dumps({"events":events})).encode("utf-8")).decode("utf-8")
    mock_pubsub_message_data={
        "data": event_list, 
        "messageId": "", 
        "message_id":"",
        "publishTime":"", 
        "publish_time":"" 

    }
    mock_pubsub_message=PubSubMessage(message=mock_pubsub_message_data, subscription="")
    await process_pubsub_message(mock_pubsub_message, mock_event_data_service, mock_agent)
    mock_agent.run_task.assert_called_once()
    mock_event_data_service.update_event_with_llm_output.assert_called_once_with("6cc23a9b097bb31ed7e08499e2f7050e", "Mocked llm output")
