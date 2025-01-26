# from search import TavilySearch
# from utils import get_search_api_keys
# import json
# with open("data/json/tavily_sample_results.json", "r") as f:
#     search_results=json.loads(f.read())

from search import TavilySearch
from utils import get_search_api_keys
import json
api_keys=get_search_api_keys()
searcher=TavilySearch(api_key=api_keys["tavily"])
query="N1 9QZ events"
request_config=searcher.create_search_request(query, {"exclude_domains":["wherecanwego.com", "peabody.org.uk"]})
search_results=searcher.run_search(request_config)
with open("data/json/tavily_sample_results.json", "w") as f:
    f.write(json.dumps(search_results))