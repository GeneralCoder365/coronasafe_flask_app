# https://github.com/GeneralCoder365/coronasafe
import os
from datetime import datetime as dt
import requests, json
import argparse

import local_density_calculator as local_density
import surrounding_density_calculator as surrounding_density

import heat_maps
GITHUB_API_TOKEN = str(os.environ['GITHUB_API_TOKEN'])
# print(GITHUB_API_TOKEN)


# Getting Google API Key

# ! FOR LOCAL TESTING!
# from dotenv import load_dotenv
# from pathlib import Path
# dotenv_path = Path('g_api_key.env')
# load_dotenv(dotenv_path=dotenv_path)
# G_API_KEY = str(os.getenv('G_API_KEY'))


G_API_KEY = str(os.environ['G_API_KEY'])
# print(G_API_KEY)


def places_search(search_query: str, str_location, g_api_key = G_API_KEY) -> list:
    # ! %2C is a comma for url requests
    # ! STR_LOCATION = "LATITUDE%2CLONGITUDE"

    # ! TEXT SEARCH DOCUMENTATION: https://developers.google.com/maps/documentation/places/web-service/search-text#json_2
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    # get method of requests module
    # return response object
    request = str(base_url + 'query=' + search_query + '&location=' + str_location + '&key=' + g_api_key)
    # print(request)
    r = requests.get(request)

    # stores data in json file
    json_file = r.json()
    search_results = json_file["results"]
    # print(search_results)

    formatted_search_results = []

    if (len(search_results) == 0):
        return False
    else:
        i = 0
        while ((i < 10) and (i < len(search_results))):
            name: str = (search_results[i])["name"]
            # print(name)
            address: str = (search_results[i])["formatted_address"]
            # print(address)
            if (name == ""):
                formatted_address = address
            else:
                formatted_address = "(" + name + ") " + address
            formatted_search_results.append(formatted_address)

            i += 1

    return formatted_search_results

# tester code
# print(places_search(input("Query: "), "39.034072%2C-77.113836"))
# print(places_search(input("Query: "), "40.7484%2C73.9857"))


# formats address chunks into whole address
def address_formatter(raw_address):
    if (("(" in raw_address) and (") " in raw_address)):
        formatted_address_array = raw_address.split(") ")[1]
        formatted_address_array = formatted_address_array.split(", ")
        formatted_address_array.pop()
        # print(formatted_address_array)
        formatted_address = ""
        for i in range(len(formatted_address_array) - 1):
            formatted_address += (formatted_address_array[i] + ", ")
        formatted_address += formatted_address_array[-1]
        formatted_address += ", USA"
    else:
        return False

    # Ex: "1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA"
    # Make sure state is just 2 letters!
    return formatted_address

# gets latitude, longitude
def get_lat_long(google_api_key, raw_address):
    input_address = address_formatter(raw_address)
    # print(input_address)

    lat = None
    long = None
    place_id = None
    status = None
    api_key = google_api_key

    # generates json request
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={input_address}&key={api_key}"

    r = requests.get(endpoint)
    # print(r)

    if r.status_code not in range(200, 299):
        # print("bob")
        return [None, None]
    
    # stores json file and attemps to retrieve latitude and longitude
    try:
        json_file = r.json()
        # print(json_file)
        results = json_file["results"][0]
        lat = results["geometry"]["location"]["lat"]
        long = results["geometry"]["location"]["lng"]
        status = json_file["status"]

        # NON-ERRORS:
        # "OK" indicates that no errors occurred; the address was successfully parsed and at least one geocode was returned
        if (status == "OK"):
            return [lat, long]

        # "ZERO_RESULTS" indicates that the geocode was successful but returned no results. This may occur if the geocoder was passed a non-existent address
        elif (status == "ZERO_RESULTS"):
            return [status, status]
        

        # ERRORS:
        # "REQUEST_DENIED" indicates that your request was denied.
        elif (status == "REQUEST_DENIED"):
            return [status, status]
        
        # "INVALID_REQUEST" generally indicates that the query (address, components or latlng) is missing.
        elif (status == "INVALID_REQUEST"):
            return [status, status]
        
        # "UNKNOWN_ERROR" indicates that the request could not be processed due to a server error. The request may succeed if you try again.
        elif (status == "UNKNOWN_ERROR"):
            return [status, status]

    # except case if json retrieval gives an error
    except:
        # Pass: https://www.google.com/search?q=pass+python+function&rlz=1C1SQJL_enUS806US806&oq=pass+python&aqs=chrome.2.69i57j0l6j69i65.2918j0j1&sourceid=chrome&ie=UTF-8 
        pass
        return [None, None]

# from timezonefinder import TimezoneFinder
def master_density_calculator(raw_address: str, g_api_key) -> int:
    location_latlong = get_lat_long(g_api_key, raw_address)
    # print(location_latlong)
    # print(type(location_latlong[0]))
    latitude = location_latlong[0]
    longitude = location_latlong[1]
    # print("latitude: ", latitude)
    # print("longitude: ", longitude)
    
    # ! for debugging
    # tf = TimezoneFinder()
    # timezone = tf.timezone_at(lng=longitude, lat=latitude)
    # print("timezone: ", timezone)
    
    try:
        local_density_rating = local_density.local_density_rating(raw_address, latitude, longitude)
    except KeyError:
        local_density_rating = None

    try:
        surrounding_density_rating = surrounding_density.surrounding_density_rating(raw_address, latitude, longitude, g_api_key)
    except Exception:
        surrounding_density_rating = None
    
    cumulative_density_rating = 0

    if (((type(local_density_rating) == int) or (type(local_density_rating) == float)) and 
    (((type(surrounding_density_rating) == int) or (type(surrounding_density_rating) == float)))):
        cumulative_density_rating = (local_density_rating * 0.8) + (surrounding_density_rating * 0.2)
    elif ((type(local_density_rating) == int) or (type(local_density_rating) == float)):
        cumulative_density_rating = local_density_rating
    elif ((type(surrounding_density_rating) == int) or (type(surrounding_density_rating) == float)):
        cumulative_density_rating = surrounding_density_rating
    else:
        return False
    
    cumulative_density_rating = round(cumulative_density_rating, 2)
    # print("local_density_rating", local_density_rating)
    # print("surrounding_density_rating", surrounding_density_rating)
    return cumulative_density_rating

# tester code
# print(master_density_calculator("(Westfield Montgomery) 7101 Democracy Blvd, Bethesda, MD 20852, United States"))


# master tester code (can change [0] to another index for the list but make sure you know that it is within the length of the results - 1)
# print(master_density_calculator(places_search(input("Query: "))[0]))

# ! CORONASAFE
def corona_safe(raw_address: str, g_api_key = G_API_KEY) -> int:    
    density_rating = master_density_calculator(raw_address, g_api_key)
    
    
    covid_risk_rating = density_rating
    return covid_risk_rating

# ! Tester Code
# print(corona_safe("(Westfield Montgomery) 7101 Democracy Blvd, Bethesda, MD 20852, United States"))
# print(corona_safe("(Empire State Building) 20 W 34th St, New York, NY 10001"))


def create_us_case_map():
    return heat_maps.create_us_case_map(GITHUB_API_TOKEN)

# tester code
# print(create_us_case_map())

def get_us_case_map():
    return heat_maps.get_us_case_map(GITHUB_API_TOKEN)

# tester code
# print(get_us_case_map())

def make_state_case_graph(state_input):
    # TO CHANGE!
    print()
    # heat_maps.make_state_case_graph(state_input)

# tester code
# make_state_case_graph("MD")