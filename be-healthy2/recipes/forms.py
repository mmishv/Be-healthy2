from django import forms
from django.forms import TextInput, Textarea, FileInput
from django.forms.models import inlineformset_factory

from .models import Recipe, Ingredient

IngredientFormSet = inlineformset_factory(
    Recipe, Ingredient, extra=1, can_delete=True, can_delete_extra=True, fields=('product', 'unit', 'quantity'),
    widgets={
            'product': forms.Select(attrs={'class': 'form-control col-sm-6', 'required': 'true'}),
            'unit': forms.Select(attrs={'class': 'form-control col-sm-2', 'required': 'true'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control col-sm-2', 'required': 'true'}),
    },
)


class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'categories', 'cooking_time', 'text', 'image')
        widgets = {
            'title': TextInput(attrs={'placeholder': "Например, оладьи", 'class': "form-control", 'required': 'true'}),
            'cooking_time': TextInput(
                attrs={'placeholder': "Например, 30", 'class': "form-control", 'required': 'true'}),
            'image': FileInput(attrs={'class': 'form-control-file', 'required': 'true', 'accept': "image/png, image/jpeg"}),
            'text': Textarea(
                attrs={'class': "form-control col-sm-8", 'required': 'true', 'rows': '5'}),
            'categories': forms.CheckboxSelectMultiple(),
            }
