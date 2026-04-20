from django.urls import path
from api.views import WeatherView, WorkoutView, SearchedCityView, SavedWorkoutView,SavedWorkoutDetailView

urlpatterns = [
    path("weather/", WeatherView.as_view(), name="weather"),
    path("workouts/", WorkoutView.as_view(), name="workout"),
    path("popular-cities/", SearchedCityView.as_view(), name="popular-cities"),
    path("saved-workouts/", SavedWorkoutView.as_view(), name="saved-workouts"),
    path("saved-workouts/<int:saved_workout_id>/", SavedWorkoutDetailView.as_view(), name="saved-workout"),
]