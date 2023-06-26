from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms

from userprofile.models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Логин', min_length=5, max_length=150, required=True,
                               widget=forms.TextInput(attrs={'class': "form-control col-sm-8"}))
    password1 = forms.CharField(label='Пароль', min_length=8, widget=forms.PasswordInput(
        attrs={'class': "form-control col-sm-8"}), required=True)
    password2 = forms.CharField(label='Подтвердите пароль', min_length=8, widget=forms.PasswordInput(
        attrs={'class': "form-control col-sm-8"}), required=True)

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(RegistrationForm, self).form_valid(form)

    def username_clean(self):
        username = self.cleaned_data['username']
        new = Profile.objects.filter(username=username)
        if new.count():
            raise ValidationError("К сожалению, такой логин уже занят")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            None,
            self.cleaned_data['password1']
        )
        user = Profile(user=user)
        user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', min_length=5, max_length=150, required=True,
                               widget=forms.TextInput(attrs={'class': "form-control col-sm-8"}))
    password = forms.CharField(label='Пароль',  widget=forms.PasswordInput(
        attrs={'class': "form-control col-sm-8"}), required=True)

    def username_clean(self):
        username = self.cleaned_data['username']
        new = Profile.objects.filter(username=username)
        if not new.count():
            raise forms.ValidationError('Пользователя с таким логином не существует')
        return username

    def clean_password(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = Profile.objects.get(username=username)
        if user and not user.check_password(password):
            raise forms.ValidationError('Неверный пароль')
