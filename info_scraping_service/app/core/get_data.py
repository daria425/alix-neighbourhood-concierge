from app.core.read_html import HTMLReader
from app.core.search import HTMLSearch, DynamicSearch
from app.utils.utils import validate_query, remove_duplicates
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


