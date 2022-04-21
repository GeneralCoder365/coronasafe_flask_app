# from tempfile import TemporaryFile
import requests, json

# ! https://developers.google.com/maps/documentation/geocoding/requests-reverse-geocoding#reverse-requests

# import os
# from dotenv import load_dotenv
# from pathlib import Path
# # Getting Google API Key
# dotenv_path = Path('g_api_key.env')
# load_dotenv(dotenv_path=dotenv_path)
# G_API_KEY = str(os.getenv('G_API_KEY'))



def reverse_geocoder(google_api_key, lat, lng):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    
    # lat_lng_param = "latlng=" + str(lat) + "," + str(lng)
    
    # key_param = "&key=" + str(google_api_key)
    
    # endpoint = str(base_url + lat_lng_param + key_param)
    endpoint = f"{base_url}?latlng={lat},{lng}&key={google_api_key}&result_type=street_address"
    # print(endpoint)
    
    r = requests.get(endpoint)
    result = r.json()
    # print(result)
    
    if (result["status"] == "OK"):
        important_chunk = result["plus_code"]["compound_code"]
        if (important_chunk == None):
            return "ERROR: No address found"
        else:
            try:
                important_chunk = important_chunk.split(" ", 1)[1] # gets rid of code leaving core location
                return str(important_chunk)
            except ValueError:
                return str(important_chunk)
    
    else:
        try:
            return str("ERROR: " + str(result["error_message"]))
        except Exception:
            return str("ERROR: " + str(result["status"]))

# print(reverse_geocoder(G_API_KEY, 40.748817, -73.985428))
# 40.7484, -73.9857
# print(reverse_geocoder(G_API_KEY, 40.7484, -73.9857))