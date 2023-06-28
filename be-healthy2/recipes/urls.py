from django.urls import path
from .views import index

urlpatterns = [
    path('', index, name='main recipes'),
    # path('create_recipe', RecipeCreate.as_view(), name='create_recipe'),
    # path('<slug:slug>/', category_slug, name='category_slug'),
]
