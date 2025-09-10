import asyncio
from crawl4ai import (
    AsyncWebCrawler,
    CrawlerRunConfig
)
from crawl4ai.async_crawler_strategy import AsyncPlaywrightCrawlerStrategy
from crawl4ai.browser_manager import BrowserManager
import os
import json
# Import CAPITAL variables (e.g., PROJECT_ROOT) 
from setup import PROJECT_ROOT, DATE 


funeral_provider_results = f"{PROJECT_ROOT}/results"
funeral_provider_output_path = f"{funeral_provider_results}/{DATE}"


########################### MONKEY PATCH ######################################

async def patched_async_playwright__crawler_strategy_close(self) -> None:
    """
    Close the browser and clean up resources.

    This patch addresses an issue with Playwright instance cleanup where the static instance
    wasn't being properly reset, leading to issues with multiple crawls.

    Issue: https://github.com/unclecode/crawl4ai/issues/842

    Returns:
        None
    """
    await self.browser_manager.close()

    # Reset the static Playwright instance
    BrowserManager._playwright_instance = None


AsyncPlaywrightCrawlerStrategy.close = patched_async_playwright__crawler_strategy_close


########################################################################################

funeral_provider_names = os.listdir(funeral_provider_output_path)

run_config = CrawlerRunConfig(
        excluded_tags=["script", "style", "form", "header", "footer", "nav"],
        excluded_selector="header, footer, nav, .social-media, .share-links, .social-links",
        only_text=True,
        remove_forms=True,
        exclude_social_media_links=True,
        exclude_external_links=True,
        #remove_overlay_elements=True,
        #magic=True,
        #simulate_user=True,
        #override_navigator=True,
        #verbose=True,
    )

funeral_provider_html_paths = [f"{funeral_provider_output_path}/{funeral_provider_name}" for funeral_provider_name in funeral_provider_names]

async def CleanHTML(html_content, crawler):
    
  
  result = await crawler.arun(
    url    = f"raw:{html_content}",
    config = run_config)
  html_converted_to_markdown = result.markdown

  return html_converted_to_markdown

# Process Funeral providers output json file. The json file follows {url : Raw HTML} format. One file might have many entries

async def ProcessFuneralContents(funeral_provider_html_path, crawler):
    
    funeral_provider_full_path  = f"{funeral_provider_html_path}/_output.json"
    #funeral_provider_full_path = f"{funeral_provider_output_path}/Helsingin Hautaustoimisto/raw_html.txt"
    #toMatch = f"{funeral_provider_output_path}/Helsingin Hautaustoimisto/_output.json"
    
    with open(funeral_provider_full_path, encoding = 'utf-8') as f:
      # if funeral_provider_full_path == toMatch:
      #   print(1)
      content : dict= json.load(f)
      #content = 2
      #html_content = f.read()
      
    #x = await CleanHTML(html_content, crawler)
    htmls_cleaned = {url : await CleanHTML(html_content, crawler)  for url, html_content in content.items()}


    # Export cleaned, markdown contents
    with open(f"{funeral_provider_html_path}/output_cleaned_v2.json", "w+", encoding = 'utf-8') as f:
        json.dump(htmls_cleaned,f, ensure_ascii = False, indent = 4)


async def main(funeral_provider_html_paths):
  
  crawler = AsyncWebCrawler()
  await crawler.start()

  # Iterate over each company
  for funeral_provider_html_path in funeral_provider_html_paths:
     await ProcessFuneralContents(funeral_provider_html_path, crawler)
     
  
  
  await crawler.close()



if __name__ == "__main__":
    asyncio.run(main(funeral_provider_html_paths))
