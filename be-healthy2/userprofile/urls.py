from django.urls import path

from main.views import ArticleCreateView
from recipes.views import RecipeDeleteView, RecipeUpdateView
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
     path('edit-recipe/<int:id>', RecipeUpdateView.as_view(), name='edit recipe'),

     path('my-articles', views.my_articles, name='my articles'),
     path('create-article', ArticleCreateView.as_view(), name='create article'),
]
