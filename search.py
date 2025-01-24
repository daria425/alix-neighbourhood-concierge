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
        
    def run_search(self, url:str, kwargs):
        """
        Executes a search request.
        
        :param url: The URL to send the request to.
        :param kwargs: Optional parameters for the request, e.g., headers, params, etc.
        """
        # Pass optional parameters to the requests.get method
        try:
            response = requests.get(url, **kwargs)
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            return {"error": f"HTTP error occurred: {http_err}", "status_code": response.status_code}
        except requests.exceptions.RequestException as req_err:
            return {"error": f"Request error occurred: {req_err}"}
        except Exception as err:
            return {"error": f"An unexpected error occurred: {err}"}
    @abstractmethod
    def create_search_url(self, query: str):
        """
        Creates a search url to use with a search API, including the API key

        """
        raise NotImplementedError("Subclasses must implement the `create_model` method")
    

class SERPSearch(Search):
    """
    A concrete implementation of the Search class for the SERP API.
    """
    base_url= "https://serpapi.com/search"
    
    def create_search_url(self, query: str, params: dict=None):
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
                if value is not None:  # Only add parameters with non-None values
                    url += f"&{key}={value}"
        
        return url
    
class TavilySearch(Search):
    """
    A concrete implementation of the Search class for the Tavily API.
    """
    base_url="https://api.tavily.com/search"
    def create_search_url(self, query: str, params: dict=None):
        """
        Creates a search URL for the Tavily API, adding additional parameters if they are provided.
        
        Args:
        --------
            query: The search query.
            params: Additional query parameters (optional).
        
        Returns:
        --------
        str: A complete URL with query parameters.
        """
        url=f"{self.base_url}?api_key={self.api_key}&query={query}"
        if params:
            for key, value in params.items():
                if value is not None:  # Only add parameters with non-None values
                    url += f"&{key}={value}"
        
        return url


    
