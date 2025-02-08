from app.core.read_html import HTMLReader
from app.core.read_search_results import SearchResultReader
from app.core.search import HTMLSearch, TavilySearch, DynamicSearch
from app.models.event import Event
from app.utils.utils import validate_query, get_search_api_keys, remove_duplicates
from typing import List

async def get_scraped_dset(query: dict) -> List[dict]:
    validate_query(query, required_keys=["request_config", "page_content_config"])
    request_config=query['request_config']
    page_content_config=query['page_content_config']
    if request_config.get("website_type")=="dynamic":
        searcher = DynamicSearch(website=request_config['website'])
    else:
        searcher=HTMLSearch(website=request_config['website'])
    reader = HTMLReader(page_content_config=page_content_config)
    url = searcher.create_request_url(
        request_config.get("postcode", ""),
        request_config.get("params", {}),
    )
    if "locator" in page_content_config:
        response = await searcher.run_search(url, locator_config=page_content_config['locator']) # will use playwright so await by default
    else: 
        response=searcher.run_search(url)
    if response.get("error") or not response.get("content"):
        return []
    event_metadata = reader.get_event_metadata(content=response['content'], include_event_details=request_config['include_event_details'])
    event_metadata=[{**event, "postcode":request_config['postcode']} for event in event_metadata]
    if request_config['include_event_details']==False:
        event_detail_html_list = await searcher.fetch_event_details(event_metadata)
        event_details = [reader.get_event_detail(d) for d in event_detail_html_list]
        event_details_map = {detail["event_id"]: detail for detail in event_details}
        for event in event_metadata:
            event["event_detail"] = event_details_map.get(event["event_id"], None)
    dset=remove_duplicates(event_metadata, 'event_id')
    return dset

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
    for result in search_results:
        result['postcode']=query['postcode']
    return search_results

