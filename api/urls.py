from django.urls import path
from api.models import SearchedCity
from api.views import WeatherView, WorkoutView, SearchedCityView, SavedWorkoutView

urlpatterns = [
    path("weather/", WeatherView.as_view(), name="weather"),
    path("workouts/", WorkoutView.as_view(), name="workout"),
    path("popular-cities/", SearchedCityView.as_view(), name="popular-cities"),
    path("saved-workouts/", SavedWorkoutView.as_view(), name="saved-workouts"),
]