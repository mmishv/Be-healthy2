from django import forms
from django.forms import TextInput, Textarea, FileInput, NumberInput

from diary.forms import custom_inlineformset_factory
from .models import Recipe, Ingredient, Product, RecipeCategory

IngredientFormSet = custom_inlineformset_factory(
    Recipe, Ingredient, extra=1, can_delete_extra=True, can_delete=True, fields=('product', 'unit', 'quantity'),
    widgets={
        'product': forms.Select(attrs={'class': 'form-control col-sm-6', 'required': 'true'}),
        'unit': forms.Select(attrs={'class': 'form-control col-sm-2', 'required': 'true'}),
        'quantity': forms.NumberInput(attrs={'class': 'form-control col-sm-2', 'required': 'true'}),
    },
)


class CreateRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        is_image_required = kwargs.pop('is_image_required', True)
        super().__init__(*args, **kwargs)
        self.fields['image'].required = is_image_required
        self.fields['categories'].required = False

    class Meta:
        model = Recipe
        fields = ('title', 'categories', 'cooking_time', 'text', 'image')
        widgets = {
            'title': TextInput(attrs={'placeholder': "Например, оладьи", 'class': "form-control", 'required': 'true'}),
            'cooking_time': NumberInput(
                attrs={'placeholder': "Например, 30", 'class': "form-control", 'required': 'true'}),
            'image': FileInput(
                attrs={'class': 'form-control-file', 'accept': "image/png, image/jpeg"}),
            'text': Textarea(
                attrs={'class': "form-control col-sm-8", 'required': 'true', 'rows': '5'}),
            'categories': forms.CheckboxSelectMultiple(),
        }


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': TextInput(attrs={'placeholder': "Название", 'class': "form-control", 'required': 'true'}),
            'calories': NumberInput(attrs={'class': "form-control col-sm-6", 'step': "0.01", 'required': 'true'}),
            'proteins': NumberInput(attrs={'class': "form-control col-sm-6", 'step': "0.01", 'required': 'true'}),
            'fats':  NumberInput(attrs={'class': "form-control col-sm-6", 'step': "0.01", 'required': 'true'}),
            'carbohydrates': NumberInput(attrs={'class': "form-control col-sm-6", 'step': "0.01", 'required': 'true'}),
        }


class CreateRecipeCategoryForm(forms.ModelForm):
    class Meta:
        model = RecipeCategory
        fields = ('name', )
        widgets = {
            'name': TextInput(attrs={'placeholder': "Название", 'class': "form-control", 'required': 'true'}),
        }
