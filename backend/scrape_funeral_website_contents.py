 # import requests
import pandas as pd
from pandas import DataFrame
import requests
from pathlib import Path
import brotli
import json
from setup import PROJECT_ROOT
from datetime import datetime
import asyncio




headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,en;q=0.9",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}


## READ FUNERAL PROVIDER FILE AND MANIPULATE IT 
def GetFuneralProvidersAndURLSToScrape() -> dict:
    
    funeral_provider_directory_path = f"{PROJECT_ROOT}/resources/funeral_provider_directory.xlsx"

    funeral_providers_raw: pd.DataFrame = pd.read_excel(
        io = funeral_provider_directory_path,
        sheet_name = 0, 
        header     = 0,
        index_col  = 0
        )


    # Spaces replaced with underscores of column names
    spaces_underscored = [str.replace(x, " ", "_") for x in funeral_providers_raw.columns ]

    # Replace column names
    funeral_providers_raw.columns = spaces_underscored

    funeral_providers : DataFrame = funeral_providers_raw.copy()

    # Remove all spaces
    funeral_providers['Urls_to_scrape'] = funeral_providers['Urls_to_scrape'].str.replace(' ', "")

    # Convert ";"-separated urls to list
    funeral_providers['Urls_to_scrape'] = funeral_providers['Urls_to_scrape'].str.split(";")


    # Replace NAs with empty list
    #funeral_providers.kic[pd.isna(funeral_providers['Urls_to_scrape']),'Urls_to_scrape'] = []
    funeral_providers['Urls_to_scrape'] = funeral_providers['Urls_to_scrape'].apply(lambda x: x if isinstance(x, list) else [])



    funeral_providers_urls_to_scrape : dict = funeral_providers["Urls_to_scrape"].to_dict()

    return funeral_providers_urls_to_scrape



async def ScrapeCompanyUrls(firm_name : str, url_list: list, FOLDER_DATE : str) -> None:

    # We only get the contents of the html response in this file. Processing of the html is done in another file.
    async def ScrapeSingleUrl(url):        
        request = requests.get(
          url     = url,
          headers = headers
        )

        await asyncio.sleep(1)
        return request
    def ExportHTMLOutput(html_response_dict : dict):
        """ 
        Exports HTML Output as a json file

        arg:
          html_response_dict: is firm-specific, url-html key-value dict
        
        """
        # Create folder if doesn't exist
        Path(f"{PROJECT_ROOT}/results/{FOLDER_DATE}/{firm_name}").mkdir(parents=True, exist_ok=True)

        # Save
        with open(f"{PROJECT_ROOT}/results/{FOLDER_DATE}/{firm_name}/raw_get_responses.json", 'w+', encoding = 'utf-8') as f:
            json.dump(html_response_dict, f, ensure_ascii = False, indent = 4)
            

    # Do not process if list is empty (this only flags if the list is completely empty; not if list contains empty, and non-empty elements)
    if len( url_list ) == 0:
        return None
    

    tasks = [ScrapeSingleUrl(url) for url in url_list if url != '' ] # Don't process empty-urls

    valid_urls = [ url for url in url_list if url != "" ]

    
    html_responses = await asyncio.gather(
        *(tasks)
    )
    # All url and data into one dict for a company
    firm_html_response_dict : dict = {
        url : html_response.text for (url, html_response) in zip(valid_urls, html_responses)
    }

 
    ExportHTMLOutput(firm_html_response_dict)
    

async def ScrapeAllCompanies(companies_to_scrape : list[str], FOLDER_DATE = datetime.today().strftime('%Y_%m_%d') ) -> None:
  """
  
  Args:
  companies_to_scrape: list of companies to scrape
  FOLDER_DATE: the date-suffix to add to the new folder w/ scraped results
  """

  # Create folder for results if doesn't exist
  Path(f"{PROJECT_ROOT}/results/{FOLDER_DATE}").mkdir(parents=True, exist_ok=True)
  all_urls_and_companies = GetFuneralProvidersAndURLSToScrape()

  filtered_urls_and_companies = {key : value 
                                 for key, value in all_urls_and_companies.items()
                                 if key in companies_to_scrape}

  
  # Scrape all urls for all firms
  await asyncio.gather(
    *(ScrapeCompanyUrls(firm_name, url_list, FOLDER_DATE) for firm_name, url_list in filtered_urls_and_companies.items() )   
  )


