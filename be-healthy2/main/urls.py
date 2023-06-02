from django.urls import path
from . import views
from .views import FullArticleView

urlpatterns = [
    path('', views.index, name='main'),
    path('calculate/', views.calculate, name='calculate'),
    path('article/<int:article_id>/<slug:slug>', FullArticleView.as_view(), name='article details')
]