from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from .views import RecipeCategoryViewSet, ProductViewSet, RecipeViewSet, IngredientViewSet

router = routers.DefaultRouter()

router.register(r'recipes', RecipeViewSet, basename='recipe')

recipe_router = nested_routers.NestedDefaultRouter(router, r'recipes', lookup='recipe')
recipe_router.register(r'ingredients', IngredientViewSet, basename='recipe-ingredients')

router.register(r'recipe-categories', RecipeCategoryViewSet, basename='recipe-category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
] + router.urls + recipe_router.urls
