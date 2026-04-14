import requests
from django.conf import settings
from django.shortcuts import render
from django.views import View

MIN_TEMP_CELSIUS = 10
BAD_WEATHER_CONDITIONS = {
    "drizzle": "It's not quite raining, but it's not not raining either — "
               "that sneaky mist that somehow soaks you without warning. "
               "Skip the guessing game and take your workout inside today.",
    "rain": "It's basically a free car wash out there — "
            "slippery, soggy, and not great for a run. "
            "Best to take your workout inside today.",
    "snow": "A winter wonderland is pretty to look at from a warm window. "
            "Lace up indoors and let the snowflakes do their thing without you. "
            "An indoor workout is the move today.",
    "thunderstorm": "Thunder means lightning is nearby, and lightning means "
                    "you should absolutely not be the tallest thing in an open field. "
                    "Head inside for your workout today."
}


def get_workout_suggestion(weather):
    description = weather["weather"][0]["main"]
    temp = weather["main"]["feels_like"]
    for condition, message in BAD_WEATHER_CONDITIONS.items():
        if condition in description:
            return message

    if temp < MIN_TEMP_CELSIUS:
        return ("It feels cold out there — not ideal for breaking a sweat outside. "
                "An indoor workout is the way to go today.")

    return "The weather looks good — perfect conditions for an outdoor workout!"


class HomeView(View):
    def get(self, request):
        city = request.GET.get('city')

        if not city:
            return render(request, 'home.html')

        geo_params = {
            'q': city,
            'appid': settings.OPENWEATHER_API_KEY,
        }
        geo_response = requests.get(settings.GEOCODING_BASE_URL, params=geo_params)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        latitude = geo_data[0]['lat']
        longitude = geo_data[0]['lon']

        weather_params = {
            'lat': latitude,
            'lon': longitude,
            'appid': settings.OPENWEATHER_API_KEY
        }
        weather_response = requests.get(settings.OPENWEATHER_BASE_URL, params=weather_params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        celsius_conversion = 273.15
        forecast = {
            'weather': weather_data["weather"][0]['main'],
            'description': get_workout_suggestion(weather_data),
            'temperature': int(weather_data["main"]["temp"] - celsius_conversion),
            'feels_like': int(weather_data["main"]["feels_like"] - celsius_conversion),
            'low': int(weather_data["main"]["temp_min"] - celsius_conversion),
            'high': int(weather_data["main"]["temp_max"] - celsius_conversion)
        }

        return render(request, 'home.html', {'forecast': forecast})
