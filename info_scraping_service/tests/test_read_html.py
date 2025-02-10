import pytest
from bs4 import Tag
import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.read_html import HTMLReader

@pytest.fixture
def sample_wcwg_html():
    content = Path(__file__).resolve().parent / "test_data" / "wcwg_result_page_content.html"
    return content.read_text()

@pytest.fixture
def sample_islingtonlife_html():
    content = Path(__file__).resolve().parent / "test_data" / "islingtonlife_result_page_content.html"
    return content.read_text()

@pytest.fixture
def sample_trinityislington_html():
    content = Path(__file__).resolve().parent / "test_data" / "trinityislington_result_page_content.html"
    return content.read_text()

@pytest.fixture
def sample_centre404_html():
    content = Path(__file__).resolve().parent / "test_data" / "centre404_result_page_content.html"
    return content.read_text()

@pytest.fixture
def sample_eventbrite_garden_classroom_html():
    content = Path(__file__).resolve().parent / "test_data" / "the-garden-classroom-76146096453_result_page_content.html"
    return content.read_text()

@pytest.fixture
def sample_eventbrite_praxis_html():
    content = Path(__file__).resolve().parent / "test_data" / "praxis-17432513338_result_page_content.html"
    return content.read_text()


# Fixtures for configuration
@pytest.fixture
def config_wherecanwego():
    return {
        "tag": "div",
        "filter": {"parameter": "class_", "value": "EventResults"}
    }

@pytest.fixture
def config_islington_life():
    return {
        "tag": "div",
        "filter": {"parameter": "class_", "value": "card__item card__item--wide"}
    }

@pytest.fixture
def config_centre404():
    return {
        "tag": "div",
        "filter": {"parameter": "class_", "value": "news-post clearfix"}
    }

@pytest.fixture
def config_eventbrite():
    return {
        "selector":"div[data-testid='organizer-profile__future-events'] div.Container_root__4i85v.NestedActionContainer_root__1jtfr.event-card" # Adjust based on actual structure
    }

@pytest.mark.parametrize("sample_html, config", [
    ("sample_wcwg_html", "config_wherecanwego"),
    ("sample_islingtonlife_html", "config_islington_life"),
    ("sample_centre404_html", "config_centre404"), 
    ("sample_eventbrite_garden_classroom_html", "config_eventbrite")
])
def test_get_event_results(sample_html, config, request):
    """Generic test for all readers."""
    sample_html_data = request.getfixturevalue(sample_html)
    config_data = request.getfixturevalue(config)

    reader = HTMLReader(page_content_config=config_data)
    results = reader._get_event_result_containers(sample_html_data, config=config_data)

    assert isinstance(results, list)
    assert all(isinstance(result, Tag) for result in results)
    assert len(results) > 0

@pytest.fixture
def metadata_config_wherecanwego():
    return {
    "domain": "wherecanwego.com",
    "container": {
        "tag": "div",
        "filter": {"parameter": "class_", "value": "EventResults"}  # Adjust based on actual structure
    },
    "title": {
        "tag": "h2",
        "filter": {"parameter": "class_", "value": "eventtitle"}
    },
    "content": {
        "tag": "div",
        "filter": {"parameter": "class_", "value": "description"}
    },
    "url": {
        "tag": "a",
        "filter": {"parameter": "id", "value": re.compile("EventRepeater")}
    }
}

@pytest.fixture
def metadata_config_centre404():
    return {
    "domain": "centre404.org.uk",
    "container": {
        "tag": "div",
        "filter": {"parameter": "class_", "value": "news-post clearfix"}  # Adjust based on actual structure
    },
    "title": {
        "tag": "div",
        "filter": {"parameter": "class_", "value": "title"}
    },
    "content": {
        "tag": "div",
        "filter": {"parameter": "class_", "value": "short-description"}
    },
    "url": {
        "tag": "a",
        "filter": {"parameter": "class_", "value": "read-more"}
    }
}

@pytest.fixture
def metadata_config_eventbrite():
    return {
    "domain": "eventbrite.co.uk",
            "locator":{
"selector": "h3.Typography_root__487rx"
            },
    "container": {
        "selector":"div[data-testid='organizer-profile__future-events'] div.Container_root__4i85v.NestedActionContainer_root__1jtfr.event-card" # Adjust based on actual structure
    },
    "title": {
        "tag": "h3",
        "filter": {"parameter": "class_", "value": "Typography_root__487rx"}
    },
    "content": {
        "tag": "section",
        "filter": {"parameter": "class_", "value": "event-card-details"}
    },
    "url": {
        "tag": "a",
        "filter": {"parameter": "class_", "value": "event-card-link"}
    }, 
    "details": {
        "container": {
            "tag": "section",
            "filter": {"parameter": "class_", "value": "event-card-details"}
        },
        "sections": {
            "tag": "p",
            "filter": {}
        }
    }

    }
@pytest.fixture
def metadata_config_islington_life():
    return {
    "domain": "islingtonlife.london",
    "container": {
        "tag": "div",
        "filter": {"parameter": "class_", "value": "card__item card__item--wide"}  # Adjust based on actual structure
    },
    "title": {
        "tag": "h2",
        "filter": {"parameter": "class_", "value": "card__item__title u-color--red"}
    },
    "content": {
        "tag": "p",
        "filter": {"parameter": "class_", "value": "card__item__teaser u-color--black"}
    },
    "url": {
        "tag": "a",
        "filter": {"parameter": "class_", "value": "card__item__container"}
    }
}


@pytest.mark.parametrize("sample_html, metadata_config", [
    ("sample_wcwg_html", "metadata_config_wherecanwego"),
    ("sample_centre404_html", "metadata_config_centre404" ), 
    ("sample_islingtonlife_html", "metadata_config_islington_life"), 
    ("sample_eventbrite_garden_classroom_html", "metadata_config_eventbrite"),
    ("sample_eventbrite_praxis_html", "metadata_config_eventbrite")

])
def test_get_event_metadata(sample_html, metadata_config, request):
    """Test for event metadata extraction."""
    sample_html_data = request.getfixturevalue(sample_html)
    metadata_config_data = request.getfixturevalue(metadata_config)

    reader = HTMLReader(page_content_config= metadata_config_data) 
    event_metadata = reader.get_event_metadata(sample_html_data)

    assert isinstance(event_metadata, list)
    assert len(event_metadata) > 0

    for metadata in event_metadata:
        assert "title" in metadata
        assert "url" in metadata
        assert "content" in metadata
        assert "timestamp" in metadata
        assert "domain" in metadata
        assert "event_id" in metadata

@pytest.mark.parametrize("sample_html, metadata_config", [
    ("sample_eventbrite_garden_classroom_html", "metadata_config_eventbrite"), 
    ("sample_eventbrite_praxis_html", "metadata_config_eventbrite")

])
def test_get_event_metadata_with_details(sample_html, metadata_config, request):
    sample_html_data = request.getfixturevalue(sample_html)
    metadata_config_data = request.getfixturevalue(metadata_config)
    reader = HTMLReader(page_content_config=metadata_config_data) 
    event_metadata = reader.get_event_metadata(content=sample_html_data, include_event_details=True)
    assert isinstance(event_metadata, list)
    assert len(event_metadata) > 0

    for metadata in event_metadata:
        assert "title" in metadata
        assert "url" in metadata
        assert "content" in metadata
        assert "timestamp" in metadata
        assert "domain" in metadata
        assert "event_id" in metadata
        assert "event_details" in metadata

        if 'event_details' in metadata: 
            event_details=metadata['event_details']
            assert isinstance(event_details, dict)
            assert 'sections' in event_details
            assert isinstance(event_details['sections'], list)
    
@pytest.fixture
def event_detail_config_centre404():
    return {
 "details": {
        "container": {
            "tag": "div",
            "filter": {"parameter": "class_", "value": "copy-wrapper"}
        },
        "sections": {
            "tag": "p",
            "filter": {}
        }
    }
    }

@pytest.fixture
def event_detail_config_eventbrite():
    return {
         "details": {
        "container": {
            "tag": "section",
            "filter": {"parameter": "class_", "value": "event-card-details"}
        },
        "sections": {
            "tag": "p",
            "filter": {}
        }
    }
    }
@pytest.fixture
def event_detail_config_wcwg():
    return {
        "details":{
           "container": {
            "tag": "section",
            "filter": {"parameter": "id", "value": "middle"}
        },
        "sections": {
            "tag": "div",
            "filter":{"parameter":"class_", "value":"spacing"}
        } 
        }
    }

@pytest.fixture
def event_detail_config_islingtonlife():
    return {
        "details":{
           "container": {
            "tag": "div",
            "filter": {"parameter": "class", "value": "entry__body__container"}
        },
        "sections": {
            "tag": "p",
            "filter":{}
        } 
        }
    }

@pytest.fixture
def sample_wcwg_event_dict():
    content = Path(__file__).resolve().parent / "test_data" / "wcwg_sample_event.html"
    event_dict={
        "event_id":"test-123", 
        "content":content.read_text()
    }
    return event_dict

@pytest.fixture
def sample_centre404_event_dict():
    content = Path(__file__).resolve().parent / "test_data" / "centre404_sample_event.html"
    event_dict={
        "event_id":"test-123", 
        "content":content.read_text()
    }
    return event_dict

@pytest.fixture
def sample_islingtonlife_event_dict():
    content = Path(__file__).resolve().parent / "test_data" / "islingtonlife_sample_event.html"
    event_dict={
        "event_id":"test-123", 
        "content":content.read_text()
    }
    return event_dict

@pytest.fixture
def sample_eventbrite_event_dict():
    content=Path(__file__).resolve().parent / "test_data" / "the-garden-classroom-76146096453_result_page_content.html"
    event_dict={
        "event_id":"test-123", 
        "content":content.read_text()
    }
    return event_dict


@pytest.mark.parametrize("event_dict, detail_config", [
    ("sample_wcwg_event_dict", "event_detail_config_wcwg"),
    ("sample_centre404_event_dict", "event_detail_config_centre404"), 
    ("sample_islingtonlife_event_dict", "event_detail_config_islingtonlife"), 
    ("sample_eventbrite_event_dict", "event_detail_config_eventbrite"),
])
def test_get_event_detail(event_dict, detail_config, request):
    """Test for event detail extraction."""
    sample_event_dict = request.getfixturevalue(event_dict)
    detail_config_data = request.getfixturevalue(detail_config)

    reader = HTMLReader(page_content_config=detail_config_data)  # Instantiate the reader
    event_details = reader.get_event_detail(sample_event_dict)

    assert isinstance(event_details, dict)
    assert "event_id" in event_details
    assert event_details["event_id"]=="test-123"
    assert "sections" in event_details
    assert isinstance(event_details["sections"], list)
    assert len(event_details["sections"])>0

