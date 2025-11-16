import asyncio
from crawl4ai import (
    AsyncWebCrawler,
    CrawlerRunConfig,
    BrowserConfig
)
import os
import json
from setup import FUNERAL_DIRECTOR_NAMES, RESULTS_DIR, FDS_TO_CLEAN






run_config = CrawlerRunConfig(
        excluded_tags=["script", "style", "form", "header", "footer", "nav"],
        excluded_selector="header, footer, nav, .social-media, .share-links, .social-links",
        only_text=True,
        remove_forms=True,
        exclude_social_media_links=True,
        exclude_external_links=True,
        log_console = False,
        verbose=False #turnoff all messages to stdin >> can't have it for MCP
        #remove_overlay_elements=True,
        #magic=True,
        #simulate_user=True,
        #override_navigator=True,
        #verbose=True,
    )

browser_config = BrowserConfig(
   verbose=False #turnoff all messages to stdin >> can't have it for MCP
)



async def CleanHTML(html_content, crawler : AsyncWebCrawler):
    
  
  result = await crawler.arun(
    url    = f"raw:{html_content}",
    config = run_config
  )

  html_converted_to_markdown = result.markdown

  return html_converted_to_markdown

# Process Funeral providers output json file. The json file follows {url : Raw HTML} format. One file might have many entries
async def ProcessFuneralContents(html_folder : str, crawler : AsyncWebCrawler) -> None:
    
    input_full_path  = f"{html_folder}/raw_get_responses.json"
    
    
    with open(input_full_path, encoding = 'utf-8') as f:
      content : dict= json.load(f)
      
    htmls_cleaned = {url : await CleanHTML(html_content, crawler)  for url, html_content in content.items()}


    # Export cleaned markdown contents
    with open(f"{html_folder}/raw_response_cleaned.json", "w+", encoding = 'utf-8') as f:
        json.dump(htmls_cleaned,f, ensure_ascii = False, indent = 4)



  
async def CleanRawGetResponse(fd_names : str | list, date : str) -> None:
   
   """
     Produce a clean markdown file from the raw HTML response file. The file(s)  contains the price information for a specific funeral director.
     
     
     Args:
       fd_names: funeral director(s) that are to be cleaned
       date  (YYYY_MM_DD)  : the date when prices were collected. NB: there the data for the funeral director must be stored inside a specific folder w/ the
         date suffix/prefix.  

     Returns: None. The function saves cleaned markdown files under the date folder.
   """

   input_paths = [f"{RESULTS_DIR}/{date}/{funeral_provider_name}" 
                  for funeral_provider_name in FUNERAL_DIRECTOR_NAMES
                  if funeral_provider_name in fd_names]
   
     # Convert to list if a string, as the for-loop below only works if object is a list
   if type(input_paths) is str:
     
     input_paths : list = [input_paths]

   crawler = AsyncWebCrawler( config=browser_config)

   await crawler.start()

   # Iterate over each company
   await asyncio.gather(
    *( ProcessFuneralContents(fd_html_res_path, crawler) for fd_html_res_path in input_paths)
   )

   await crawler.close()