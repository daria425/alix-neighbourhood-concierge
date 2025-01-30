from bs4 import BeautifulSoup
from bs4.element import Tag
from utils import format_timestamp, generate_event_id
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
    
    def get_event_metadata(self, content: str, config:dict ) -> List[Tag]:
        """
        Extracts common event metadata (title, description, URL).
        
        Args:
            result (Tag): The BeautifulSoup element containing the event data.
            title_tag (str): The tag or class used to find the event title.
            description_tag (str): The tag or class used to find the event description.
            url_tag (str): The tag or class used to find the event URL.
        
        Returns:
            dict: A dictionary containing the event's title, description, and URL.
        """
        event_results=self.get_event_result_containers(content, config['container'])
        title_config=config['title']
        url_config=config['url']
        description_config=config['content']
        event_metadata=[
             {
                    "domain": config["domain"],
        "title": result.find(title_config.get("tag"), **{
            title_config["filter"].get("parameter", "class_"): title_config["filter"].get("value", "")
        }).get_text(strip=True) if result.find(title_config.get("tag"), **{
            title_config["filter"].get("parameter", "class_"): title_config["filter"].get("value", "")
        }) else "",

        "url": result.find(url_config.get("tag"), **{
            url_config["filter"].get("parameter", "class_"): url_config["filter"].get("value", "")
        }).get("href", "") if result.find(url_config.get("tag"), **{
            url_config["filter"].get("parameter", "class_"): url_config["filter"].get("value", "")
        }) else "",

        "content": result.find(description_config.get("tag"), **{
            description_config["filter"].get("parameter", "class_"): description_config["filter"].get("value", "")
        }).get_text(strip=True) if result.find(description_config.get("tag"), **{
            description_config["filter"].get("parameter", "class_"): description_config["filter"].get("value", "")
        }) else "",

        "timestamp": format_timestamp()
    
        }
        for result in event_results
        ]
        for e in event_metadata:
            e["event_id"] = generate_event_id(e)
        return event_metadata



    @abstractmethod
    def get_event_detail(self, content: str) -> List[Tag]:
        """
        Ensures that subclasses implement the `get_event_detail` method
        """
        raise NotImplementedError(
            "Subclasses must implement the `get_event_detail` method"
        )
    
    def get_event_result_containers(self, content:str, config:dict) -> List[Tag]:
        """
        Finds and returns all event result containers in the HTML.

        Returns:
            list: A list of BeautifulSoup elements containing the event results.
        """
        soup = self._parse_content(content)
        tag=config.get("tag", None)
        filter_param = config["filter"].get("parameter", "class_")
        filter_value = config["filter"].get("value", "")
        event_results = soup.find_all(tag, **{filter_param: filter_value})
        return event_results

class WhereCanWeGoReader(HTMLReader):

    def get_event_detail(self, event_dict: dict):
        """
        Extracts detailed information about an event from its HTML content.

        Args:
            event_dict (dict): A dictionary containing the following keys:
                - 'event_id' (str): The unique identifier for the event.
                - 'content' (str): The raw HTML content of the event details page.

        Returns:
            dict: A dictionary containing detailed information about the event, with the following structure:
                - 'event_id' (str): The unique identifier for the event.
                - 'sections' (list): A list of sections, where each section is a dictionary containing:
                    - 'content' (str): The textual content of the section.
                    - 'links' (list): A list of hyperlinks found within the section.
        """
        event_details = {"event_id": event_dict["event_id"]}
        detail_sections = []
        if event_dict["content"] != "":
            soup = self._parse_content(event_dict["content"])
            info_containers = soup.find_all("div", class_="spacing")
            for i in range(0, len(info_containers)):
                text_content = info_containers[i].text
                links = [link.get("href") for link in info_containers[i].find_all("a")]
                section_content = {"content": text_content, "links": links}
                detail_sections.append(section_content)
        event_details["sections"] = detail_sections
        return event_details

class TrinityIslingtonReader(HTMLReader):

    def get_event_detail(self, event_result: Tag):
        detail_sections = []
        event_details = {}
        info_containers = event_result.find(
            "div", class_="image-subtitle sqs-dynamic-text"
        ).find_all("p")
        for i in range(0, len(info_containers)):
            text_content = info_containers[i].text
            links = [link.get("href") for link in info_containers[i].find_all("a")]
            section_content = {"content": text_content, "links": links}
            detail_sections.append(section_content)
        event_details["sections"] = detail_sections
        return event_details

class Centre404Reader(HTMLReader):
    def get_event_detail(self, event_dict:dict):
        detail_sections = []
        event_details = {"event_id": event_dict["event_id"]}
        if event_dict["content"] != "":
            soup = self._parse_content(event_dict["content"])
            info_containers = soup.find(
                "div", class_="copy-wrapper"
            ).find_all("p")
            for i in range(0, len(info_containers)):
                text_content = info_containers[i].get_text()
                links = [link.get("href") for link in info_containers[i].find_all("a")]
                section_content = {"content": text_content, "links": links}
                detail_sections.append(section_content)
        print(detail_sections)
        event_details["sections"] = detail_sections
        return event_details
        
        

class IslingtonLifeReader(HTMLReader):
    domain = "islingtonlife.london"

    def get_event_detail(self, event_dict: dict):
        """
        Extracts detailed information about an event from its HTML content.

        Args:
            event_dict (dict): A dictionary containing the following keys:
                - 'event_id' (str): The unique identifier for the event.
                - 'content' (str): The raw HTML content of the event details page.

        Returns:
            dict: A dictionary containing detailed information about the event, with the following structure:
                - 'event_id' (str): The unique identifier for the event.
                - 'sections' (list): A list of sections, where each section is a dictionary containing:
                    - 'content' (str): The textual content of the section.
                    - 'links' (list): A list of hyperlinks found within the section.
        """
        detail_sections = []
        event_details = {"event_id": event_dict["event_id"]}
        if event_dict["content"] != "":
            soup = self._parse_content(event_dict["content"])
            info_containers = soup.find(
                "div", class_="entry__body__container"
            ).find_all("p")
            for i in range(0, len(info_containers)):
                text_content = info_containers[i].text
                links = [link.get("href") for link in info_containers[i].find_all("a")]
                section_content = {"content": text_content, "links": links}
                detail_sections.append(section_content)
        event_details["sections"] = detail_sections
        return event_details



        

