# SETUP 
import os

PROJECT_ROOT = "C:/Projects/Efunero/backend"
DATE = "2025_09_08"

USERNAME = "akselbektas@yahoo.co.uk"
APPLICATION_PASSWORD = "QBTO jQkr UaNS eo2C jK6K 7pt6"
PROBLEMATIC_FUNERAL_PROVIDERS = ['Hautaustoimisto Toro']

# SETUP
RESULTS_DIR = f"{PROJECT_ROOT}/results"
RESULTS_DATE_PATH = f"{RESULTS_DIR}/{DATE}"
FUNERAL_DIRECTOR_NAMES = [x for x in os.listdir(RESULTS_DATE_PATH) if x != "cleaned"]



