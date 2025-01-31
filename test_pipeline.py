import json
import time
from agent import EventInfoExtractionAgent
from get_data import get_tavily_dset, get_scraped_dset
from config.query_config import query_config_centre404, query_config_islignton, query_config_wherecanwego
from utils import format_timestamp
from itertools import chain
from dotenv import load_dotenv
import os
load_dotenv()
postcode=os.getenv("POSTCODE")
client=os.getenv("CLIENT_NAME")
miles=2
query={
    "postcode":postcode, 
    "params": {"miles":miles}
}
configs=[query_config_islignton, query_config_centre404, query_config_wherecanwego]
scraped_data_list=[]
start_time=time.time()
for config in configs:
    config['request_config']['postcode']=query['postcode']
    config['request_config']['params']=query['params']
    scraped_data=get_scraped_dset(config)
    scraped_data_list.append(scraped_data)
tavily_results=get_tavily_dset(query)
final_list=list(chain.from_iterable(scraped_data_list))+tavily_results
has_errors=any("error" in input for input in final_list)
end_time=time.time()
execution_time = end_time - start_time
final_data={
    "postcode": query['postcode'],
    "timestamp": format_timestamp(), 
    "client": client, 
    "errors":has_errors, 
    "execution_time": f"{execution_time:.2f}", 
    "data":final_list
}
with open("data/json/sample_results.json", "w") as f:
    f.write(json.dumps(final_data))
# # test run of the full pipeline
# start_time=time.time()
# tavily_results=get_tavily_dset(query=query)
# final_list=tavily_results
# # TO-DO add llm text summary?
# print(f"Total search results: {len(final_list)}")
# extract_agent=EventInfoExtractionAgent()
# for input in final_list[:15]:
#     input_copy = input.copy()
#     input_copy["text"] = json.dumps(input_copy)
#     formatted_input = f"""
#     -----------
#     BEGIN ENTRY
#     -----------
#     {input_copy["text"]}
#     ----------
#     END ENTRY
#     ----------
#     """
#     llm_response = extract_agent.run_task(formatted_input)
#     input["llm_output"] = llm_response
# has_errors=any("error" in input for input in final_list)
# end_time=time.time()
# execution_time = end_time - start_time
# final_data={
#     "postcode": query['postcode'],
#     "timestamp": format_timestamp(), 
#     "client": client, 
#     "errors":has_errors, 
#     "execution_time": f"{execution_time:.2f}", 
#     "data":final_list
# }
# with open("data/json/sample_results.json", "w") as f:
#     f.write(json.dumps(final_data))