from abc import ABC, abstractmethod
import requests
from typing import List
from concurrent.futures import ThreadPoolExecutor

class Search(ABC):
    base_url: str # Class attribute
    """
    Abstract base class for interacting with web search APIs.

    This class defines the interface for getting a response from a search API provider.
    """
    def __init__(self, api_key:str):
        if not hasattr(self, "base_url") or not self.base_url:
            raise ValueError("Subclasses must define a `base_url` attribute.")
        if api_key is None:
            raise ValueError("A valid API key must be provided to initialize a search subclass") # so i dont forget lol
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

class HTMLSearch(ABC):
    """
    Abstract base class for getting HTML content of event listing websites
    """
    base_url: str

    def run_search(self, url, kwargs: dict=None):
        if kwargs is None:
            kwargs = {}
        try:
            response=requests.get(url, **kwargs)
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as http_err:
            return {"error": f"HTTP error occurred: {http_err}", "status_code": response.status_code}
        except requests.exceptions.RequestException as req_err:
            return {"error": f"Request error occurred: {req_err}"}
        except Exception as err:
            return {"error": f"An unexpected error occurred: {err}"}
    
    @abstractmethod
    def create_request_url(self, postcode: str, params:dict=None):
        """
        Creates a search request url to scrape (for event listing websites)
        """
        raise NotImplementedError("Subclasses must implement the `create_search_url` method")
    def _fetch_event(self,event:str)->dict:
        """
        Fetches HTML content for an individual event.

        Args:
        ------
            event (dict): A dictionary containing event metadata, including a `url`.

        Returns:
        --------
        dict: {
        html_content: The response from the `url`, 
        event_id: ID of the event passed in
        } or an error message.
        """
        url=event.get("url")
        event_id=event.get("event_id")
        if url and event_id:
            html_content=self.run_search(url, kwargs={})
            return {
                "content": html_content, 
                "event_id": event_id
            }
        return {"error": "No URL/event id provided"}
    
    def fetch_event_details(self, event_metadata:List[dict]):
        """
        Fetches detailed HTML content for a list of events concurrently.

        Args:
        ------
            event_metadata (List[dict]): A list of dictionaries containing event metadata.

        Returns:
        --------
        List[dict]: A list of responses from the `url` of the events.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self._fetch_event, event) for event in event_metadata]
            return [future.result() for future in futures]
    
class WhereCanWeGoSearch(HTMLSearch):
    """
    A concrete implementation of the HTMLSearch class for the WhereCanWeGo website.
    """
    base_url="https://www.wherecanwego.com/whats-on/"
    def create_request_url(self, postcode:str, params:dict=None):
        """
        Creates a search URL for scraping a WhereCanWeGo webpage for a given postcode, adding additional parameters if they are provided.
        
        Args:
        --------
            postcode: The postcode to search for.
            params: Additional query parameters (optional).
        
        Returns:
        --------
        str: A complete URL with query parameters.
        
        """

        url=f"{self.base_url}{postcode}?id=7" #default to weekly events for now
        if params:
            for key, value in params.items():
                if value is not None: 
                    url += f"&{key}={value}"
        return url

class IslingtonLifeSearch(HTMLSearch):
    base_url="https://islingtonlife.london/things-to-do/"
    def create_request_url(self):
        return self.base_url
    
class TrinityIslingtonSearch(HTMLSearch):
    base_url="https://trinityislington.org/whats-happening"
    def create_request_url(self):
        return self.base_url
    
class Centre404Search(HTMLSearch):
    base_url="https://centre404.org.uk/blog/"
    def create_request_url(self):
        return self.base_url
    
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

    
