# https://pypi.org/project/LivePopularTimes/
# https://github.com/GrocerCheck/LivePopularTimes

from datetime import datetime, time, timedelta
import livepopulartimes

from timezonefinder import TimezoneFinder
import pytz

def location_current_datetime(latitude, longitude):
    latitude = float(latitude)
    longitude = float(longitude)
    tf = TimezoneFinder()
    timezone = tf.timezone_at(lng=longitude, lat=latitude)
    # print("timezone: ", timezone)
    
    location_datetime = datetime.now(pytz.timezone(timezone))
    # print("location_datetime", location_datetime)
    location_day_of_week = location_datetime.weekday()
    # print("location_day_of_week", location_day_of_week)
    location_hour = location_datetime.hour
    # print("location_hour", location_hour)
    
    return [location_day_of_week, location_hour]

# ! Tester Code
# print(location_current_datetime("27.173891", "78.042068"))

def local_density_rating(formatted_address, latitude, longitude):
    try:
        place_data = livepopulartimes.get_populartimes_by_address(formatted_address)
    except KeyError:
        return False
    
    current_popularity = place_data["current_popularity"]
    # print("Current popularity_1: " + str(current_popularity))
    # current_popularity = None data type if no popularity data at current time
    
    if (current_popularity == None):
        location_datetime = location_current_datetime(latitude, longitude)
        current_day_of_week = location_datetime[0]
        current_hour = location_datetime[1]
        # print(current_day_of_week)
        # print(current_hour)

        # today's popular times (0 AM - 11 PM so index = hour)
        current_popularity = place_data["populartimes"][current_day_of_week - 1]["data"][current_hour]
        # print("Current popularity_2: " + str(current_popularity))

        # range: [0, 100) = (0 <= x < 101)
        if (current_popularity not in range(0, 101)):
            return None
    
    if ((type(current_popularity) == int) or (type(current_popularity) == float)):
        return current_popularity
    else:
        return "Error"

# tester code:
# print(local_density_rating("(Starbucks) 10251 Old Georgetown Rd, Bethesda, MD 20814"))
# print(local_density_rating("(McDonald's) 11564 Rockville Pike, Rockville, MD 20852"))