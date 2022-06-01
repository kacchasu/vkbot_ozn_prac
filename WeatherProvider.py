import urllib.request
import json
from datetime import datetime, timedelta, date

# morning (5:00-10:00) day (10:00-18:00) evening (18:00-23:00) night (23:00-5:00)

WEATHER_API_KEY = 'cdc771db22a8186cf104788e3b17d693'

START_MORNING_HOUR = 3
START_DAY_HOUR = 11
START_EVENING_HOUR = 15
START_NIGHT_HOUR = 21

'''
    Ясное небо, температура: 16-18 C
    Давление: 742 мм рт. ст., влажность: 35%
    Ветер: лёгкий, 2 м/c, западный
'''


class WeatherObject:
    min_temp = None
    max_temp = None
    icon = None
    description = None
    pressure = None
    humidity = None
    wind_type = None
    wind_speed = None
    direction = None

    @staticmethod
    def logging(key, comm):
        f1 = open("log.txt", "a")
        t1 = datetime.now()
        f1.write(key + " --- ")
        f1.write(t1.strftime("%d/%m/%Y %H:%M") + " --- ")
        f1.write("corona class: " + comm + '\n')

    def __init__(self):
        self.logging("CRE", "weather object: created")

    def set_temp_range(self, min_temp, max_temp):
        self.min_temp = round(min_temp)
        self.max_temp = round(max_temp)

    def set_icon(self, icon):
        self.icon = icon

    def set_description(self, description):
        if description == "Thunderstorm":
            self.description = "Ураган"
        elif description == "Drizzle":
            self.description = "Морось"
        elif description == "Rain":
            self.description = "Дождь"
        elif description == "Snow":
            self.description = "Снег"
        elif description == "Mist":
            self.description = "Лёгкий туман"
        elif description == "Smoke":
            self.description = "Дымка"
        elif description == "Haze":
            self.description = "Мгла"
        elif description == "Dust":
            self.description = "Песчаные вихри"
        elif description == "Fog":
            self.description = "Туман"
        elif description == "Sand":
            self.description = "Песчаная буря"
        elif description == "Dust":
            self.description = "Пыльная буря"
        elif description == "Ash":
            self.description = "Вулканический пепел"
        elif description == "Squall":
            self.description = "Шквалистый ветер"
        elif description == "Tornado":
            self.description = "Торнадо"
        elif description == "Clear":
            self.description = "Ясно"
        elif description == "Clouds":
            self.description = "Облачно"

    def set_pressure(self, pressure):
        self.pressure = pressure

    def set_humidity(self, humidity):
        self.humidity = humidity

    def set_wind_power(self, wind_speed):
        if 0.0 <= wind_speed <= 0.2:
            self.wind_type = "Штиль"
            self.wind_speed = round(wind_speed, 1)
        elif 0.3 <= wind_speed <= 1.5:
            self.wind_type = "Тихий"
            self.wind_speed = round(wind_speed, 1)
        elif 1.6 <= wind_speed <= 3.3:
            self.wind_type = "Лёгкий"
            self.wind_speed = round(wind_speed, 1)
        elif 3.4 <= wind_speed <= 5.4:
            self.wind_type = "Слабый"
            self.wind_speed = round(wind_speed, 1)
        elif 5.5 <= wind_speed <= 7.9:
            self.wind_type = "Умеренный"
            self.wind_speed = round(wind_speed, 1)
        elif 8.0 <= wind_speed <= 10.7:
            self.wind_type = "Свежий"
            self.wind_speed = round(wind_speed, 1)
        elif 10.8 <= wind_speed <= 13.8:
            self.wind_type = "Сильный"
            self.wind_speed = round(wind_speed, 1)
        elif 13.9 <= wind_speed <= 17.1:
            self.wind_type = "Крепкий"
            self.wind_speed = round(wind_speed, 1)
        elif 17.2 <= wind_speed <= 20.7:
            self.wind_type = "Очень крепкий"
            self.wind_speed = round(wind_speed, 1)
        elif 20.8 <= wind_speed <= 24.4:
            self.wind_type = "Шторм"
            self.wind_speed = round(wind_speed, 1)
        elif 24.5 <= wind_speed <= 28.4:
            self.wind_type = "Сильный шторм"
            self.wind_speed = round(wind_speed, 1)
        elif 28.5 <= wind_speed <= 32.6:
            self.wind_type = "Жестокий шторм"
            self.wind_speed = round(wind_speed, 1)
        elif 33.0 <= wind_speed:
            self.wind_type = "Ураган"
            self.wind_speed = round(wind_speed, 1)

    def set_wind_direction(self, direction_angle):
        angle = direction_angle // 45 * 45

        if angle == 0:
            self.direction = "северный"
        elif angle == 45:
            self.direction = "северо-восточный"
        elif angle == 90:
            self.direction = "восточный"
        elif angle == 135:
            self.direction = "юго-восточный"
        elif angle == 180:
            self.direction = "южный"
        elif angle == 225:
            self.direction = "юго-западный"
        elif angle == 270:
            self.direction = "западный"
        elif angle == 315:
            self.direction = "северо-западный"


class WeatherProvider:

    @staticmethod
    def logging(key, comm):
        f1 = open("log.txt", "a")
        t1 = datetime.now()
        f1.write(key + " --- ")
        f1.write(t1.strftime("%d/%m/%Y %H:%M") + " --- ")
        f1.write("corona class: " + comm + '\n')

    def get_current_weather(self):
        response = urllib.request.urlopen(
            f"http://api.openweathermap.org/data/2.5/weather?q=moscow&appid={WEATHER_API_KEY}&units=metric").read()
        json_object = json.loads(response)

        json_weather = json_object.get("weather")[0]  # choose the first option of description
        json_main = json_object.get("main")
        json_wind = json_object.get("wind")

        result = WeatherObject()
        result.set_icon(json_weather.get("icon"))
        result.set_description(json_weather.get("main"))
        result.set_wind_direction(json_wind.get("deg"))
        result.set_wind_power(json_wind.get("speed"))
        result.set_humidity(json_main.get("humidity"))
        result.set_pressure(json_main.get("pressure"))
        result.set_temp_range(json_main.get("temp_min"), json_main.get("temp_max"))

        self.logging("GET", "weather provider: got current weather")

        return result

    def get_weather_object(self, json_response):
        json_object = json_response

        json_weather = json_object.get("weather")[0]  # choose the first option of description
        json_main = json_object.get("main")
        json_wind = json_object.get("wind")

        result = WeatherObject()
        result.set_icon(json_weather.get("icon"))
        result.set_description(json_weather.get("main"))
        result.set_wind_direction(json_wind.get("deg"))
        result.set_wind_power(json_wind.get("speed"))
        result.set_humidity(json_main.get("humidity"))
        result.set_pressure(json_main.get("pressure"))
        result.set_temp_range(json_main.get("temp_min"), json_main.get("temp_max"))

        self.logging("GET", "weather provider: got weather object from json response")

        return result

    # morning (5:00-10:00) day (10:00-18:00) evening (18:00-23:00) night (23:00-5:00)

    def get_today_weather(self):
        response = urllib.request.urlopen(
            f"http://api.openweathermap.org/data/2.5/forecast?q=moscow&appid={WEATHER_API_KEY}&units=metric").read()
        json_list = json.loads(response).get("list")
        result = dict()
        today_day = datetime.today().day

        for period in json_list:
            period_datetime = datetime.fromtimestamp(period.get("dt"))

            if period_datetime.day != today_day:
                break

            if START_MORNING_HOUR <= period_datetime.hour < START_DAY_HOUR:
                result["morning"] = period
            elif START_DAY_HOUR <= period_datetime.hour < START_EVENING_HOUR:
                result["day"] = period
            elif START_EVENING_HOUR <= period_datetime.hour < START_NIGHT_HOUR:
                result["evening"] = period
            elif START_NIGHT_HOUR <= period_datetime.hour:
                result["night"] = period

        for key in result.keys():
            result[key] = self.get_weather_object(result[key])

        self.logging("GET", "weather provider: got today weather")

        return result

    def get_tomorrow_weather(self):
        response = urllib.request.urlopen(
            f"http://api.openweathermap.org/data/2.5/forecast?q=moscow&appid={WEATHER_API_KEY}&units=metric").read()
        json_list = json.loads(response).get("list")
        result = dict()
        tomorrow_start = (datetime.today() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow_end = tomorrow_start + timedelta(days=1)

        for period in json_list:
            period_datetime = datetime.fromtimestamp(period.get("dt"))

            if period_datetime < tomorrow_start:
                continue # not found yet

            if period_datetime >= tomorrow_end:
                break # if we are trying to look at the day that's after tomorrow

            if START_MORNING_HOUR <= period_datetime.hour < START_DAY_HOUR:
                result["morning"] = period
            elif START_DAY_HOUR <= period_datetime.hour < START_EVENING_HOUR:
                result["day"] = period
            elif START_EVENING_HOUR <= period_datetime.hour < START_NIGHT_HOUR:
                result["evening"] = period
            elif START_NIGHT_HOUR <= period_datetime.hour:
                result["night"] = period

        for key in result.keys():
            result[key] = self.get_weather_object(result[key])

        self.logging("GET", "weather provider: got tomorrow weather")

        return result

    def get_all_period_weather(self):
        response = urllib.request.urlopen(
            f"http://api.openweathermap.org/data/2.5/forecast?q=moscow&appid={WEATHER_API_KEY}&units=metric").read()
        json_list = json.loads(response).get("list")
        result = dict() # it's a DATES dict

        for period in json_list:
            period_datetime = datetime.fromtimestamp(period.get("dt"))

            if period_datetime.date() not in result:
                result[period_datetime.date()] = dict() # it's a PERIODS dict

            if START_MORNING_HOUR <= period_datetime.hour < START_DAY_HOUR:
                result[period_datetime.date()]["morning"] = period
            elif START_DAY_HOUR <= period_datetime.hour < START_EVENING_HOUR:
                result[period_datetime.date()]["day"] = period
            elif START_EVENING_HOUR <= period_datetime.hour < START_NIGHT_HOUR:
                result[period_datetime.date()]["evening"] = period
            elif START_NIGHT_HOUR <= period_datetime.hour:
                result[period_datetime.date()]["night"] = period

        for date_key in result.keys():
            for key in result[date_key].keys():
                result[date_key][key] = self.get_weather_object(result[date_key][key])

        self.logging("GET", "weather provider: got all period weather")

        return result


