import pandas as pd
import json
import os
import ast
from setup import *

# Is problematic: Helsingin Hautaustoimisto

NA_VALUES = ["NA", None, "", "Nan", "0"]
data_types = {
        "items" : object,
        "price" : str
    }
funeral_provider_results = f"{PROJECT_ROOT}/results"
funeral_provider_output_path = f"{funeral_provider_results}/{DATE}"


funeral_provider_names = os.listdir(funeral_provider_output_path)



def ProcessRawPrices(funeral_provider_name : str) -> pd.DataFrame | None:
    
    funeral_provider_results_path = f"{funeral_provider_output_path}/{funeral_provider_name}"
    #funeral_provider_results_path = "C:/Users/aksel/OneDrive/Projects/funeral_services/app_development/results/2025_04_06/eHautaus"    
    # Read the JSON file
    json_file_path = f"{funeral_provider_results_path}/prices_raw_2.json"
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Extract the individual prices data
    individual_prices = data.get('individual_prices')
    total_row    = data.get('contains_items')

    if ( len(individual_prices) == 0 ):
        return

    df_total_row = pd.DataFrame(
        {'items' : [total_row]}
    )
    

    # Convert to DataFrame
    df_individual_prices = pd.DataFrame(individual_prices)

    
    df_individual_prices = df_individual_prices.astype(
        data_types
    )

    IsPriceNotNA = [item not in NA_VALUES for item in df_individual_prices.price ]
    

    # Drop NA prices
    df_individual_prices = df_individual_prices.loc[ IsPriceNotNA, :]
  
    IsDFEmpty = len(df_individual_prices)

    assert IsDFEmpty != 0
    
    
    # Try converting to numeric
    try:
        # Convert to numeric
      df_individual_prices['price'] = df_individual_prices['price'].astype(float)
        
    except ValueError:
        return False # Not numeric

    
    isAllAboveZero = all( df_individual_prices['price'] >= 0 )
    
    assert isAllAboveZero

     # Check that list of individual items is equal to "contains items"  
     # Don't check if the list == valid list after dropping for NAs... this is often violated.
    individual_items           : list[list[str]] =  df_individual_prices.loc[:, 'items'] 
    

    df_individual_prices = df_individual_prices.assign(IsAllItems = False)


    # Calculate sum of individual prices to get price of the funeral package
    funeral_package_price : float = sum(df_individual_prices.loc[:, 'price'] )
    
    df_total_row = df_total_row.assign(
            IsAllItems = True,
            price      = funeral_package_price
        
    )

    df_funeral_provider_final = pd.concat([df_individual_prices, df_total_row])
   
    df_funeral_provider_final = df_funeral_provider_final.assign(
       date = DATE,
       funeral_provider = funeral_provider_name
    )

    return df_funeral_provider_final 
    


df_funeral_providers = [ProcessRawPrices(funeral_provider_name) for funeral_provider_name in funeral_provider_names]

# Merge individual funeral providers price dfs together
df_funeral_providers_final = pd.concat(df_funeral_providers)



df_funeral_providers_final.to_csv(
    path_or_buf = f"{PROJECT_ROOT}/funeral_provider_prices_clean.csv",
    sep         = ";",
    index       = False,
)

