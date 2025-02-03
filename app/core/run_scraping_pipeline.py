
from app.core.get_data import get_tavily_dset, get_scraped_dset
from itertools import chain
from dotenv import load_dotenv
load_dotenv()

# query={
#     "postcode":'N19QZ', 
#     "params": {"miles":2}
# }



def run_scraping_pipeline(query:dict):
    scraped_data_list=[]
    configs=[
  {
    "request_config": {
      "website": "islingtonlife",
      "website_type": "static",
      "include_event_details": False
    },
    "page_content_config": {
      "domain": "islingtonlife.london",
      "container": {
        "tag": "div",
        "filter": {
          "parameter": "class_",
          "value": "card__item card__item--wide"
        }
      },
      "title": {
        "tag": "h2",
        "filter": {
          "parameter": "class_",
          "value": "card__item__title u-color--red"
        }
      },
      "content": {
        "tag": "p",
        "filter": {
          "parameter": "class_",
          "value": "card__item__teaser u-color--black"
        }
      },
      "url": {
        "tag": "a",
        "filter": { "parameter": "class_", "value": "card__item__container" }
      },
      "details": {
        "container": {
          "tag": "div",
          "filter": { "parameter": "class_", "value": "entry__body__container" }
        },
        "sections": { "tag": "p", "filter": {} }
      }
    }
  },
  {
    "request_config": {
      "website": "centre404",
      "website_type": "static",
      "include_event_details": False
    },
    "page_content_config": {
      "domain": "centre404.org.uk",
      "container": {
        "tag": "div",
        "filter": { "parameter": "class_", "value": "news-post clearfix" }
      },
      "title": {
        "tag": "div",
        "filter": { "parameter": "class_", "value": "title" }
      },
      "content": {
        "tag": "div",
        "filter": { "parameter": "class_", "value": "short-description" }
      },
      "url": {
        "tag": "a",
        "filter": { "parameter": "class_", "value": "read-more" }
      },
      "details": {
        "container": {
          "tag": "div",
          "filter": { "parameter": "class_", "value": "copy-wrapper" }
        },
        "sections": { "tag": "p", "filter": {} }
      }
    }
  },
  {
    "request_config": {
      "website": "wherecanwego",
      "website_type": "static",
      "include_event_details": False
    },
    "page_content_config": {
      "domain": "wherecanwego.com",
      "container": {
        "selector": "div[class*='EventResults']"
      },
      "title": {
        "tag": "h2",
        "filter": { "parameter": "class_", "value": "eventtitle" }
      },
      "content": {
        "tag": "div",
        "filter": { "parameter": "class_", "value": "description" }
      },
      "url": {
        "tag": "a",
        "filter": { "parameter": "class_", "value": "ShowMore" }
      },
      "details": {
        "container": {
          "tag": "section",
          "filter": { "parameter": "id", "value": "middle" }
        },
        "sections": {
          "tag": "div",
          "filter": { "parameter": "class_", "value": "spacing" }
        }
      }
    }
  },
  {
    "request_config": {
      "website": "the-garden-classroom-76146096453",
      "website_type": "dynamic",
      "include_event_details": True
    },
    "page_content_config": {
      "domain": "eventbrite.co.uk",
      "locator": { "selector": "h3.Typography_root__487rx" },
      "container": {
        "selector": "div[data-testid='organizer-profile__future-events'] div.Container_root__4i85v.NestedActionContainer_root__1jtfr.event-card"
      },
      "title": {
        "tag": "h3",
        "filter": { "parameter": "class_", "value": "Typography_root__487rx" }
      },
      "content": {
        "tag": "section",
        "filter": { "parameter": "class_", "value": "event-card-details" }
      },
      "url": {
        "tag": "a",
        "filter": { "parameter": "class_", "value": "event-card-link" }
      },
      "details": {
        "container": {
          "tag": "section",
          "filter": { "parameter": "class_", "value": "event-card-details" }
        },
        "sections": { "tag": "p", "filter": {} }
      }
    }
  },
  {
    "request_config": {
      "website": "praxis-17432513338",
      "website_type": "dynamic",
      "include_event_details": True
    },
    "page_content_config": {
      "domain": "eventbrite.co.uk",
      "locator": { "selector": "h3.Typography_root__487rx" },
      "container": {
        "selector": "div[data-testid='organizer-profile__future-events'] div.Container_root__4i85v.NestedActionContainer_root__1jtfr.event-card"
      },
      "title": {
        "tag": "h3",
        "filter": { "parameter": "class_", "value": "Typography_root__487rx" }
      },
      "content": {
        "tag": "section",
        "filter": { "parameter": "class_", "value": "event-card-details" }
      },
      "url": {
        "tag": "a",
        "filter": { "parameter": "class_", "value": "event-card-link" }
      },
      "details": {
        "container": {
          "tag": "section",
          "filter": { "parameter": "class_", "value": "event-card-details" }
        },
        "sections": { "tag": "p", "filter": {} }
      }
    }
  }
]

    for config in configs:
        config['request_config']['postcode']=query['postcode']
        config['request_config']['params']=query['params']
        scraped_data=get_scraped_dset(config)
        scraped_data_list.append(scraped_data)
    tavily_results=get_tavily_dset(query)
    final_list=list(chain.from_iterable(scraped_data_list))+tavily_results
    return final_list
