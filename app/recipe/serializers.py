"""Serializer class for recipe API"""

from rest_framework import serializers
from core import models


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe serializer"""

    class Meta:
        model = models.Recipe()
        fields = ['user', 'title', 'description',
                  'time_minutes', 'price', 'link']
        read_only_fields = ['id']
