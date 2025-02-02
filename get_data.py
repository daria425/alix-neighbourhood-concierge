from read_html import HTMLReader
from read_search_results import SearchResultReader
from search import HTMLSearch, TavilySearch
from utils import validate_query, get_search_api_keys
from typing import List

def get_scraped_dset(query: dict) -> List[dict]:
    validate_query(query, required_keys=["request_config", "page_content_config"])
    searcher = HTMLSearch(website=query["request_config"]["website"])
    reader = HTMLReader(page_content_config=query["page_content_config"])
    url = searcher.create_request_url(
        query["request_config"].get("postcode", ""),
        query["request_config"].get("params", {}),
    )
    response = searcher.run_search(url)
    if response.get("error") or not response.get("content"):
        return []
    event_metadata = reader.get_event_metadata(content=response['content'])
    event_detail_html_list = searcher.fetch_event_details(event_metadata)
    
    # Extract event details
    event_details = [reader.get_event_detail(d) for d in event_detail_html_list]
    
    # Create a dictionary for quick lookup
    event_details_map = {detail["event_id"]: detail for detail in event_details}
    
    # Match event details efficiently
    for event in event_metadata:
        event["event_detail"] = event_details_map.get(event["event_id"], None)
        event['event_detail'].pop('event_id')
    return event_metadata

def get_tavily_dset(query: dict) -> List[dict]:
    api_keys = get_search_api_keys()
    validate_query(query, required_keys=["postcode"])
    searcher = TavilySearch(api_key=api_keys["tavily"])
    search_query = f"{query['postcode']} events"
    request_config = searcher.create_search_request(
        search_query,
        {
            "exclude_domains": [
                "wherecanwego.com",
                "peabody.org.uk",
                "www.flightradar24.com",
            ],
            "limit": 10,
        },
    )
    response = searcher.run_search(request_config)
    search_result_reader = SearchResultReader(search_results=response["results"])
    search_results = search_result_reader.scrape_results()
    return search_results


eventbrite_config={
     "page_content_config":{
            "domain": "eventbrite.co.uk",
    "container": {
        "selector":"div[data-testid='organizer-profile__future-events'] div.Container_root__4i85v.NestedActionContainer_root__1jtfr.event-card" # Adjust based on actual structure
    },
    "title": {
        "tag": "h3",
        "filter": {"parameter": "class_", "value": "Typography_root__487rx"}
    },
    "content": {
        "tag": "section",
        "filter": {"parameter": "class_", "value": "event-card-details"}
    },
    "url": {
        "tag": "a",
        "filter": {"parameter": "class_", "value": "event-card-link"}
    }, 
    "details": {
        "container": {
            "tag": "section",
            "filter": {"parameter": "class_", "value": "event-card-details"}
        },
        "sections": {
            "tag": "p",
            "filter": {}
        }
    }
    } 
}
# reader=HTMLReader(page_content_config=eventbrite_config['page_content_config'])
# with open("eventbrite_html.html") as f:
#     content=f.read()
# mtdt=reader.get_event_metadata(content, get_results_from_container=True)
# for m in mtdt:
#     print(m['event_details'])
# #     print(m['content'])
# #     # print(details)