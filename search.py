from abc import ABC, abstractmethod
import requests
from typing import List
from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor
import logging
from utils import get_locator_str


class APIWebSearch(ABC):
    base_url: str  # Class attribute
    """
    Abstract base class for interacting with web search APIs.

    This class defines the interface for getting a response from a search API provider.
    """

    def __init__(self, api_key: str):
        if not hasattr(self, "base_url") or not self.base_url:
            raise ValueError("Subclasses must define a `base_url` attribute.")
        if api_key is None:
            raise ValueError(
                "A valid API key must be provided to initialize a search subclass"
            )  # so i dont forget lol
        self.api_key = api_key

    def run_search(self, request_config: dict, kwargs: dict = None):
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
            response = requests.post(
                request_config["url"],
                json=request_config.get("request_body", {}),
                **kwargs,
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

    @abstractmethod
    def create_search_request(self, query: str):
        """
        Creates a search request to use with a search API, including the API key
        """
        raise NotImplementedError(
            "Subclasses must implement the `create_search_request` method"
        )


class WebsiteSearch(ABC):
    def __init__(self, website: str):
        self.website = website
        self.base_url = self.get_base_url()
        self._modify_url = self.get_modify_method()

    @abstractmethod
    def get_base_url(self):
        """
        Gets the base url based off the website passed in and a url map in the subclass
        """
        raise NotImplementedError(
            "Subclasses must implement the `create_base_url` method"
        )

    @abstractmethod
    def run_search(self, url):
        """
        Executes a search request with a given url using either requests or Playwright
        """
        raise NotImplementedError("Subclasses must implement the `run_search` method")

    def get_modify_method(self):
        return getattr(
            self, f"_modify_{self.website}", lambda *args, **kwargs: self.base_url
        )

    def create_request_url(self, *args, **kwargs):
        return self._modify_url(*args, **kwargs)

    def _fetch_event(self, event: str) -> dict:
        """
        Fetches HTML content for an individual event.

        Args:
        ------
            event (dict): A dictionary containing event metadata, including a `url`.

        Returns:
        --------
        dict: {
            "content": The response from the `url`,
            "event_id": ID of the event passed in,
        } or an empty content string in case of an error.
        """
        url = event.get("url")
        event_id = event.get("event_id")
        if not url or not event_id:
            return {"error": "No URL/event id provided"}

        response = self.run_search(url, kwargs={})

        if response.get("content"):
            return {"content": response["content"], "event_id": event_id}
        status_code = response.get("status_code", "Unknown")
        logging.warning(
            f"Error fetching event {event_id}: {response.get('error', '')} (Status: {status_code})"
        )

        return {"content": "", "event_id": event_id}

    def fetch_event_details(self, event_metadata: List[dict]):
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
            futures = [
                executor.submit(self._fetch_event, event) for event in event_metadata
            ]
            return [future.result() for future in futures]


class HTMLSearch(WebsiteSearch):
    def __init__(self, website: str):
        super().__init__(website)

    def get_base_url(self) -> str:
        urls = {
            "wherecanwego": "https://www.wherecanwego.com/whats-on/",
            "islingtonlife": "https://islingtonlife.london/things-to-do/",
            "trinityislington": "https://trinityislington.org/whats-happening",
            "centre404": "https://centre404.org.uk/blog/",
        }
        return urls.get(self.website, "")

    def _modify_wherecanwego(self, postcode: str, params: dict = None):
        url = f"{self.base_url}{postcode}?id=7"
        if params:
            for key, value in params.items():
                if value is not None:
                    url += f"&{key}={value}"
        return url

    def run_search(self, url, kwargs: dict = None):
        kwargs = kwargs or {}

        try:
            response = requests.get(url, **kwargs)
            response.raise_for_status()
            return {"content": response.text}

        except requests.exceptions.HTTPError as http_err:
            status_code = response.status_code if response else "Unknown"
            logging.error(f"HTTP error for {url}: {http_err} (Status: {status_code})")
            return {
                "error": f"HTTP error occurred: {http_err}",
                "status_code": status_code,
            }

        except requests.exceptions.RequestException as req_err:
            logging.error(f"Request error for {url}: {req_err}")
            return {"error": f"Request error occurred: {req_err}", "status_code": None}

        except Exception as err:
            logging.exception(f"Unexpected error for {url}: {err}")
            return {
                "error": f"An unexpected error occurred: {err}",
                "status_code": None,
            }


class DynamicSearch(WebsiteSearch):
    def __init__(self, website: str):
        super().__init__(website)

    def get_base_url(self):
        urls = {"eventbrite": "https://www.eventbrite.co.uk/"}
        return urls.get(self.website, "")

    def _modify_eventbrite(self, organizer_id):
        return f"{self.base_url}o/{organizer_id}"

    def run_search(self, url: str, locator_config: dict):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")
            try:
                locator_str = get_locator_str(locator_config)
                locator = page.locator(locator_str).first
                locator.wait_for(state="attached", timeout=60000)
                content = page.content()
                return {"content": content}
            except Exception as err:
                logging.exception(f"Unexpected error for {url}: {err}")
                return {
                    "error": f"An unexpected error occurred: {err}",
                    "status_code": None,
                }
            finally:
                browser.close()

locator_config={
    "tag":"h3", 
    "filter":{
        "parameter": "class", "value": "Typography_root__487rx"
    }
}
# organizer_id="the-garden-classroom-76146096453"
# searcher=DynamicSearch(website="eventbrite")
# url=searcher.create_request_url(organizer_id)
# html=searcher.run_search(url, locator_config)
# with open("eventbrite_html.html", "w") as f:
#     f.write(html['content'])
class TavilySearch(APIWebSearch):
    """
    A concrete implementation of the Search class for the Tavily API.
    """

    base_url = "https://api.tavily.com/search"

    def create_search_request(self, query: str, params: dict = None):
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
            **(
                params or {}
            ),  # Merge params if provided, otherwise default to an empty dict
        }
        return {"method": "POST", "url": self.base_url, "request_body": request_body}
