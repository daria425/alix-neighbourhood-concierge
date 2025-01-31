import re
query_wherecanwego = {
    "request_config": {
        "website": "wherecanwego",
        "postcode": "N19QZ",
        "params": {"miles": 2},
    },
    "page_content_config": {
        "domain": "wherecanwego.com",
        "container": {
            "tag": "div",
            "filter": {
                "parameter": "class_",
                "value": "EventResults",
            },  # Adjust based on actual structure
        },
        "title": {
            "tag": "h2",
            "filter": {"parameter": "class_", "value": "eventtitle"},
        },
        "content": {
            "tag": "div",
            "filter": {"parameter": "class_", "value": "description"},
        },
        "url": {
            "tag": "a",
            "filter": {"parameter": "id", "value": re.compile("EventRepeater")},
        },
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
    },
}

query_islignton = {
    "request_config": {
        "website": "islingtonlife",
        "postcode": "N19QZ",
    },
    "page_content_config": {
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
    }, 
            "details":{
           "container": {
            "tag": "div",
            "filter": {"parameter": "class_", "value": "entry__body__container"}
        },
        "sections": {
            "tag": "p",
            "filter":{}
        } 
        }
    }
}

query_centre404={
        "request_config": {
        "website": "centre404",
        "postcode": "N19QZ",
    },
    "page_content_config":{
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
    }, 
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
}

