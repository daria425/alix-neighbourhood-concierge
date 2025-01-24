import os
from dotenv import load_dotenv
load_dotenv()

def get_search_api_keys()->dict:
    """
    Retrieves API keys for both SERP and Tavily API providers from environment variables.
    
    The function fetches the API keys stored in the environment variables `SERP_API_KEY` and 
    `TAVILY_API_KEY`, and returns them in a dictionary.

    Returns
    -------
    dict
        A dictionary containing the API keys for both providers. The dictionary has the following structure:
        {
            "serp": <SERP_API_KEY>,
            "tavily": <TAVILY_API_KEY>
        }

    """
    serp_api_key=os.getenv("SERP_API_KEY")
    tavily_api_key=os.getenv("TAVILY_API_KEY")
    return {
        "serp": serp_api_key, "tavily":tavily_api_key
    }
