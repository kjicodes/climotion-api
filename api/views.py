from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from api.serializers import SearchedCitySerializer, SavedWorkoutSerializer
from api.models import SearchedCity, SavedWorkout
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


class SearchedCityViewSet(ModelViewSet):
    queryset = SearchedCity.objects.all()
    serializer_class = SearchedCitySerializer


class SavedWorkoutViewSet(ModelViewSet):
    queryset = SavedWorkout.objects.all()
    serializer_class = SavedWorkoutSerializer















