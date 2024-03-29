from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms

from userprofile.models import Profile


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

    def clean_username(self):
        username = self.cleaned_data['username']
        new = User.objects.filter(username=username)
        if new.count() > 0:
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
        Profile.objects.create(user=user)
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', min_length=5, max_length=150, required=True,
                               widget=forms.TextInput(attrs={'class': "form-control col-sm-8"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': "form-control col-sm-8"}), required=True)

    def clean_username(self):
        username = self.cleaned_data['username']
        new = User.objects.filter(username=username)
        if not new.count():
            raise forms.ValidationError('Пользователя с таким логином не существует')
        return username

    def clean_password(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.get(username=username)
        if user and not user.check_password(password):
            raise forms.ValidationError('Неверный пароль')


class AboutMeProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['sex', 'height', 'weight', 'age', 'activity', 'goal', 'calories', 'fats', 'proteins', 'carbohydrates']
        widgets = {
            'sex': forms.RadioSelect(),
            'height': forms.NumberInput(attrs={'placeholder': 'Рост, см'}),
            'weight': forms.NumberInput(attrs={'placeholder': 'Вес'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Возраст'}),
        }


class MainInfoProfileForm(forms.ModelForm):
    avatar = forms.ImageField(label='Аватар', required=False)
    first_name = forms.CharField(label='Имя', max_length=150, required=False)

    class Meta:
        model = Profile
        fields = ['avatar', 'first_name']

    user = None

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['first_name'].initial = self.user.first_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.cleaned_data['first_name']:
            if self.user:
                self.user.first_name = self.cleaned_data['first_name']
                if commit:
                    self.user.save()
        if self.cleaned_data['avatar']:
            profile.avatar = self.cleaned_data['avatar']
        if commit:
            profile.save()
        return profile
