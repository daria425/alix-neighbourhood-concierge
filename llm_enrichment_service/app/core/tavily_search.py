
import requests
import os
from dotenv import  load_dotenv
load_dotenv()
tavily_api_key=os.getenv("TAVILY_API_KEY")
class TavilySearch:
    base_url= "https://api.tavily.com/search"
    api_key=tavily_api_key

    def run_search(self, query:str, kwargs=None):
        """
        Executes a search request.

        Args:
        ------
        request_body (dict): Body of the POST request to send to the Tavily API.
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
        request_body=self.create_search_request(query)
        try:
            response = requests.post(
                self.base_url,
                json=request_body,
                **kwargs
            )
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            return {
                "error": f"HTTP error occurred: {http_err}",
                "status_code": response.status_code,
            }
        except requests.exceptions.RequestException as req_err:
            return {"error": f"Request error occurred: {req_err}"}
        except Exception as err:
            return {"error": f"An unexpected error occurred: {err}"}

    def create_search_request(self, query: str):
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
        request_body={
            "query":query, 
            "api_key":self.api_key
        }
        return request_body
    
