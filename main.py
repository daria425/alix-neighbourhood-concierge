from search import TavilySearch
from utils import get_search_api_keys
import json
keys=get_search_api_keys()
searcher=TavilySearch(api_key=keys["tavily"])
postcode="N19QZ"
query=f"{postcode} events"
request_config=searcher.create_search_request(query=query)
results=searcher.run_search(request_config)
print(results)
with open("sample_results.json", "w") as f:
    f.write(json.dumps(results))