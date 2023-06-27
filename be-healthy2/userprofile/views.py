from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import UpdateView

from userprofile.forms import LoginForm, RegistrationForm, AboutMeProfileForm, MainInfoProfileForm
from userprofile.models import Profile


@login_required
def get_about_me(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    return render(request, 'userprofile/general/about_me.html', {'profile': profile,
                                                                 'form': AboutMeProfileForm(),
                                                                 'modal_form': MainInfoProfileForm()})


class ProfileAboutMeUpdateView(UpdateView):
    model = Profile
    form_class = AboutMeProfileForm
    success_url = '/profile/main'
    template_name = 'userprofile/auth.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.save()
        return super().form_valid(form)


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