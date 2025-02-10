
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.core.agent import EventInfoExtractionAgent
agent=EventInfoExtractionAgent()
events= [{
    "domain": "centre404.org.uk",
    "title": "(Cancelled) Coffee Morning Jan 2025",
    "url": "https://centre404.org.uk/blog/11882/",
    "content": "This event is cancelled due to staff sickness.Looking for childcare? Want to find free and fun...",
    "timestamp": "2025-01-31T16:18:09.135427+00:00Z",
    "event_id": "1e864dfe23628baa6b11d1a5fb78620d",
    "event_detail": {
      "event_id": "1e864dfe23628baa6b11d1a5fb78620d",
      "sections": [
        { "content": "", "links": [] },
        { "content": "", "links": [] },
        {
          "content": "This event is cancelled due to staff sickness.",
          "links": []
        },
        { "content": "", "links": [] },
        { "content": "", "links": [] },
        {
          "content": "Looking for childcare? Want to find free and fun activities for your child? Need advice on family support? Interested in starting childminding or working in a nursery? \ud83e\uddf8\ud83d\udc76Please join us for our next coffee morning with Islington Family Information Service (FIS)!",
          "links": []
        },
        { "content": "", "links": [] },
        { "content": "Date: Thursday, January 23rd", "links": [] },
        { "content": "Time: 10.30am-12 pm", "links": [] },
        {
          "content": "Location: Centre 404, 404 Camden Road, London N7 0SJ",
          "links": []
        },
        { "content": "", "links": [] },
        {
          "content": "\u2615\ufe0fFIS provides free and impartial service offering information and advice for families with children and young people (0-25) and practitioners working with them. \ud83d\udcda\ud83d\udca1They also offers a free childcare finding brokerage service for families with children under 5 and school-age children needing before and after-school care or childcare during holidays. \ud83c\udf92\ud83d\udcde\u2709\ufe0fThe service provides information on:",
          "links": []
        },
        { "content": "", "links": [] },
        {
          "content": "Come along to learn more and get connected! For any questions please contact family@centre404.org.uk .",
          "links": []
        },
        { "content": "", "links": [] }, 
      ]
    }
  }]

def test_llm_output():
    for event in events:
        event_str=f"""
    BEGIN ENTRY
    -----------
    {json.dumps(event)}
    -----------
    END ENTRY
    """
        res=agent.run_task(contents=event_str)
        assert res is not None
        assert isinstance(res, dict)
        assert "tag" in res
        assert "event_name" in res
        assert "url" in res
        assert "is_within_2_weeks" in res