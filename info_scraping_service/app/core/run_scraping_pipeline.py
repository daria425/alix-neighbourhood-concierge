
from app.core.get_data import get_scraped_dset
from app.db.database_service import EventSearchConfigService
from app.utils.utils import convert_events_to_model
from itertools import chain
import asyncio
from dotenv import load_dotenv
load_dotenv()

# query={
#     "postcode":'N19QZ', 
#     "params": {"miles":2}
# }

event_search_config_service=EventSearchConfigService()

async def run_scraping_pipeline(query:dict):
    scraped_data_list=[]
    configs=await event_search_config_service.get_config(postcode=query['postcode'])
    async_tasks=[]
    for config in configs:
        config['request_config']['postcode']=query['postcode']
        config['request_config']['params']=query['params']
        async_tasks.append(get_scraped_dset(config))
    scraped_data_list = await asyncio.gather(*async_tasks)
    event_list=list(chain.from_iterable(scraped_data_list))
    final_list=convert_events_to_model(event_list)
    return final_list
