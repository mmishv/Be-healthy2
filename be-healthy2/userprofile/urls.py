from django.urls import path
from . import views

urlpatterns = [
     path('auth', views.RegisterView.as_view(), name='auth'),
     path('register', views.RegisterView.as_view(), name='register'),
     path('login', views.LoginView.as_view(), name='login'),
     path('logout', views.LogoutView.as_view(), name='logout'),
]