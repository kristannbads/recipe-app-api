"""Serializer class for recipe API"""

from rest_framework import serializers
from core import models


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe lists"""

    class Meta:
        model = models.Recipe
        fields = ['id', 'title',
                  'time_minutes', 'price', 'link']
        read_only_fields = ['id']


class RecipeDetailSerializer(serializers.ModelSerializer):
    """Serializer for recipe detail view"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
