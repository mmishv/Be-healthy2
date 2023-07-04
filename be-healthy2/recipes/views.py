from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from recipes.forms import CreateRecipeForm, IngredientFormSet
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
    form_class = CreateRecipeForm
    success_url = reverse_lazy('main recipes')

    def __init__(self, **kwargs):
        super().__init__()
        self.object = None

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = IngredientFormSet()
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        self.object = None
        form = CreateRecipeForm(request.POST, request.FILES)
        formset = IngredientFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        form.save_m2m()
        formset.instance = self.object
        formset.instance.user = self.request.user
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy('my recipes')
    pk_url_kwarg = 'id'


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    template_name = 'recipes/edit_recipe.html'
    form_class = CreateRecipeForm
    formset_class = IngredientFormSet
    success_url = reverse_lazy('my recipes')

    def __init__(self, **kwargs):
        super().__init__()
        self.object = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = get_object_or_404(Recipe, id=self.kwargs['id'])
        formset = IngredientFormSet(instance=self.object)
        context['formset'] = formset
        return context

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Recipe, id=self.kwargs['id'])
        recipe = self.object
        form = CreateRecipeForm(is_image_required=False)
        formset = IngredientFormSet(initial=[
            {'product': p['product_id'], 'unit': p['unit'], 'quantity': p['quantity']}
            for p in recipe.ingredient_amount.values()], extra=recipe.ingredient_amount.values().count())
        return self.render_to_response(self.get_context_data(recipe=recipe, form=form, formset=formset,
                                                             category_names=recipe.categories.all().values_list(
                                                                 'name', flat=True)))

    def post(self, request, *args, **kwargs):
        self.object = get_object_or_404(Recipe, id=self.kwargs['id'])
        form = CreateRecipeForm(request.POST, request.FILES, is_image_required=False, instance=self.object)
        formset = IngredientFormSet(request.POST, instance=self.object)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object.categories.clear()
        self.object.ingredients.clear()
        self.object = form.save(commit=False)
        form.instance.save()
        form.save_m2m()
        for form in formset.forms:
            instance = form.save(commit=False)
            instance.recipe = self.object
            instance.save()
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        return redirect(self.get_success_url())
