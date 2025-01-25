from read_html import WhereCanWeGoReader
from search import WhereCanWeGoSearch
import json

postcode="N19QZ"
miles=2

searcher=WhereCanWeGoSearch()
url=searcher.create_request_url(postcode, {"miles":miles})
print(url)

html_content=searcher.run_search(url)

reader=WhereCanWeGoReader()
event_metadata=reader.get_event_metadata(content=html_content)
event_detail_html_list=searcher.fetch_event_details(event_metadata)
event_details = []
for d in event_detail_html_list:
    event_detail = reader.get_event_detail(d)
    event_details.append(event_detail)
for event in event_metadata:
    matching_event_detail = next((detail for detail in event_details if detail['event_id'] == event['event_id']), None)
    if matching_event_detail:
        event['event_detail'] = matching_event_detail

with open("sample.json", "w") as f:
    f.write(json.dumps(event_metadata))

