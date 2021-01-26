import requests
import json
import datetime
from pytz import timezone

class Forecast():
    def __init__(self, key):
        self.API_KEY = key # xxxに自分のAPI Keyを入力。

    def forecast_now_weather(self, city_name):
        api = "http://api.openweathermap.org/data/2.5/weather?units=metric&q={city}&APPID={key}"

        url = api.format(city = city_name, key = self.API_KEY)
        response = requests.get(url)
        data = response.json()
        jsonText = json.dumps(data, indent=4)
        forecastData = json.loads(response.text)

        return forecastData
    
    def forecast_week(self, city_name):
        api = "http://api.openweathermap.org/data/2.5/forecast?units=metric&q={city}&appid={key}"

        url = api.format(city = city_name, key = self.API_KEY)
        response = requests.get(url)
        data = response.json()
        jsonText = json.dumps(data, indent=4)
        forecastData = json.loads(response.text)
        return forecastData

    def print_week(self, forecastData):
        for item in forecastData['list']:
            forecastDatetime = timezone(
                'Asia/Tokyo').localize(datetime.datetime.fromtimestamp(item['dt']))
            weatherDescription = item['weather'][0]['description']
            temperature = item['main']['temp']
            rainfall = 0
            if 'rain' in item and '3h' in item['rain']:
                rainfall = item['rain']['3h']
            print('日時:{0} 天気:{1} 気温(℃):{2} 雨量(mm):{3}'.format(
                forecastDatetime, weatherDescription, temperature, rainfall))