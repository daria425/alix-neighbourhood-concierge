from bs4 import BeautifulSoup
from bs4.element import Tag
from typing import List
from abc import ABC, abstractmethod
import re
class HTMLReader(ABC):
    """
    Absract base class for reading the HTML content of a page.  
    Defines the interface for parsing HTML content and returning event information.
    """
    def _parse_content(self, content: str) -> BeautifulSoup:
        """
        Parses the provided HTML content into a BeautifulSoup object.

        Args:
            content (str): The raw HTML content to parse.

        Returns:
            BeautifulSoup: Parsed HTML content.
        """
        return BeautifulSoup(content, "html.parser")
    @abstractmethod
    def get_event_results(self, content:str)->List[Tag]:
        """
        Ensures that subclasses implement the `get_event_results` method
        """
        raise NotImplementedError("Subclasses must implement the `get_event_results` method")
    @abstractmethod
    def get_event_metadata(self)->List[Tag]:
        """
        Ensures that subclasses implement the `get_event_metadata` method
        """
        raise NotImplementedError("Subclasses must implement the `get_event_metadata` method")
    @abstractmethod
    def get_event_detail(self, content:str)->List[Tag]:
        """
        Ensures that subclasses implement the `get_event_detail` method
        """
        raise NotImplementedError("Subclasses must implement the `get_event_detail` method")

class WhereCanWeGoReader(HTMLReader):  
    def get_event_results(self, content)->List[Tag]:
        """
        Finds and returns all event result containers in the HTML.

        Returns:
            list: A list of BeautifulSoup elements containing the event results.
        """
        soup=self._parse_content(content)
        event_results=soup.find_all("div", class_="EventResults")
        return event_results

    def get_event_metadata(self)->List[dict]:
        """
        Extracts metadata for an event from the HTML content.

        The metadata includes:
        - Event title
        - Event description
        - Event location
        - URL for more information

        Returns:
            List[dict]: A list of dictionaries containing the following keys:
                - 'event_title' (str): The title of the event.
                - 'description' (str): A truncated description of the event.
                - 'location' (str): The location where the event will be held.
                - 'more_info_url' (str): The URL linking to more information about the event.
        """
        event_results=self.get_event_results()
        event_metadata = [
        {
            "event_title": result.find("h2", class_="eventtitle")
                                .find("a", id=re.compile("EventRepeater"))
                                .text.replace("\n", "").strip(),
            "description": result.find("div", class_="description")
                                 .text.replace("\n", "").replace("more >", "").strip(),
            "location": result.find("div", class_="VenueLine")
                              .text.replace("\n", "").strip(),
            "more_info_url": result.find("h2", class_="eventtitle")
                                   .find("a", id=re.compile("EventRepeater"))
                                   .get("href"),
            "event_id": result.find("h2", class_="eventtitle")
                                   .find("a", id=re.compile("EventRepeater"))
                                   .get("href").split("/")[-1]
        }
        for result in event_results
    ]
        print(event_metadata[0])
        return event_metadata
    
    def get_event_detail(self, content:str):
        soup=self._parse_content(content)
        info_containers=soup.find_all("div", class_="spacing")
        event_details={}
        for i in range(0, len(info_containers)):
            text_content=info_containers[i].text
            links=[link.get("href") for link in info_containers[i].find_all("a")]
            event_details[f'container_{i}_content']={
                "text_content": text_content, 
                "links":links
            }
        return event_details



