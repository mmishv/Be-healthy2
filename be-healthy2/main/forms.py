from django import forms

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

