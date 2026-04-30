import requests
import random
import json
from django.conf import settings


UPPER_MUSCLES = ["abdominals", "biceps", "chest", "lats", "lower_back", "middle_back", "traps", "triceps"]
LOWER_MUSCLES = ["abductors", "adductors", "calves", "glutes", "hamstrings", "quadriceps"]
MUSCLE_GROUPS = {
    "upper": UPPER_MUSCLES,
    "lower": LOWER_MUSCLES,
    "full": UPPER_MUSCLES + LOWER_MUSCLES,
}

MIN_TEMP_CELSIUS = 5
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
    """Evaluate weather conditions and temperature to return an indoor or outdoor workout recommendation."""

    description = weather["weather"][0]["main"].lower()
    temp = weather["main"]["feels_like"]
    for condition, message in BAD_WEATHER_CONDITIONS.items():
        if condition in description:
            return message

    if temp < MIN_TEMP_CELSIUS:
        return ("It feels cold out there — not ideal for breaking a sweat outside. "
                "An indoor workout is the way to go today.")

    return "The weather looks good — perfect conditions for an outdoor workout!"


def get_weather(city):
    """Resolves a city name to coordinates, then fetches and formats current weather conditions via the OpenWeather API."""

    geo_api_params = {
        'q': city,
        'appid': settings.OPENWEATHER_API_KEY,
    }

    geo_api_response = requests.get(settings.GEOCODING_BASE_URL, params=geo_api_params)
    geo_api_response.raise_for_status()
    geo_api_data = geo_api_response.json()
    
    if not geo_api_data:
        raise ValueError(f'City {city} not found.')
    
    latitude = geo_api_data[0]['lat']
    longitude = geo_api_data[0]['lon']

    weather_api_params = {
        'lat': latitude,
        'lon': longitude,
        'appid': settings.OPENWEATHER_API_KEY
    }
    weather_api_response = requests.get(settings.OPENWEATHER_BASE_URL, params=weather_api_params)
    weather_api_response.raise_for_status()
    weather_data = weather_api_response.json()

    celsius_conversion = 273.15
    forecast = {
        'city': city.capitalize(),
        'weather': weather_data["weather"][0]['main'],
        'description': get_workout_suggestion(weather_data),
        'temperature': int(weather_data["main"]["temp"] - celsius_conversion),
        'feels_like': int(weather_data["main"]["feels_like"] - celsius_conversion),
        'low': int(weather_data["main"]["temp_min"] - celsius_conversion),
        'high': int(weather_data["main"]["temp_max"] - celsius_conversion)
    }

    return forecast

def get_exercises(exercise_type, difficulty, muscle_groups: list=None):
    """Fetches a randomized list of exercises from the API Ninjas Exercises API based on type, difficulty, and optional muscle groups."""

    headers = {
        "X-Api-Key": settings.EXERCISES_API_KEY
    }

    all_exercises = []
    if muscle_groups:
        random_muscle_groups = random.sample(muscle_groups, min(5, len(muscle_groups)))
        print(f"Randomly chosen muscle groups: {random_muscle_groups}")

        shortfall = 0
        for group in random_muscle_groups:
            exercises_api_params = {
                "type": exercise_type,
                "muscle": group,
                "difficulty": difficulty
            }
            exercises_api_response = requests.get(settings.EXERCISES_BASE_URL, params=exercises_api_params, headers=headers)
            exercises_api_response.raise_for_status()
            exercises_api_data = exercises_api_response.json()

            target = 1 + shortfall
            k = min(target, len(exercises_api_data))
            exercise = random.sample(exercises_api_data, k)
            print("Printer chosen exercise per muscle group (1 value)")
            print(json.dumps(exercise, indent=2))

            for item in exercise:
                if "_" in item["muscle"]:
                    item["muscle"] = item["muscle"].replace("_", " ")
                all_exercises.append(item)

            shortfall = target - k

    else:
        if exercise_type == "cardio":
            exercises_api_params = {
                "type": exercise_type,
                "difficulty": difficulty
            }
        else:
            exercises_api_params = { "type": exercise_type }

        exercises_api_response = requests.get(settings.EXERCISES_BASE_URL, params=exercises_api_params,
                                              headers=headers)
        exercises_api_response.raise_for_status()
        exercises_api_data = exercises_api_response.json()

        exercises = random.sample(exercises_api_data, min(5, len(exercises_api_data)))

        for item in exercises:
            all_exercises.append(item)

    return all_exercises