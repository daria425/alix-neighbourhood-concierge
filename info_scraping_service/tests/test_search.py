import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.search import HTMLSearch

@pytest.fixture
def wcwg_search():
    return HTMLSearch(website="wherecanwego")

@pytest.fixture
def islington_search():
    return HTMLSearch(website="islingtonlife")

@pytest.fixture
def trinity_search():
    return HTMLSearch(website="trinityislington")

@pytest.fixture
def centre404_search():
    return HTMLSearch(website="centre404")

def test_create_request_url_modified(wcwg_search):
    postcode = "N19QZ"
    params = {"miles":2}
    expected_url = f"https://www.wherecanwego.com/whats-on/{postcode}?id=7&miles=2"

    result_url = wcwg_search.create_request_url(postcode, params)
    assert result_url == expected_url, f"Expected {expected_url}, but got {result_url}"

def test_create_request_url_unmodified(islington_search, trinity_search, centre404_search):
    # Testing each non-WCWG website
    expected_url_islington = "https://islingtonlife.london/things-to-do/"
    expected_url_trinity = "https://trinityislington.org/whats-happening"
    expected_url_centre404 = "https://centre404.org.uk/blog/"
    assert islington_search.create_request_url() == expected_url_islington
    assert trinity_search.create_request_url() == expected_url_trinity
    assert centre404_search.create_request_url() == expected_url_centre404
