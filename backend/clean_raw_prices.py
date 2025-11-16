import pandas as pd
import json
from setup import PROJECT_ROOT
from pathlib import Path



df_eng_to_fi_dictionary = pd.read_excel(f"{PROJECT_ROOT}/resources/field_dictionary_eng_to_fin.xlsx")

eng_to_fi_dictionary : dict = dict( zip(df_eng_to_fi_dictionary["name_eng"], df_eng_to_fi_dictionary["name_fin"]) )


def CreateAdditionalInfoDict(collected_items: list ) -> dict :
    include_flags = { item_fi : item_eng in collected_items for item_eng, item_fi in eng_to_fi_dictionary.items() }
    add_info = {  
      key : {
        "isIncluded" : value,
        "additionalInfo" : "TBD"
      } 
      for key, value in include_flags.items()
    }
    return (add_info)


def ProcessRawPricesForACompany(name : str, DATE : str) -> pd.DataFrame | None:

    results_date_path = f"{PROJECT_ROOT}/results/{DATE}"

    # Add specification to LLM instructions on how to treat missing values
    NA_VALUES = ["NA", None, "", "Nan", "0"]

    # Create output directory for cleaned and merged prices, if it doesn't exist
    Path(f"{results_date_path}/cleaned").mkdir(parents=True, exist_ok=True)
    
    results_path = f"{results_date_path}/{name}"
    
    # Read the JSON file
    json_file_path = f"{results_path}/prices_raw.json"
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Extract the individual prices data
    individual_prices = data.get('individual_prices')
    total_row    = data.get('contains_items')

    
    total_row_add_info = CreateAdditionalInfoDict(total_row)

    if ( len(individual_prices) == 0 ):
        return

    df_total_row = pd.DataFrame(
        {'items' : [total_row_add_info]}
    )
    

    # Convert to DataFrame
    df_individual_prices = pd.DataFrame(individual_prices)

    
    df_individual_prices = df_individual_prices.astype(
         {
        "items" : object,
        "price" : str
        }
    )

    IsPriceNotNA = [item not in NA_VALUES for item in df_individual_prices.price ]
    

    # Drop NA prices
    df_individual_prices = df_individual_prices.loc[ IsPriceNotNA, :]
  
    IsDFEmpty = len(df_individual_prices)

    assert IsDFEmpty != 0
    
    
    # Try converting to numeric
    try:
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

    df_final = pd.concat([df_individual_prices, df_total_row])
   
    df_final = df_final.assign(
       date = DATE,
       funeral_provider = name
    )

    df_final.to_csv(
    path_or_buf = f"{results_date_path}/cleaned/{name}_prices_clean.csv",
    sep         = ";",
    index       = False,
    )
    
    return df_final

    
def ProcessRawPricesForAllCompanies(fd_names : list[str], DATE : str) -> None:

    prices_cleaned : pd.DataFrame = [ProcessRawPricesForACompany(fd_name, DATE) for fd_name in fd_names]

    prices_merged = pd.concat(prices_cleaned)

    prices_merged.to_csv(
    path_or_buf = f"{PROJECT_ROOT}/results/{DATE}/cleaned/clean_prices.csv",
    sep         = ";",
    index       = False,
    )








