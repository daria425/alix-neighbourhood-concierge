from abc import ABC, abstractmethod
import requests
from utils import get_search_api_keys
class Search(ABC):
    base_url: str # Class attribute
    """
    Abstract base class for cinteracting with web search APIs.

    This class defines the interface for getting a response from a search API provider.
    """
    def __init__(self, api_key:str):
        if not hasattr(self, "base_url") or not self.base_url:
            raise ValueError("Subclasses must define a `base_url` attribute.")
        self.api_key=api_key
        
    def run_search(self, request_config:dict, kwargs:dict=None):
        """
        Executes a search request.
        
        Args:
        ------
        request_config (dict): Configuration for the request, including method and URL.
            Example:
            {
                "method": "GET" or "POST",
                "url": "https://example.com/api"
            }
        kwargs (dict, optional): Additional parameters for the request, such as headers, 
            query parameters, or request body. E.g., {'json': {}, 'headers': {}}.

        Returns:
        --------
        dict: The response in JSON format, or an error message if an exception occurs.
        """        
        if kwargs is None:
            kwargs = {}
        try:
            if request_config["method"]=="GET":
                response = requests.get(request_config["url"], **kwargs)
            else:
                response=requests.post(request_config["url"], json=request_config.get("request_body", {}),**kwargs)
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            return {"error": f"HTTP error occurred: {http_err}", "status_code": response.status_code}
        except requests.exceptions.RequestException as req_err:
            return {"error": f"Request error occurred: {req_err}"}
        except Exception as err:
            return {"error": f"An unexpected error occurred: {err}"}
    @abstractmethod
    def create_search_request(self, query: str):
        """
        Creates a search request to use with a search API, including the API key

        """
        raise NotImplementedError("Subclasses must implement the `create_search_request` method")
    

class SERPSearch(Search):
    """
    A concrete implementation of the Search class for the SERP API.
    """
    base_url= "https://serpapi.com/search"
    
    def create_search_request(self, query: str, params: dict=None):
        """
        Creates a search URL for the SERP API, adding additional parameters if they are provided.
        
        Args:
        --------
            query: The search query.
            params: Additional query parameters (optional).
        
        Returns:
        --------
        str: A complete URL with query parameters.
        
        """
        url=f"{self.base_url}?api_key={self.api_key}&q={query}"
        if params:
            for key, value in params.items():
                if value is not None: 
                    url += f"&{key}={value}"
        
        return {"method": "GET", "url":url}
    
class TavilySearch(Search):
    """
    A concrete implementation of the Search class for the Tavily API.
    """
    base_url="https://api.tavily.com/search"
    def create_search_request(self, query: str, params: dict=None):
        """
        Creates a search request configuration for the Tavily API, including the URL, HTTP method, 
        and request body with optional additional parameters.

        Args:
        --------
            query (str): The search query to be included in the request body.
            params (dict, optional): Additional query parameters to be added to the request body. 
                Defaults to None.

        Returns:
        --------
            dict: A dictionary containing the request configuration with the following keys:
                - "method" (str): The HTTP method for the request ("POST").
                - "url" (str): The base URL for the API endpoint.
                - "request_body" (dict): The request body, including the query, API key, and 
                any additional parameters.
                
            Example:
            --------
            {
                "method": "POST",
                "url": "https://api.tavily.com/search",
                "request_body": {
                    "query": "example search",
                    "api_key": "your_api_key",
                    "additional_param": "value"
                }
            }
        """
        request_body = {
            "query": query,
            "api_key": self.api_key,
            **(params or {})  # Merge params if provided, otherwise default to an empty dict
        }
        return {
            "method": "POST", "url":self.base_url, "request_body":request_body
        }

    
