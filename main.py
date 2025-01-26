import json
import time
from agent import EventInfoExtractionAgent
from get_data import get_tavily_dset, get_where_can_we_go_dset
postcode="N19QZ"
miles=2
query={
    "postcode":postcode, 
    "miles":miles
}
wcwg_results=get_where_can_we_go_dset(query=query)
tavily_results=get_tavily_dset(query=query)
# final_list=tavily_results+wcwg_results
# extract_agent=EventInfoExtractionAgent()
# for input in final_list:
#     # Create a copy of the dictionary to avoid modifying it prematurely
#     input_copy = input.copy()

#     # Convert the dictionary into a JSON-formatted string
#     input_copy["text"] = json.dumps(input_copy)

#     # Format the input for the LLM
#     formatted_input = f"""
#     -----------
#     BEGIN ENTRY
#     -----------
#     {input_copy["text"]}
#     ----------
#     END ENTRY
#     ----------
#     """

#     # Run the LLM task and capture the response
#     llm_response = extract_agent.run_task(formatted_input)

#     # Store the LLM output in the original dictionary
#     input["llm_output"] = llm_response
# with open("test.json",  "w") as f:
#     f.write(json.dumps(final_list))
