 # import requests
import pandas as pd
from pandas import DataFrame
import requests
from time import sleep
from pathlib import Path
import brotli
import json
from setup import PROJECT_ROOT
from datetime import datetime



funeral_provider_directory_path = f"{PROJECT_ROOT}/resources/funeral_provider_directory.xlsx"

# Get current date, in YYYY_MM_DD format
#scrape_date = datetime.today().strftime('%Y_%m_%d')
scrape_date = "2025_09_08" # Hard-coded for now


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

# Create folder for results if doesn't exist
Path(f"{PROJECT_ROOT}/results/{scrape_date}").mkdir(parents=True, exist_ok=True)


## READ FUNERAL PROVIDER FILE AND MANIPULATE IT 

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



def ScrapeUrls(firm_name : str, url_list: list) -> None:

    # We only get the contents of the html response in this file. Processing of the html is done in another file.
    def ScrapeSingleUrl(url):        
        request = requests.get(
          url     = url,
          headers = headers
        )
        return request
    def ExportHTMLOutput(html_responses_content):
        # Create folder if doesn't exist
        Path(f"{PROJECT_ROOT}/results/{scrape_date}/{firm_name}").mkdir(parents=True, exist_ok=True)

        # Save
        with open(f"{PROJECT_ROOT}/results/{scrape_date}/{firm_name}/raw_get_responses.json", 'w+', encoding = 'utf-8') as f:
            json.dump(html_responses_content, f, ensure_ascii = False, indent = 4)
            

    # Do not process if list is empty (this only flags if the list is completely empty; not if list contains empty, and non-empty elements)
    if len( url_list ) == 0:
        return None

    html_responses = { url: ScrapeSingleUrl(url) for url in url_list if url != '' } # the if statement flag empty,''-entries


    # Extract text of html responses
    html_responses_content = {url: html_response.text for url, html_response in html_responses.items()}
 
    ExportHTMLOutput(html_responses_content)

    # [ExportHTMLOutput(i, html_response) for i, html_response in enumerate(html_responses.values())]
    sleep(1) 
    

    
# Scrape all urls for all firms
firm_html_responses = {
   firm_name : ScrapeUrls(firm_name, url_list) for firm_name, url_list in funeral_providers_urls_to_scrape.items()
}
