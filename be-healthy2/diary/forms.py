from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet

from diary.models import Meal, MealProduct


class CustomBaseInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra', 1)
        super().__init__(*args, **kwargs)
        self.extra = extra


def custom_inlineformset_factory(*args, **kwargs):
    kwargs['formset'] = CustomBaseInlineFormSet
    return inlineformset_factory(*args, **kwargs)


MealProductFormSet = custom_inlineformset_factory(
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
