from read_html import WhereCanWeGoReader, IslingtonLifeReader, TrinityIslingtonReader, Centre404Reader
from read_search_results import SearchResultReader
from search import WhereCanWeGoSearch, TavilySearch, IslingtonLifeSearch, TrinityIslingtonSearch, Centre404Search
from utils import validate_query, get_search_api_keys
from typing import List
import json

def get_where_can_we_go_dset(query:dict)->List[dict]:
    validate_query(query, required_keys=['postcode', 'miles'])
    searcher=WhereCanWeGoSearch()
    reader=WhereCanWeGoReader()
    url=searcher.create_request_url(query['postcode'], {"miles":query['miles']})
    html_content=searcher.run_search(url)
    if isinstance(html_content, dict) and html_content.get("error"):
        return []
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
    return event_metadata

def get_tavily_dset(query:dict)->List[dict]:
    api_keys=get_search_api_keys()
    validate_query(query, required_keys=['postcode'])
    searcher=TavilySearch(api_key=api_keys["tavily"])
    search_query=f"{query['postcode']} events"
    request_config=searcher.create_search_request(search_query, {"exclude_domains":["wherecanwego.com", "peabody.org.uk", "www.flightradar24.com"], "limit":10})
    response=searcher.run_search(request_config)
    search_result_reader=SearchResultReader(search_results=response["results"])
    search_results=search_result_reader.scrape_results()
    return search_results

def get_islington_life_dset(query:dict)->List[dict]:
    validate_query(query, required_keys=['postcode'])
    if query['postcode']!="N19QZ":
        raise ValueError(f"Wrong scraping pipeline initialized for {query['postcode']}")
    searcher=IslingtonLifeSearch()
    reader=IslingtonLifeReader()
    url=searcher.create_request_url()
    html_content=searcher.run_search(url)
    if isinstance(html_content, dict) and html_content.get("error"):
        return []
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
    return event_metadata
    
def get_trinity_inslington_dset(query: dict)->List[dict]:
    validate_query(query, required_keys=['postcode'])
    if query['postcode']!="N19QZ":
        raise ValueError(f"Wrong scraping pipeline initialized for {query['postcode']}")
    searcher=TrinityIslingtonSearch()
    reader=TrinityIslingtonReader()
    url=searcher.create_request_url()
    html_content=searcher.run_search(url)
    if isinstance(html_content, dict) and html_content.get("error"):
        return []
    event_metadata=reader.get_event_metadata(html_content)
    return event_metadata

def get_centre_404_dset(query:dict)->List[dict]:
    validate_query(query, required_keys=['postcode'])
    if query['postcode']!="N19QZ":
        raise ValueError(f"Wrong scraping pipeline initialized for {query['postcode']}")
    searcher=Centre404Search()
    reader=Centre404Reader()
    url=searcher.create_request_url()
    html_content=searcher.run_search(url)
    if isinstance(html_content, dict) and html_content.get("error"):
        return []
    event_metadata=reader.get_event_metadata(html_content)
    event_detail_html_list=searcher.fetch_event_details(event_metadata)
    event_details=[]
    for d in event_detail_html_list:
        event_detail = reader.get_event_detail(d)
        event_details.append(event_detail)
    for event in event_metadata:
        matching_event_detail = next((detail for detail in event_details if detail['event_id'] == event['event_id']), None)
        if matching_event_detail:
            event['event_detail'] = matching_event_detail
    return event_metadata
    
    
    

    



    




# create some executor interface that runs this and adds the client & postcode as well
