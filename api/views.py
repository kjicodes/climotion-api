from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import SearchedCity, SavedWorkout
from api.serializers import SearchedCitySerializer, SavedWorkoutSerializer
from api.utils import get_weather, get_exercises, MUSCLE_GROUPS


class WeatherView(APIView):
    """Returns current weather condition and either an indoor or outdoor workout recommendation for a given city."""

    def get(self, request):
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

    def get(self, request):
        exercise_type = request.query_params.get("exercise-type")
        difficulty = request.query_params.get("difficulty")
        muscle_group = request.query_params.get("muscle-group")

        if exercise_type == "cardio":
            if not difficulty:
                response = { "error": "Difficulty is required for cardio exercises." }
                return Response(response, status=HTTP_400_BAD_REQUEST)

            workout = get_exercises(exercise_type, difficulty, muscle_groups=None)
        elif exercise_type == "stretching":
            workout = get_exercises(exercise_type, difficulty=None, muscle_groups=None)
        else:
            if not difficulty or not muscle_group:
                response = {"error": "Difficulty and muscle group are required."}
                return Response(response, status=HTTP_400_BAD_REQUEST)
            workout = get_exercises(exercise_type, difficulty, MUSCLE_GROUPS[muscle_group])

        response = { "data": workout }
        return Response(response, status=HTTP_200_OK)


class SearchedCityView(APIView):
    """Returns a list of previously searched cities to populate city input suggestions."""

    def get(self, request):
        saved_cities = SearchedCity.objects.all()

        if not saved_cities.exists():
            response = { "error": "No saved cities found." }
            return Response(response, status=HTTP_400_BAD_REQUEST)

        serializer = SearchedCitySerializer(saved_cities, many=True)
        response = { "data": serializer.data }
        return Response(response, status=HTTP_200_OK)


class SavedWorkoutView(APIView):
    """Returns a list of previously saved workouts and saves new ones."""

    def get(self, request):
        saved_workouts = SavedWorkout.objects.all()

        if not saved_workouts.exists():
            response = { "error": "No saved workouts found." }
            return Response(response, status=HTTP_400_BAD_REQUEST)

        serializer = SavedWorkoutSerializer(saved_workouts, many=True)
        response = { "data": serializer.data }
        return Response(response, status=HTTP_200_OK)

    def post(self, request):
        serializer = SavedWorkoutSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class SavedWorkoutDetailView(APIView):
    """Returns a single saved workout by id."""

    def get(self, request, saved_workout_id):
        try:
            saved_workout = SavedWorkout.objects.get(id=saved_workout_id)
        except SavedWorkout.DoesNotExist:
            response = { "error": "Workout does not exist." }
            return Response(response, status=HTTP_400_BAD_REQUEST)
        else:
            serializer = SavedWorkoutSerializer(saved_workout)

            response = { "data": serializer.data }
            return Response(response, status=HTTP_200_OK)













