import json
import requests
import os
import firebase_admin
from setup import initialize_firebase, RESULTS_DATE_PATH



funeral_provider_export_path = f"{RESULTS_DATE_PATH}/cleaned/final_firebase_export_version.json"


# Define function for uploading data to firebase
def upload_funeral_data(data : dict):
    db = initialize_firebase()
    

    try:
        # Batch write for better performance
        batch = db.batch()
        
        for item in data:
            # Create a reference with auto-generated ID
            doc_ref = db.collection("funeral_providers_1").document()
            batch.set(doc_ref, item)
        
        # Commit the batch
        batch.commit()
    finally:
        firebase_admin.delete_app(firebase_admin.get_app())

# Load JSON data
with open(funeral_provider_export_path, "r", encoding="utf-8") as f:
    funeral_data = json.load(f)

    upload_funeral_data(funeral_data)



