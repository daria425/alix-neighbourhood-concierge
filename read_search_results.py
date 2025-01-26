
import requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
class SearchResultReader:
    def __init__(self, search_results):
        self.search_results=search_results

    def _get_clean_text(self, content):
        soup=BeautifulSoup(content, "html.parser")
        text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        extracted_text = ' '.join(elem.get_text() for elem in text_elements)
        clean_text=re.sub(r'\s+', ' ', extracted_text).strip()
        return clean_text

    def _scrape_url(self, url:str):
        try:
            response=requests.get(url)
            response.raise_for_status()
            content=response.content
            return content
        except requests.exceptions.HTTPError as http_err:
            return {"error": f"HTTP error occurred: {http_err}", "status_code": response.status_code}
        except requests.exceptions.RequestException as req_err:
            return {"error": f"Request error occurred: {req_err}"}
        except Exception as err:
            return {"error": f"An unexpected error occurred: {err}"}
    def scrape_results(self):
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(self._scrape_url, search_result["url"]): search_result 
                for search_result in self.search_results
            }
            for future in futures:
                extracted_content = future.result()  # Scraped content for a URL
                cleaned_content=self._get_clean_text(content=extracted_content)
                search_result = futures[future]  # Corresponding search result dict
                search_result["content"] = cleaned_content if cleaned_content != '' else search_result['content']
            return self.search_results
    
    def format_results_for_agent(self):
        results_with_content=self.scrape_results()
        texts=[]
        for res in results_with_content:
            info=f"""
            -----------
            BEGIN ENTRY
            -----------
            domain:{urlparse(res['url'])}
            content:{res['content']}
            ----------
            END ENTRY
            ----------
            """
            texts.append(info)
        return texts


