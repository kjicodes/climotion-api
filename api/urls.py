from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf.urls import include
from api.views import WeatherView, WorkoutView, SearchedCityViewSet, SavedWorkoutViewSet

router = DefaultRouter()
router.register("searched-cities", SearchedCityViewSet)
router.register("saved-workouts", SavedWorkoutViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("weather/", WeatherView.as_view(), name="weather"),
    path("workouts/", WorkoutView.as_view(), name="workout"),
]