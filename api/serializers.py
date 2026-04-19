from rest_framework import serializers
from api.models import SearchedCity, SavedWorkout


class SearchedCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchedCity
        fields = ["id", "city_name"]


class SavedWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedWorkout
        fields = ["id", "exercise_type", "difficulty", "workout", "created_at"]