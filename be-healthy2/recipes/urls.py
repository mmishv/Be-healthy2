from django.urls import path
from .views import index, category

urlpatterns = [
    path('', index, name='main recipes'),
    path('<int:category_id>/<slug:slug>', category, name='category'),
    # path('create_recipe', RecipeCreate.as_view(), name='create_recipe'),
]
