from rest_framework import serializers
from api.models import SearchedCity, SavedWorkout


class SearchedCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchedCity
        fields = ["id", "city_name"]


class SavedWorkoutSerializer(serializers.ModelSerializer):
    workout_reflection = serializers.SerializerMethodField()

    class Meta:
        model = SavedWorkout
        fields = ["id", "exercise_type", "difficulty", "workout", "workout_reflection_before", "workout_reflection_after", "workout_reflection", "created_at"]
        extra_kwargs = {
            "workout_reflection_before": {
                "write_only": True
            },
            "workout_reflection_after": {
                "write_only": True
            }
        }


    def get_workout_reflection(self, obj):
        return {
            "before_workout": obj.workout_reflection_before,
            "after_workout": obj.workout_reflection_after
            }
