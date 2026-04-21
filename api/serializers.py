import re
from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import SearchedCity, SavedWorkout


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "password"]
        extra_kwargs = {
            "first_name": { "required": True },
            "last_name": { "required": True },
            "password": {
                "write_only": True,
                "required": True
            }
        }

    def validate_password(self, value):
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$', value):
            raise serializers.ValidationError("Password must be at least 8 characters and contain an uppercase letter, lowercase letter, number, and special character (@$!%*?&).")
        return value

    def create(self, validated_data):
        new_user = User.objects.create_user(**validated_data)
        return new_user


class SearchedCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchedCity
        fields = ["id", "city_name"]


class SavedWorkoutSerializer(serializers.ModelSerializer):
    workout_reflection = serializers.SerializerMethodField()

    class Meta:
        model = SavedWorkout
        fields = ["id", "user", "exercise_type", "difficulty", "workout", "workout_reflection_before", "workout_reflection_after", "workout_reflection", "created_at"]
        extra_kwargs = {
            "user": {
                "read_only": True
            },
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
