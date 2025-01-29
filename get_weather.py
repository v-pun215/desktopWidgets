import datetime

import requests
import json
import geocoder
g = geocoder.ip('me')
class Weather(object):
    def __init__(self):
        self.url = open("url.txt").readline()
        self.headers = {"accept": "application/json"}

    def get_data(self):
        params = {
            "latitude": {g.latlng[0]},
            "longitude": {g.latlng[1]},
            "current": ["temperature_2m", "precipitation", "rain", "weather_code", "wind_speed_10m", "wind_direction_10m", "apparent_temperature"],
            "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "rain_sum"],
            "timezone": "auto"
        }
        response = requests.get(self.url, headers=params)
        return json.loads(response.text)

    @staticmethod
    def format_data(data):
        icons = {
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
        precip_type = {
            "rain": "💧",
            "snow": "❄️",
            "sleet": "🌨️",
            "storm": "⛈️"
        }
        new_text = f"""
        <html>
            <body>
                <div>
                    <p style="color: #8A9AAA; margin-bottom: 0px; white-space: pre; font-size: 13px;">{data.get("location_name")}""" \
                   f"""{"&#9;" * 1}               {round(data.get("current_conditions").get("wind_avg"))} mph """ \
                   f"""{data.get("current_conditions").get("wind_direction_cardinal")}&#9;""" \
                   f"""{precip_type.get(data.get("forecast").get("daily")[0].get("precip_type"))}""" \
                   f"""{data.get("forecast").get("daily")[0].get("precip_probability")}% """ \
                   f"""↑ {round(data.get("forecast").get("daily")[0].get("air_temp_high"))}° """ \
                   f"""↓ {round(data.get("forecast").get("daily")[0].get("air_temp_low"))}°</p>
                    <h1 style="margin-top: 0px; margin-bottom: 0px;">
                        {round(data.get("current_conditions").get("air_temperature"))}° 
                        {icons.get(data.get("current_conditions").get("icon"))}
                    </h1>
                    <p style="color: #8A9AAA; margin-top: 0px; margin-bottom: 0px; font-size: 15px;">
                        Feels like:
                        {round(data.get("current_conditions").get("feels_like"))}°
                    </p>
                    <hr></hr>""" + \
                   " ".join([f'''
                    <p style="margin-top: 0px; margin-bottom: 0px; font-size: 11px; white-space: pre;">''' 
                             f'''{datetime.datetime.fromtimestamp(info.get("day_start_local")).strftime("%A")}'''
                             f'''{"&#9;" * 2}{icons.get(info.get("icon"))}'''
                             f'''{"&#9;" * 1}      {precip_type.get(info.get("precip_type"))}'''
                             f'''{info.get("precip_probability")}%{"&#9;" * 2}'''
                             f'''↑ {round(info.get("air_temp_high"))}°&#9;'''
                             f'''↓ {round(info.get("air_temp_low"))}°</p>'''
                             f'''<hr style="margin-top: 0px; margin-bottom: 0px;"></hr>'''
                             for info in
                             data.get("forecast").get("daily")]) + \
                   """
                </div>
            </body>
        </html>"""
        return new_text