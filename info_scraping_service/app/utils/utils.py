import os
import hashlib
from dotenv import load_dotenv
from typing import List
from datetime import datetime, timezone
from app.models.event import Event
from typing import List

load_dotenv()


def validate_query(query: dict, required_keys: List[str]) -> None:
    """
    Validates that the query dictionary contains all the required keys.

    Args:
        query (dict): The input query dictionary to validate.
        required_keys (List[str]): A list of required keys.

    Raises:
        ValueError: If any of the required keys are missing.
    """
    missing_keys = set(required_keys) - set(query.keys())
    if missing_keys:
        raise ValueError(f"Missing required keys in query: {', '.join(missing_keys)}")

def format_timestamp():
    current_timestamp = datetime.now(timezone.utc)
    iso_timestamp = current_timestamp.isoformat() + "Z"
    return iso_timestamp


def generate_event_id(event: dict) -> str:
    # Extract relevant fields with default values
    domain = event.get("domain", "").strip().lower()
    title = event.get("title", "").strip().lower()
    url = event.get("url", "").strip().lower()
    
    # Create a unique string by concatenating the fields
    unique_string = f"{domain}|{title}|{url}"
    
    # Generate and return the MD5 hash
    return hashlib.md5(unique_string.encode()).hexdigest()

def remove_duplicates(dicts:list, key:str):
    exists=set()
    unique_dicts=[]
    for dict in dicts:
        value=dict.get(key)
        if value not in exists:
            exists.add(value)
            unique_dicts.append(dict)
    return unique_dicts

def convert_events_to_model(event_list:List[dict])->List[Event]:
    processed_event_list=[Event(**event) for event in event_list]
    return processed_event_list

def remove_unicode_chars(text:str):
    if text:
        return text.encode("ascii", "ignore").decode("ascii")
    return ""