# SETUP 
import os

PROJECT_ROOT = "C:/Projects/Efunero/backend"
DATE = "2025_09_08"

USERNAME = "akselbektas@yahoo.co.uk"
APPLICATION_PASSWORD = "QBTO jQkr UaNS eo2C jK6K 7pt6"
PROBLEMATIC_FUNERAL_PROVIDERS = ['Hautaustoimisto Toro']



## UTIL Functions
def GetFuneralProviderResultsPaths():
    funeral_provider_output_path = f"{PROJECT_ROOT}/python/results/{DATE}"
    funeral_provider_names = os.listdir(funeral_provider_output_path)
    
    funeral_provider_results_path  = [ f"{funeral_provider_output_path}/{funeral_provider_name}" for funeral_provider_name in funeral_provider_names]

    return funeral_provider_results_path
    

