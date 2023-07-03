from django import forms
from django.forms import formset_factory, TextInput, NumberInput, Textarea

from main.models import Article
from recipes.models import UNIT_CHOICES, Product

SEX_CHOICES = [
    ('female', 'Женский'),
    ('male', 'Мужской'),
]

ACTIVITY_CHOICES = [
    (1, 'Без учета физ. нагрузки'),
    (1.2, 'Сидячий образ жизни'),
    (1.375, 'Легкая активность (1-2 раза в неделю)'),
    (1.55, 'Умеренная активность (3-5 раз в неделю)'),
    (1.725, 'Высокая активность (более 5 раз в неделю)'),
    (1.9, 'Очень высокая активность (профессиональный спорт)'),
]

GOAL_CHOICES = [
    (1, 'Поддержание веса'),
    (1.2, 'Набор веса'),
    (0.8, 'Снижение веса'),
]


class CalculatorForm(forms.Form):
    sex = forms.ChoiceField(
        choices=SEX_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='female'
    )
    height = forms.IntegerField(label='Рост', widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                              'placeholder': 'Рост, см'}))
    weight = forms.FloatField(label='Вес', widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Вес, кг'}))
    age = forms.IntegerField(label='Возраст', widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                              'placeholder': 'Возраст'}))
    activity = forms.ChoiceField(
        choices=ACTIVITY_CHOICES,
        label='Физическая активность',
        widget=forms.Select(attrs={'class': 'form-control col-sm-8'})
    )
    goal = forms.ChoiceField(
        choices=GOAL_CHOICES,
        label='Цель',
        widget=forms.Select(attrs={'class': 'form-control col-sm-8'})
    )


class MixerProductForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control col-sm-6', 'required': 'true'}))
    unit = forms.ChoiceField(choices=UNIT_CHOICES,
                             widget=forms.Select(attrs={'class': 'form-control col-sm-2', 'required': 'true'}))
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control col-sm-2', 'required': 'true', 'placeholder': "кол-во"}))


MixerProductFormSet = formset_factory(MixerProductForm, extra=1)


class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'full_text', 'categories']
        widgets = {
            'title': TextInput(attrs={'placeholder': "Например, Правильное питание - верный путь к здоровью",
                                      'class': "form-control", 'required': 'true'}),
            'full_text': Textarea(
                attrs={'class': "form-control col-sm-8", 'required': 'true', 'rows': '5'}),
            'categories': forms.CheckboxSelectMultiple(),
        }
