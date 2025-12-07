import asyncio
from setup import FDS_TO_CLEAN
from scrape_funeral_website_contents import ScrapeAllCompanies
from clean_raw_get_response import CleanRawGetResponse
from extract_prices_from_cleaned_response import ParseMarkdownFilesForAllCompanies
from clean_raw_prices import ProcessRawPricesForAllCompanies
from create_master_file_for_export import CreateMasterFileForExport
from export_to_firebase import ExportMasterFileToFirebase

DATE = "2025_11_16"
# asyncio.run(
#     ScrapeAllCompanies( FDS_TO_CLEAN, FOLDER_DATE= DATE )
# )

# asyncio.run(
#     CleanRawGetResponse( FDS_TO_CLEAN, DATE)
# )


#ParseMarkdownFilesForAllCompanies( FDS_TO_CLEAN, DATE)


#ProcessRawPricesForAllCompanies( FDS_TO_CLEAN, DATE)

#CreateMasterFileForExport( DATE )

ExportMasterFileToFirebase( DATE )
