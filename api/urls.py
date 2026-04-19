from django.urls import path
from api.views import WeatherView, WorkoutView

urlpatterns = [
    path("weather/", WeatherView.as_view(), name="weather"),
    path("workouts/", WorkoutView.as_view(), name="workout"),
]