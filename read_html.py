from bs4 import BeautifulSoup
from bs4.element import Tag
from utils import format_timestamp, generate_event_id
from typing import List
from abc import ABC, abstractmethod
import re

#TO-DO use get_text()


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
    def get_event_results(self, content: str) -> List[Tag]:
        """
        Ensures that subclasses implement the `get_event_results` method
        """
        raise NotImplementedError(
            "Subclasses must implement the `get_event_results` method"
        )

    @abstractmethod
    def get_event_metadata(self, content: str) -> List[Tag]:
        """
        Ensures that subclasses implement the `get_event_metadata` method
        """
        raise NotImplementedError(
            "Subclasses must implement the `get_event_metadata` method"
        )

    @abstractmethod
    def get_event_detail(self, content: str) -> List[Tag]:
        """
        Ensures that subclasses implement the `get_event_detail` method
        """
        raise NotImplementedError(
            "Subclasses must implement the `get_event_detail` method"
        )


class WhereCanWeGoReader(HTMLReader):
    domain = "wherecanwego.com"

    def get_event_results(self, content) -> List[Tag]:
        """
        Finds and returns all event result containers in the HTML.

        Returns:
            list: A list of BeautifulSoup elements containing the event results.
        """
        soup = self._parse_content(content)
        event_results = soup.find_all("div", class_="EventResults")
        return event_results

    def get_event_metadata(self, content) -> List[dict]:
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
                -'timestamp'(str): ISO formatted time string of when the scraping was executed
        """
        event_results = self.get_event_results(content)
        print(len(event_results))
        event_metadata = [
            {
                "domain": self.domain,
                "title": result.find("h2", class_="eventtitle")
                .find("a", id=re.compile("EventRepeater"))
                .text.replace("\n", "")
                .strip(),
                "content": result.find("div", class_="description")
                .text.replace("\n", "")
                .replace("more >", "")
                .strip(),
                "location": result.find("div", class_="VenueLine")
                .text.replace("\n", "")
                .strip(),
                "url": result.find("h2", class_="eventtitle")
                .find("a", id=re.compile("EventRepeater"))
                .get("href"),
                "timestamp": format_timestamp(),
            }
            for result in event_results
        ]
        for e in event_metadata:
            e["event_id"] = generate_event_id(e)
        return event_metadata

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


class IslingtonLifeReader(HTMLReader):
    domain = "islingtonlife.london"

    def get_event_results(self, content):
        soup = self._parse_content(content)
        event_results = soup.find_all("div", class_="card__item card__item--wide")
        print(len(event_results))
        return event_results

    def get_event_metadata(self, content) -> List[dict]:
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
                - 'timestamp'(str): ISO formatted time string of when the scraping was executed
        """
        event_results = self.get_event_results(content)
        event_metadata = [
            {
                "domain": self.domain,
                "title": result.find("h2", class_="card__item__title u-color--red")
                .text.replace("\n", "")
                .strip(),
                "content": result.find("p", class_="card__item__teaser u-color--black")
                .text.replace("\n", "")
                .strip(),
                "url": result.find("a", class_="card__item__container").get("href"),
                "timestamp": format_timestamp(),
            }
            for result in event_results
        ]
        for e in event_metadata:
            e["event_id"] = generate_event_id(e)
        return event_metadata

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


class TrinityIslingtonReader(HTMLReader):
    domain = "trinityislington.org"

    def get_event_results(self, content):
        soup = self._parse_content(content)
        event_results = soup.find_all(
            "div", class_="image-card sqs-dynamic-text-container"
        )
        return event_results

    def get_event_metadata(self, content):
        event_results = self.get_event_results(content)
        event_metadata = [
            {
                "domain": self.domain,
                "title": result.find("div", class_="image-title-wrapper")
                .text.replace("\n", "")
                .strip(),
                "url": f"https://{self.domain}/whats-happening",
                "timestamp": format_timestamp(),
                "event_detail": self.get_event_detail(result),
            }
            for result in event_results
        ]
        for e in event_metadata:
            unique_id = generate_event_id(e)
            e["event_id"] = unique_id
            e["event_detail"]["event_id"] = unique_id
        return event_metadata

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
    domain="centre404.org.uk"
    def get_event_results(self, content):
        soup = self._parse_content(content)
        event_results = soup.find_all(
            "div", class_="news-post clearfix"
        )
        return event_results
    def get_event_metadata(self, content):
        event_results = self.get_event_results(content)
        event_metadata = [
            {
                "domain": self.domain,
                "title": result.find("div", class_="title-bar clearfix")
                .get_text(strip=True),
                "content": result.find("div", class_="short-description").get_text(strip=True),
                "url": result.find("a", class_="read-more").get("href") ,
                "timestamp": format_timestamp(),
            }
            for result in event_results
        ]
        for e in event_metadata:
            e["event_id"] = generate_event_id(e)
        return event_metadata
    def get_event_detail(self, content):
        pass
        
        

