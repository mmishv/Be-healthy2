from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView

from recipes.forms import AddRecipeForm, IngredientFormSet
from recipes.models import Recipe, RecipeCategory


def index(request):
    recipes = Recipe.objects.filter(moderated=True).order_by('-date')
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/recipes.html', {
        'categories': RecipeCategory.objects.all(),
        'page': page,
    })


def category(request, category_id, slug):
    recipes = Recipe.objects.filter(categories__id=category_id, moderated=True).order_by('-date')
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/recipes.html', {
        'categories': RecipeCategory.objects.all(),
        'page': page,
    })


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = 'recipes/new_recipe.html'
    form_class = AddRecipeForm
    success_url = '/recipes'

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = IngredientFormSet()
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        self.object = None
        form = AddRecipeForm(request.POST, request.FILES)
        formset = IngredientFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset, request.user)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset, user):
        self.object = form.save(commit=False)
        self.object.author = user
        self.object.save()
        form.save_m2m()
        formset.instance = self.object
        formset.instance.user = self.request.user
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))
