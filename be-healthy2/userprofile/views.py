from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.views import View

from userprofile.forms import LoginForm, RegistrationForm


class RegisterView(View):
    def get(self, request):
        return render(request, 'userprofile/auth.html',
                      {'reg_form': RegistrationForm(), 'log_form': LoginForm()})

    def post(self, request):
        reg_form = RegistrationForm(request.POST)
        if reg_form.is_valid():
            user = reg_form.save()
            login(request, user)
            return redirect('/')
        return render(request, 'userprofile/auth.html',
                      {'reg_form': reg_form, 'log_form': LoginForm()})


class LoginView(View):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Пользователя с такими данными не существует')
            return render(request, 'userprofile/auth.html',
                          {'reg_form': RegistrationForm(), 'log_form': LoginForm(request.POST)})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')
