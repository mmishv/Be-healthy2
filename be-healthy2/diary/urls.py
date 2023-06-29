import datetime

from django.urls import path
from . import views

urlpatterns = [
    path(f'{datetime.date.today()}', views.index, name='diary today'),
    path('<int:year>-<int:month>-<int:day>', views.index, name='diary'),
]
