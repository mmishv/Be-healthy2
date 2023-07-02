from django.urls import path

from recipes.views import RecipeDeleteView
from . import views

urlpatterns = [
     path('auth', views.RegisterView.as_view(), name='auth'),
     path('register', views.RegisterView.as_view(), name='register'),
     path('login', views.LoginView.as_view(), name='login'),
     path('logout', views.LogoutView.as_view(), name='logout'),

     path('main', views.get_about_me, name='about me'),
     path('update', views.ProfileAboutMeUpdateView.as_view(), name='update parameters'),
     path('edit', views.MainInfoProfileUpdateView.as_view(), name='edit main info'),

     path('my-recipes', views.my_recipes, name='my recipes'),
     path('delete-recipe/<int:id>', RecipeDeleteView.as_view(), name='delete recipe'),
]
