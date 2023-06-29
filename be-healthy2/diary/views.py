import datetime
from django.shortcuts import render
from datetime import datetime as dt
from diary.models import Meal
from userprofile.models import Profile


def get_current_page(request):
    return get_diary_page(request, f'{datetime.date.today()}')


def get_page_by_date(request, year, month, day):
    return get_diary_page(request, f'{year}-{month}-{day}')


def get_diary_page(request, date):
    page_date = dt.strptime(date, "%Y-%m-%d").date()
    start_time = dt.combine(page_date, datetime.time.min)
    end_time = dt.combine(page_date, datetime.time.max)
    return render(request, 'diary/diary.html', {
        'profile': Profile.objects.get(user=request.user),
        'meals': Meal.objects.filter(user=request.user, date__range=(start_time, end_time)),
        'total': Meal.get_daily_total(request.user, page_date),
        'date': date,
    })
