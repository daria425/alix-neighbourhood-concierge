from bs4 import BeautifulSoup
from bs4.element import Tag
from utils import format_timestamp, generate_event_id
from typing import List

class HTMLReader():

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
    
    def get_event_detail(self, event_dict: dict, config: dict):
        """
        Extracts detailed information about an event from its HTML content using the provided config.

        Args:
            event_dict (dict): A dictionary containing:
                - 'event_id' (str): The unique identifier for the event.
                - 'content' (str): The raw HTML content of the event details page.
            config (dict): Configuration dictionary defining how to extract details.

        Returns:
            dict: A dictionary containing detailed event information.
        """
        event_details = {"event_id": event_dict["event_id"]}
        detail_sections = []

        if event_dict["content"]:
            soup = self._parse_content(event_dict["content"])

            # Extract main container for details
            details_config = config.get("details", {})
            container_tag = details_config["container"]["tag"]
            container_filter = details_config["container"]["filter"]

            details_container = soup.find(container_tag, **{container_filter.get("parameter", "class_"): container_filter.get("value","")})

            if details_container:
                section_tag = details_config["sections"]["tag"]
                section_filter=details_config["sections"]["filter"]
                info_containers = details_container.find_all(section_tag, **{section_filter.get("parameter", "class_"): section_filter.get("value","")})
                for section in info_containers:
                    text_content = section.get_text(strip=True)
                    links = [link.get("href") for link in section.find_all("a")]
                    detail_sections.append({"content": text_content, "links": links})

        event_details["sections"] = detail_sections
        return event_details
