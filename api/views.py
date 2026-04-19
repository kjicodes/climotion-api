import requests
import random
import json
from django.conf import settings
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import SearchedCity
from api.serializers import SearchedCitySerializer

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
MUSCLE_GROUPS = {
    "full": ["abdominals", "biceps", "chest", "lats", "lower_back", "middle_back", "traps", "triceps", "abductors", "adductors", "calves", "glutes", "hamstrings", "quadriceps"],
    "upper": ["abdominals", "biceps", "chest", "lats", "lower_back", "middle_back", "traps", "triceps"],
    "lower": ["abductors", "adductors", "calves", "glutes", "hamstrings", "quadriceps"]
}


def get_workout_suggestion(weather):
    """Evaluate weather conditions and temperature to return an indoor or outdoor workout recommendation."""

    description = weather["weather"][0]["main"]
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
        random_muscle_groups = random.sample(muscle_groups, min(4, len(muscle_groups)))
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
        exercises_api_params = {
            "type": exercise_type,
            "difficulty": difficulty
        }
        exercises_api_response = requests.get(settings.EXERCISES_BASE_URL, params=exercises_api_params,
                                              headers=headers)
        exercises_api_response.raise_for_status()
        exercises_api_data = exercises_api_response.json()

        exercises = random.sample(exercises_api_data, min(4, len(exercises_api_data)))

        for item in exercises:
            all_exercises.append(item)

    return all_exercises



class WeatherView(APIView):
    """Returns current weather condition and either an indoor or outdoor workout recommendation for a given city."""

    def get(self, request, *args, **kwargs):
        city = request.query_params.get('city')
        if not city:
            response = { "error": "City is required." }
            return Response(response, status=HTTP_400_BAD_REQUEST)

        city_is_valid = city.replace(" ", "").replace("-", "").replace("'", "").isalpha()
        city_is_numeric = city.isdigit()
        if city_is_numeric or not city_is_valid:
            response = { "error": "City must only contain letters, spaces, hyphens, or apostrophes." }
            return Response(response, status=HTTP_400_BAD_REQUEST)

        # save searched city to db if it does not exist
        if not SearchedCity.objects.filter(city_name=city).exists():
            SearchedCity.objects.create(city_name=city)


        forecast = get_weather(city)
        response = { "data": forecast }
        return Response(response, status=HTTP_200_OK)




class WorkoutView(APIView):
    """Returns a list of exercises based on the user's selected workout type, difficulty, and muscle groups."""

    def get(self, request, *args, **kwargs):
        exercise_type = request.query_params.get("exercise-type")
        difficulty = request.query_params.get("difficulty")
        muscle_group = request.query_params.get("muscle-group")


        if exercise_type == "cardio":
            if not difficulty:
                response = { "error": "Difficulty is required for cardio exercises." }
                return Response(response, status=HTTP_400_BAD_REQUEST)

            workout = get_exercises(exercise_type, difficulty, muscle_groups=None)
            response = { "data": workout }
            return Response(response, status=HTTP_200_OK)
        else:
            if not exercise_type or not difficulty or not muscle_group:
                response = {"error": "Exercise type, difficulty, and muscle group are required."}
                return Response(response, status=HTTP_400_BAD_REQUEST)
            workout = get_exercises(exercise_type, difficulty, MUSCLE_GROUPS[muscle_group])
            response = { "data": workout }
            return Response(response, status=HTTP_200_OK)


class SearchedCityView(APIView):
    """Returns a list of previously searched cities to populate city input suggestions."""

    def get(self, request, *args, **kwargs):
        # fetch saved cities to show as drop-down suggestions list to the user
        saved_cities = SearchedCitySerializer(SearchedCity.objects.all(), many=True)

        response = { "data": saved_cities.data }
        return Response(response, status=HTTP_200_OK)






