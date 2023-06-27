from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.views import View

from userprofile.forms import LoginForm, RegistrationForm, AboutMeProfileForm, MainInfoProfileForm
from userprofile.models import Profile


def get_about_me(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    return render(request, 'userprofile/general/about_me.html', {'profile': profile,
                                                                 'form': AboutMeProfileForm(),
                                                                 'modal_form': MainInfoProfileForm()})


class RegisterView(View):
    def get(self, request):
        return render(request, 'userprofile/auth.html',
                      {'reg_form': RegistrationForm(), 'log_form': LoginForm()})

    def post(self, request):
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('/')
        return render(request, 'userprofile/auth.html',
                      {'reg_form': form, 'log_form': LoginForm()})


class LoginView(View):
    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
        else:
            return render(request, 'userprofile/auth.html',
                          {'reg_form': RegistrationForm(), 'log_form': LoginForm(request.POST)})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')