
from app.core.get_data import get_tavily_dset, get_scraped_dset
from app.db.database_service import EventSearchConfigService
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
    tavily_results=get_tavily_dset(query)
    final_list=list(chain.from_iterable(scraped_data_list))+tavily_results
    return final_list
