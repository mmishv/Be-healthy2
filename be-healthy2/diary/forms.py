from django import forms
from django.forms import TextInput, inlineformset_factory

from diary.models import Meal, MealProduct


MealProductFormSet = inlineformset_factory(
    Meal, MealProduct, extra=1, can_delete=True, can_delete_extra=True, fields=('product', 'unit', 'quantity'),
    widgets={
            'product': forms.Select(attrs={'class': 'form-control col-sm-6', 'required': 'true'}),
            'unit': forms.Select(attrs={'class': 'form-control col-sm-2', 'required': 'true'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control col-sm-2', 'required': 'true'}),
    },
)


class CreateMealForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Название приёма пищи", 'class': "modal-title"}),
        required=False
    )

    class Meta:
        model = Meal
        fields = ('name',)
