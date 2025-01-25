from read_html import WhereCanWeGoReader
from search import WhereCanWeGoSearch
searcher=WhereCanWeGoSearch()
file_path = "data/html/result_page_content.html"  
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()
    
reader=WhereCanWeGoReader()
event_metadata=reader.get_event_metadata(content=html_content)
event_detail_html_list=searcher.fetch_event_details(event_metadata)
for d in event_detail_html_list:
    event_detail=reader.get_event_detail(d)
    print(event_detail)
