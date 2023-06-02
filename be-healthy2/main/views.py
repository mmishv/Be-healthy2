from django.shortcuts import render
from .forms import CalculatorForm


def index(request):
    return render(request, 'main/main.html', {
        'form': CalculatorForm()
    })


def calculate(request):
    result = 0
    if request.method == 'GET':
        form = CalculatorForm(request.GET)
        if form.is_valid():
            sex = request.GET['sex']
            weight = request.GET['weight']
            height = request.GET['height']
            age = request.GET['age']
            activity = request.GET['activity']
            goal = request.GET['goal']
            result = 447.6 + 9.2 * float(weight) + 3.1 * float(height) - 4.3 * float(age) if sex == 'F' else \
                88.36 + 13.4 * float(weight) + 4.8 * float(height) - 5.7 * float(age)
            result *= float(activity)*float(goal)
            result = int(result)
    return render(request, 'main/main.html', {
        'form': CalculatorForm(request.GET),
        'result': result,
    })
