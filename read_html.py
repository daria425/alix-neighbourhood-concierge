from bs4 import BeautifulSoup
from bs4.element import Tag
from typing import List
from abc import ABC, abstractmethod
import re
from uuid import uuid4
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
    def get_event_metadata(self, content:str)->List[Tag]:
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
    domain="www.wherecanwego.com" 
    def get_event_results(self, content)->List[Tag]:
        """
        Finds and returns all event result containers in the HTML.

        Returns:
            list: A list of BeautifulSoup elements containing the event results.
        """
        soup=self._parse_content(content)
        event_results=soup.find_all("div", class_="EventResults")
        return event_results

    def get_event_metadata(self, content)->List[dict]:
        """
        Extracts metadata for an event from the HTML content.

        The metadata includes:
         -Event provider domain
        - Event title
        - Event description
        - Event location
        - URL for more information
        -Event ID to match detail contents by

        Returns:
            List[dict]: A list of dictionaries containing the following keys:
                - 'title' (str): The title of the event.
                - 'description' (str): A truncated description of the event.
                - 'location' (str): The location where the event will be held.
                - 'url' (str): The URL linking to more information about the event.
        """
        event_results=self.get_event_results(content)
        event_metadata = [
        {
            "domain": self.domain,
            "title": result.find("h2", class_="eventtitle")
                                .find("a", id=re.compile("EventRepeater"))
                                .text.replace("\n", "").strip(),
            "content": result.find("div", class_="description")
                                 .text.replace("\n", "").replace("more >", "").strip(),
            "location": result.find("div", class_="VenueLine")
                              .text.replace("\n", "").strip(),
            "url": result.find("h2", class_="eventtitle")
                                   .find("a", id=re.compile("EventRepeater"))
                                   .get("href"),
            "event_id": str(uuid4())
        }
        for result in event_results
    ]
        return event_metadata
    
    def get_event_detail(self, event_dict:dict):
        """
        Extracts detailed information about an event from its HTML content.

        Args:
            event_dict (dict): A dictionary containing the following keys:
                - 'event_id' (str): The unique identifier for the event.
                - 'html_content' (str): The raw HTML content of the event details page.

        Returns:
            dict: A dictionary containing detailed information about the event, with the following structure:
                - 'event_id' (str): The unique identifier for the event.
                - 'sections' (list): A list of sections, where each section is a dictionary containing:
                    - 'text_content' (str): The textual content of the section.
                    - 'links' (list): A list of hyperlinks found within the section.
        """
        soup=self._parse_content(event_dict["html_content"])
        info_containers=soup.find_all("div", class_="spacing")
        event_details={"event_id":event_dict["event_id"]}
        detail_sections=[]
        for i in range(0, len(info_containers)):
            text_content=info_containers[i].text
            links=[link.get("href") for link in info_containers[i].find_all("a")]
            section_content={
                "content": text_content, 
                "links":links
            }
            detail_sections.append(section_content)
        event_details["sections"]=detail_sections
        return event_details



