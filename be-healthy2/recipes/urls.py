from django.urls import path
from .views import index, category, RecipeCreateView

urlpatterns = [
    path('', index, name='main recipes'),
    path('<int:category_id>/<slug:slug>', category, name='category'),
    path('new_recipe', RecipeCreateView.as_view(), name='create_recipe'),
]
