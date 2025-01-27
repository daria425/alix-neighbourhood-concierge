import json
import time
from agent import EventInfoExtractionAgent
from get_data import get_tavily_dset, get_where_can_we_go_dset
from utils import format_timestamp
postcode="N19QZ"
miles=2
query={
    "postcode":postcode, 
    "miles":miles
}
client="PEABODY"
start_time=time.time()
wcwg_results=get_where_can_we_go_dset(query=query)
tavily_results=get_tavily_dset(query=query)
print("Scraping complete")
final_list=tavily_results+wcwg_results
print(f"Total search results: {len(final_list)}")
extract_agent=EventInfoExtractionAgent()
for input in final_list:
    input_copy = input.copy()
    input_copy["text"] = json.dumps(input_copy)
    formatted_input = f"""
    -----------
    BEGIN ENTRY
    -----------
    {input_copy["text"]}
    ----------
    END ENTRY
    ----------
    """
    llm_response = extract_agent.run_task(formatted_input)
    input["llm_output"] = llm_response
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