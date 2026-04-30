from requests.exceptions import HTTPError
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_503_SERVICE_UNAVAILABLE
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers import SearchedCitySerializer, SavedWorkoutSerializer, UserSerializer
from api.models import SearchedCity, SavedWorkout
from api.utils import get_weather, get_exercises, MUSCLE_GROUPS


class UserViewSet(ModelViewSet):
    """Handles user registration and authentication."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User created successfully.",
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        if self.action == "create":
            return []
        return [IsAuthenticated()]

    def get_queryset(self):
        user = User.objects.filter(id=self.request.user.id)
        return user

class WeatherView(APIView):
    """Returns current weather condition and either an indoor or outdoor workout recommendation for a given city."""
    permission_classes = [AllowAny]

    def get(self, request):
        city = request.query_params.get('city')
        if not city:
            response = { "error": "City is required." }
            return Response(response, status=HTTP_400_BAD_REQUEST)

        try:
            forecast = get_weather(city)
        except ValueError:
            response = { "error": "City not found. Please try again."}
            return Response(response, status=HTTP_404_NOT_FOUND)
        except HTTPError:
            response = { "error": "Weather data unavailable. Please try again later."}
            return Response(response, status=HTTP_503_SERVICE_UNAVAILABLE)
        
        city_entry, _ = SearchedCity.objects.get_or_create(city_name=city)
        city_entry.search_count += 1
        city_entry.save()
        
        return Response(forecast, status=HTTP_200_OK)


class WorkoutView(APIView):
    """Authenticated users can retrieve a list of exercises based on the user's selected workout type, difficulty, and muscle groups."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        exercise_type = request.query_params.get("exercise-type")
        difficulty = request.query_params.get("difficulty")
        muscle_group = request.query_params.get("muscle-group")
        
        if not exercise_type:
            response = { "error": "Exercise type is required."}
            return Response(response, status=HTTP_400_BAD_REQUEST)

        try:
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
        except HTTPError:
            response = { "error": "Exercises unavailable. Please try again later."}
            return Response(response, status=HTTP_503_SERVICE_UNAVAILABLE)

        return Response(workout, status=HTTP_200_OK)


class SearchedCityViewSet(ReadOnlyModelViewSet):
    queryset = SearchedCity.objects.all()
    serializer_class = SearchedCitySerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return SearchedCity.objects.order_by('-search_count')


class SavedWorkoutViewSet(ModelViewSet):
    """CRUD operation for the authenticated user's saved workouts."""
    queryset = SavedWorkout.objects.all()
    serializer_class = SavedWorkoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        saved_workouts = SavedWorkout.objects.filter(user=user)
        return saved_workouts

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
