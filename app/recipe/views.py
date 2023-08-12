"""Views for Recipe API"""


from recipe.serializers import RecipeSerializer
from rest_framework import generics, authentication, permissions, status
from rest_framework.response import Response
from rest_framework import viewsets
from core.models import Recipe

# Create your views here.


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')
