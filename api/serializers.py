from rest_framework import serializers
from api.models import SearchedCity


class SearchedCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchedCity
        fields = ["id", "city_name"]