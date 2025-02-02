from bs4 import BeautifulSoup
from bs4.element import Tag
from utils import format_timestamp, generate_event_id
from typing import List

class HTMLReader:
    def __init__(self, page_content_config:dict):
        self.config=page_content_config

    def extract_text(self,result, config):
        """Extract text using find() or select_one() if CSS selector is provided."""
        if not config:
            return ""

        if "selector" in config:  # Use CSS selector if available
            element = result.select_one(config["selector"])
        else:  # Fallback to traditional find()
            tag = config.get("tag")
            filter_param = config["filter"].get("parameter", "class_")
            filter_value = config["filter"].get("value", "")
            element = result.find(tag, **{filter_param: filter_value})
        return element.get_text(strip=True) if element else ""

    def extract_url(self, result, config):
        """Extract URL using find() or select_one() if CSS selector is provided."""
        if not config:
            return ""

        if "selector" in config:  # Use CSS selector if available
            element = result.select_one(config["selector"])
        else:  # Fallback to traditional find()
            tag = config.get("tag")
            filter_param = config["filter"].get("parameter", "class_")
            filter_value = config["filter"].get("value", "")
            element = result.find(tag, **{filter_param: filter_value})

        return element.get("href", "") if element else ""

        
    def _parse_content(self, content: str) -> BeautifulSoup:
        """
        Parses the provided HTML content into a BeautifulSoup object.

        Args:
            content (str): The raw HTML content to parse.

        Returns:
            BeautifulSoup: Parsed HTML content.
        """

        return BeautifulSoup(content, "html.parser")
    
    def get_event_metadata(self, content: str, include_event_details=False) -> List[Tag]:
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
        event_results=self._get_event_result_containers(content, self.config['container'])
        title_config=self.config['title']
        url_config=self.config['url']
        description_config=self.config['content']
        event_metadata=[
             {
        "domain": self.config["domain"],
        "title": self.extract_text(result, title_config),
        "url": self.extract_url(result, url_config),
        "content": self.extract_text(result, description_config),
        "timestamp": format_timestamp(),
        "html":str(result) if result else ""
        }
        for result in event_results
        ]
        for e in event_metadata:
            id= generate_event_id(e)
            e['event_id']=id
            if include_event_details:
                event_dict={'event_id':id, "content":e['html']}
                event_details=self.get_event_detail(event_dict)
                e['event_details']=event_details
                e.pop('html')
        return event_metadata
    def _get_event_result_containers(self, content:str, config:dict) -> List[Tag]:
        """
        Finds and returns all event result containers in the HTML.

        Returns:
            list: A list of BeautifulSoup elements containing the event results.
        """
        soup = self._parse_content(content)
        if 'selector' in config:
            event_results=soup.select(config['selector'])
        else:
            tag=config.get("tag", None)
            filter_param = config["filter"].get("parameter", "class_")
            filter_value = config["filter"].get("value", "")
            event_results = soup.find_all(tag, **{filter_param: filter_value})
        return event_results
    
    def get_event_detail(self, event_dict: dict):
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
        if 'content' not in event_dict or event_dict['content'] is None:
            raise ValueError(f"event_dict['content'] is missing or None: {event_dict}")
        if event_dict["content"]:
            soup = self._parse_content(event_dict['content'])
            details_config = self.config.get("details", {})
            container_tag = details_config["container"]["tag"]
            container_filter = details_config["container"]["filter"]

            details_container = soup.find(container_tag, **{container_filter.get("parameter", "class_"): container_filter.get("value","")})
            if details_container:
                section_tag = details_config["sections"]["tag"]
                section_filter=details_config["sections"]["filter"]
                if section_filter:
                    info_containers = details_container.find_all(
                        section_tag, **{section_filter.get("parameter", "class_"): section_filter.get("value", "")}
                    )
                else:
                    info_containers = details_container.find_all(section_tag)
                for section in info_containers:
                    text_content = section.get_text(strip=True)
                    links = [link.get("href") for link in section.find_all("a")]
                    detail_sections.append({"content": text_content, "links": links})

        event_details["sections"] = detail_sections
        return event_details
