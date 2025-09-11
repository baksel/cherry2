# SETUP 
import os
from firebase_admin import credentials, firestore, initialize_app

PROJECT_ROOT = "C:/Projects/Efunero/backend"
DATE = "2025_09_08"

firebase_config_path = f"{PROJECT_ROOT}/resources/efunero-firebase-adminsdk-fbsvc-c3659522ea.json"

PROBLEMATIC_FUNERAL_PROVIDERS = ['Hautaustoimisto Toro']

# SETUP
RESULTS_DIR = f"{PROJECT_ROOT}/results"
RESULTS_DATE_PATH = f"{RESULTS_DIR}/{DATE}"
FUNERAL_DIRECTOR_NAMES = [x for x in os.listdir(RESULTS_DATE_PATH) if x != "cleaned"]


def initialize_firebase():
    cred = credentials.Certificate(firebase_config_path)
    initialize_app(cred)
    return firestore.client()

