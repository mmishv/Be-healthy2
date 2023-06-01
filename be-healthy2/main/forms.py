from django.forms import ModelForm, NumberInput, Select, RadioSelect
from .models import Calculator


class CalculatorForm(ModelForm):
    class Meta:
        model = Calculator
        fields = '__all__'
        widgets = {'sex': RadioSelect(choices=(('male', "мужской"),
                                               ('female', "женский"))),
                   'height': NumberInput(),
                   'weight': NumberInput(),
                   'age': NumberInput(),
                   'activity': Select(choices=((1, "Без учета физ. нагрузки"),
                                               (1.2, "Сидячий образ жизни"),
                                               (1.375, "Небольшая активность"),
                                               (1.55, "Умеренная активность"),
                                               (1.725, "Высокая активность"),
                                               (1.9, "Очень высокая активность"))),
                   'goal': Select(choices=((0.8, "Снизить вес"), (1, "Поддерживать вес"), (1.2, "Набрать вес")))}
