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


