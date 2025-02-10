from abc import ABC, abstractmethod
import requests
from typing import List
from playwright.async_api import async_playwright
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging

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
    async def run_search(self, url):
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

    async def _fetch_event(self, event: str) -> dict:
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
        if asyncio.iscoroutinefunction(self.run_search):
            response=await self.run_search(url, kwargs={})
        else:
            response = self.run_search(url, kwargs={})
        if response.get("content"):
            return {"content": response["content"], "event_id": event_id}
        status_code = response.get("status_code", "Unknown")
        logging.warning(
            f"Error fetching event {event_id}: {response.get('error', '')} (Status: {status_code})"
        )

        return {"content": "", "event_id": event_id}
    
    def _fetch_event_sync(self, event: str)->dict:
        """Sync version of `_fetch_event()` for use with `run_in_executor`."""
        return asyncio.run(self._fetch_event(event)) 



    async def fetch_event_details(self, event_metadata: List[dict]):
        """
        Fetches detailed HTML content for a list of events concurrently (handles async/sync methods).

        Args:
        ------
            event_metadata (List[dict]): A list of dictionaries containing event metadata.

        Returns:
        --------
        List[dict]: A list of responses from the `url` of the events.
        """
        if asyncio.iscoroutinefunction(self.run_search):
            print("Running async run_search")
            tasks = [self._fetch_event(event) for event in event_metadata]
            return await asyncio.gather(*tasks)
        else:
            print("Running sync run_search")
            loop = asyncio.get_running_loop()
            with ThreadPoolExecutor() as executor:
                tasks = [loop.run_in_executor(executor, self._fetch_event_sync, event) for event in event_metadata]  # Use a sync version
            return await asyncio.gather(*tasks)


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
        if "miles" in params:
            url=f"{self.base_url}{postcode}?id=7&miles={params['miles']}" 
        print(url)
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
        urls = {"the-garden-classroom-76146096453": "https://www.eventbrite.co.uk/o/the-garden-classroom-76146096453",
                "praxis-17432513338":"https://www.eventbrite.co.uk/o/praxis-17432513338", 
                "mary's_youth_club":"https://www.marys.org.uk/youthclub/timetable/"
                }
        
        return urls.get(self.website, "")


    async def run_search(self, url: str, locator_config: dict):
        TIMEOUT=60000
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, wait_until="networkidle")
            try:
                locator_str=locator_config['selector']
                locator = page.locator(locator_str).first
                await locator.wait_for(state="attached", timeout=TIMEOUT)
                content = await page.content()
                return {"content": content}
            except Exception as err:
                logging.exception(f"Unexpected error for {url}: {err}")
                return {
                    "error": f"An unexpected error occurred: {err}",
                    "status_code": None,
                }
            finally:
                await browser.close()

