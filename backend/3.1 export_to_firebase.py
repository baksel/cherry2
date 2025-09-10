import json
import requests
import os
from setup import *

# SETUP
wp_site_url = "efunero.com"
custom_post_type = "funeral_provider"

access_token = 'oaJB$l2DmRTnn8i$V0PKe9bPcq#jXxUm9sNX0&KVI@J)MO*QOsNr*FtX4JYfOc)t'

#os.getenv("WP_ACCESS_TOKEN")

# WordPress.com REST API endpoint
endpoint = f"https://public-api.wordpress.com/rest/v1.1/sites/{wp_site_url}/posts/new"

funeral_provider_export_path = f"{PROJECT_ROOT}/results/wordpress/funeral_providers_export_{DATE}.json"

# Load JSON data
with open(funeral_provider_export_path, "r", encoding="utf-8") as f:
    funeral_data = json.load(f)

# Post each funeral provider
for entry in funeral_data:
    # Format for WordPress.com REST API
    post_data = {
        "title": entry["funeral_provider"],
        "status": "publish",
        #"content": f"Location: {entry['location']}, Price: €{entry['price']}, Date: {entry['date']}",
        "type": "funeral_provider",
        "metadata": [
            {"key": "name_of_provider", "value": entry["funeral_provider"]},
            {"key": "url_field", "value": entry["url"]},
            {"key": "location_field", "value": entry["location"]},
            {"key": "price_field", "value": entry["price"]},
            {"key": "date_field", "value": entry["date"]}
        ]
    }

    # Make request using the access token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(endpoint, headers=headers, json=post_data)

    print(1)