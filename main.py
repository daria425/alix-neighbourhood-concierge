import json
import time
from agent import EventInfoExtractionAgent

start_time=time.time()
with open("data/json/tavily_sample_results.json") as f:
    tavily_results=json.loads(f.read())
with open("data/json/wherecanwego_sample_results.json") as f:
    wcwg_results=json.loads(f.read())

final_list=tavily_results+wcwg_results
extract_agent=EventInfoExtractionAgent()
for input in final_list:
    # Create a copy of the dictionary to avoid modifying it prematurely
    input_copy = input.copy()

    # Convert the dictionary into a JSON-formatted string
    input_copy["text"] = json.dumps(input_copy)

    # Format the input for the LLM
    formatted_input = f"""
    -----------
    BEGIN ENTRY
    -----------
    {input_copy["text"]}
    ----------
    END ENTRY
    ----------
    """

    # Run the LLM task and capture the response
    llm_response = extract_agent.run_task(formatted_input)

    # Store the LLM output in the original dictionary
    input["llm_output"] = llm_response
with open("test.json",  "w") as f:
    f.write(json.dumps(final_list))

end_time = time.time()

# Calculate the execution time
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.2f} seconds")