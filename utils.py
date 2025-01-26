import os
from dotenv import load_dotenv
from typing import List
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

def validate_query(query: dict, required_keys: List[str]) -> None:
    """
    Validates that the query dictionary contains all the required keys.

    Args:
        query (dict): The input query dictionary to validate.
        required_keys (List[str]): A list of required keys.

    Raises:
        ValueError: If any of the required keys are missing.
    """
    missing_keys = set(required_keys) - set(query.keys())
    if missing_keys:
        raise ValueError(f"Missing required keys in query: {', '.join(missing_keys)}")
