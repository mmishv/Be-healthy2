import datetime

from django.urls import path
from . import views
from .views import MealDeleteView

urlpatterns = [
    path(f'{datetime.date.today()}', views.get_current_page, name='diary today'),
    path('<int:year>-<int:month>-<int:day>', views.get_page_by_date, name='diary'),
    path('create-meal/<int:year>-<int:month>-<int:day>', views.MealCreateView.as_view(), name='create meal'),
    path('delete-meal/<int:year>-<int:month>-<int:day>/<int:id>', MealDeleteView.as_view(), name='delete meal'),
]
