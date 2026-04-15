import requests
import random
import json
from django.conf import settings
from django.shortcuts import render
from django.views import View

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


def get_weather(city):
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
    headers = {
        "X-Api-Key": settings.EXERCISES_API_KEY
    }

    all_exercises = []
    if muscle_groups:
        #pick 4 random groups from the list and get 1 random exercise per group
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
        #Return up to 3 cardio exercises
        exercises_api_params = {
            "type": exercise_type,
            "difficulty": difficulty
        }
        exercises_api_response = requests.get(settings.EXERCISES_BASE_URL, params=exercises_api_params,
                                              headers=headers)
        exercises_api_response.raise_for_status()
        exercises_api_data = exercises_api_response.json()

        exercises = random.sample(exercises_api_data, min(3, len(exercises_api_data)))

        for item in exercises:
            all_exercises.append(item)

    print(json.dumps(all_exercises, indent=2))
    return all_exercises



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

        forecast = get_weather(city)

        return render(request, 'home.html', {'forecast': forecast})


class ExerciseView(View):

    def get(self, request):
        workout = request.session.pop("workout", None)
        return render(request, "workout.html", {"workout": workout})


    def post(self, request):
        exercise_type = request.POST.get("exercise-type")
        difficulty = request.POST.get("difficulty")
        muscle_group = request.POST.get("muscle-group")

        workout = ""
        if exercise_type == "cardio":
            workout = get_exercises(exercise_type, difficulty, muscle_groups=None)
        else:
            if muscle_group == "upper":
                workout = get_exercises(exercise_type, difficulty, MUSCLE_GROUPS["upper"])
            elif muscle_group == "lower":
                workout = get_exercises(exercise_type, difficulty, MUSCLE_GROUPS["lower"])
            else:
                workout = get_exercises(exercise_type, difficulty, MUSCLE_GROUPS["full"])

        request.session["workout"] = workout
        return render(request, "workout.html", {"workout": workout})

