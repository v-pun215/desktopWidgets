import openmeteo_requests
import datetime
import geocoder
import requests_cache
import pandas as pd
from retry_requests import retry
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="DesktopWidgets/0,1")
# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
g = geocoder.ip('me')
location = geolocator.reverse(str(g.lat)+","+str(g.lng))
address = location.raw['address']
city = address.get('city', '')
params = {
	"latitude": {g.latlng[0]},
	"longitude": {g.latlng[1]},
	"current": ["temperature_2m", "precipitation", "rain", "weather_code", "wind_speed_10m", "wind_direction_10m", "apparent_temperature"],
	"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "rain_sum"],
	"timezone": "auto"
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Current values. The order of variables needs to be the same as requested.
current = response.Current()
current_temperature_2m = current.Variables(0).Value()
current_precipitation = current.Variables(1).Value()
current_rain = current.Variables(2).Value()
current_weather_code = current.Variables(3).Value()

timestamp = current.Time()
dt_object = datetime.datetime.fromtimestamp(timestamp)
print("dt_object =", dt_object)
weather_code_mapping = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Heavy Drizzle",
    56: "Light Freezing Drizzle",
    57: "Heavy Freezing Drizzle",
    61: "Light Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    66: "Light Freezing Rain",
    67: "Heavy Freezing Rain",
    71: "Light Snow",
    73: "Moderate Snow",
    75: "Heavy Snow",
    77: "Snow Grains",
    80: "Light Rain Showers",
    81: "Moderate Rain Showers",
    82: "Violent Rain Showers",
    85: "Light Snow Showers",
    86: "Heavy Snow Showers",
    95: "Thunderstorm",
    96: "Thunderstorm with Slight Hail",
    99: "Thunderstorm with Heavy Hail"
}
weather_code_icons = {
    0: "☀️",
    1: "🌤️",
    2: "⛅",
    3: "☁️",
    45: "🌫️",
    48: "🌫️",
    51: "🌧️",
    53: "🌧️",
    55: "🌧️",
    56: "🌧️",
    57: "🌧️",
    61: "🌧️",
    63: "🌧️",
    65: "🌧️",
    66: "🌧️",
    67: "🌧️",
    71: "❄️",
    73: "❄️",
    75: "❄️",
    77: "❄️",
    80: "🌧️",
    81: "🌧️",
    82: "🌧️",
    85: "❄️",
    86: "❄️",
    95: "⛈️",
    96: "⛈️",
    99: "⛈️"
}
current_weather_code = int(current_weather_code)
current_formatted_weather_code = weather_code_mapping.get(current_weather_code, "Unknown Weather Code")
current_weather_icon = weather_code_icons.get(current_weather_code, "❓")
current_percentage = round(current_precipitation * 100)
current_wind_speed_10m = current.Variables(4).Value()
current_wind_direction_10m = current.Variables(5).Value()
current_apparent_temperature = current.Variables(6).Value()
print(f"Current time {current.Time()}")
print(f"Current temperature_2m {current_temperature_2m}")
print(f"Current precipitation {current_percentage}%")
print(f"Current rain {current_rain}")
print(f"Current weather_code {current_weather_code}")
print(f"Formatted Weather Code: {current_formatted_weather_code}")
print(f"Current Weather Icon: {current_weather_icon}")
def getDayName(date):
    date = str(date)
    head, sep, tail = date.partition(" ")
    date_object = datetime.datetime.strptime(head, "%Y-%m-%d").date()
    return date_object.strftime("%A")
# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_weather_code = daily.Variables(0).ValuesAsNumpy()
daily_dayname = getDayName(datetime.datetime.fromtimestamp(daily.Time()))
daily_formatted_weather_code = [weather_code_mapping.get(int(code), "Unknown Weather Code") for code in daily_weather_code]
daily_weather_icons = [weather_code_icons.get(int(code), "❓") for code in daily_weather_code]
daily_max_temperature_2m = daily.Variables(1).ValuesAsNumpy()
daily_min_temperature_2m = daily.Variables(2).ValuesAsNumpy()

daily_rain_sum = daily.Variables(5).ValuesAsNumpy()

daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}
daily_data["weather_code"] = daily_weather_code
daily_data["formatted_weather_code"] = daily_formatted_weather_code
daily_data["weather_icons"] = daily_weather_icons
daily_data["rain_sum"] = daily_rain_sum
daily_data["dayname"] = daily_dayname
daily_data["max_temperature_2m"] = daily_max_temperature_2m
daily_data["min_temperature_2m"] = daily_min_temperature_2m
daily_data["day_start_local"] = daily.Time()


daily_dataframe = pd.DataFrame(data = daily_data)
print(daily_dataframe)
def degrees_to_cardinal(degrees):
    directions = [
        (0, 'N'), (22.5, 'NNE'), (45, 'NE'), (67.5, 'ENE'),
        (90, 'E'), (112.5, 'ESE'), (135, 'SE'), (157.5, 'SSE'),
        (180, 'S'), (202.5, 'SSW'), (225, 'SW'), (247.5, 'WSW'),
        (270, 'W'), (292.5, 'WNW'), (315, 'NW'), (337.5, 'NNW')
    ]
    
    # Normalize the degree to be within 0-360
    degrees = degrees % 360
    
    # Find the closest direction
    for i in range(len(directions)-1):
        if degrees >= directions[i][0] and degrees < directions[i+1][0]:
            return directions[i][1]
    
    # If it's 360 degrees, it should return 'N'
    return directions[-1][1]
def getCSS():
    new_text = f"""
        <html>
            <body>
                <div>
                    <p style="color: #8A9AAA; margin-bottom: 0px; white-space: pre; font-size: 13px;">{city}""" \
                   f"""{"&#9;" * 1}               {round(current_wind_speed_10m)} kph """ \
                   f"""{degrees_to_cardinal(current_wind_direction_10m)}&#9;""" \
                   f"""💧""" \
                   f"""{current_percentage}% """ \
                   f"""↑ {round(int(daily_max_temperature_2m))}° """ \
                   f"""↓ {round(daily_min_temperature_2m)}°</p>
                    <h1 style="margin-top: 0px; margin-bottom: 0px;">
                        {round(current_temperature_2m)}° 
                        {weather_code_icons.get(current_weather_code, "❓")}
                    </h1>
                    <p style="color: #8A9AAA; margin-top: 0px; margin-bottom: 0px; font-size: 15px;">
                        Feels like:
                        {round(current_apparent_temperature)}°
                    </p>
                    <hr></hr>""" + \
                   " ".join([f'''
                    <p style="margin-top: 0px; margin-bottom: 0px; font-size: 11px; white-space: pre;">''' 
                             f'''{datetime.datetime.fromtimestamp(info.get("day_start_local")).strftime("%A")}'''
                             f'''{"&#9;" * 2}{[weather_code_icons.get(int(code), "❓") for code in daily_weather_code]}'''
                             f'''{"&#9;" * 1}      💧'''
                             f'''{round(info.get("rain_sum"))}%{"&#9;" * 2}'''
                             f'''↑ {round(info.get("max_temperature_2m"))}°&#9;'''
                             f'''↓ {round(info.get("min_temperature_2m"))}°</p>'''
                             f'''<hr style="margin-top: 0px; margin-bottom: 0px;"></hr>'''
                             for info in
                             daily_data ]) + \
                   """
                </div>
            </body>
        </html>"""
    print(new_text)
getCSS()