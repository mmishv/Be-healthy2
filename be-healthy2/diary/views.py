from django.shortcuts import render

from diary.models import Meal


def index(request):
    return render(request, 'diary/diary.html', {
        'meals': Meal.objects.filter(user=request.user)
    })
