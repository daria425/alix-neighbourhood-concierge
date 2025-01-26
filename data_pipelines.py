from read_html import WhereCanWeGoReader
from search import WhereCanWeGoSearch
from utils import validate_query
from typing import List



def get_where_can_we_go_dset(query:dict)->List[dict]:
    validate_query(query, required_keys=['postcode', 'miles'])
    searcher=WhereCanWeGoSearch()
    url=searcher.create_request_url(query['postcode'], {"miles":query['miles']})
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
    return event_details

