from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import Recipe, RecipeCategory, Product, Ingredient
from .serializers import RecipeSerializer, ProductSerializer, RecipeCategorySerializer, IngredientSerializer
from rest_framework import viewsets, permissions, filters


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'date', 'categories__name', 'ingredient_amount__product__name']
    ordering_fields = ['title', 'date', 'categories__name']
    ordering = ['date']
    permission_classes_by_action = {
        'create': [permissions.IsAuthenticated],
        'retrieve': [permissions.AllowAny],
        'update': [permissions.IsAuthenticated],
        'partial_update': [permissions.IsAuthenticated],
        'destroy': [permissions.IsAuthenticated],
        'list': [permissions.AllowAny],
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['POST'])
    def moderate(self, request):
        recipe = self.get_object()
        recipe.moderated = True
        recipe.save()
        return Response({'message': 'Recipe moderated.'})


class RecipeCategoryViewSet(viewsets.ModelViewSet):
    queryset = RecipeCategory.objects.all()
    serializer_class = RecipeCategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
