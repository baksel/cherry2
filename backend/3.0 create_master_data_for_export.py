import pandas as pd
import json
import os
import ast
from setup import PROJECT_ROOT, RESULTS_DATE_PATH


# Create folder if doesn't exist

funeral_provider_clean_prices_path = f"{RESULTS_DATE_PATH}/cleaned/funeral_provider_prices_clean.csv"

funeral_provider_directory_path = f"{PROJECT_ROOT}/resources/funeral_provider_directory.xlsx"


# Import the funeral directory for merging address, url, and location
df_funeral_provider_directory_raw = pd.read_excel(funeral_provider_directory_path)

# Import clean prices
funeral_provider_clean_prices_df_raw = pd.read_csv(
    funeral_provider_clean_prices_path,
    sep = ";"
)

# Select only the funeral package row
df_funeral_providers_clean_prices : pd.DataFrame= funeral_provider_clean_prices_df_raw.loc[ funeral_provider_clean_prices_df_raw.IsAllItems == True,]

# Select the columns we need from the directory
df_funeral_provider_directory = df_funeral_provider_directory_raw[['Name', 'Url', 'Palvelualue', "Puhelinnumero", 'Osoitteet']]


df_funeral_providers_final = pd.merge(
    df_funeral_provider_directory,
    df_funeral_providers_clean_prices,
    left_on   = 'Name',
    right_on  = 'funeral_provider',
    how       = 'right'
)

df_funeral_providers_final.rename(
    columns = {
        'Palvelualue' : "location",
        'Osoitteet'    : "address",
        "Url"          : "url"
    },
    inplace = True
)

# These columns are not sent Wordpress
df_funeral_providers_final.drop(
    axis    = 1,
    columns = ["Name", "IsAllItems"],
    inplace = True
)


df_funeral_providers_final.to_json(
    path_or_buf = f"{RESULTS_DATE_PATH}/cleaned/final_firebase_export_version.json", 
    orient      = "records", 
    indent      = 2,
    force_ascii = False,
)

