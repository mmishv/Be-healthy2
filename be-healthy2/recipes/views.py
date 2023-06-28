from django.core.paginator import Paginator
from django.shortcuts import render

from recipes.models import Recipe, RecipeCategory


def index(request):
    recipes = Recipe.objects.order_by('-date')
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/recipes.html', {
        'categories': RecipeCategory.objects.all(),
        'page': page,
    })


def category(request, category_id, slug):
    recipes = Recipe.objects.filter(categories__id=category_id).order_by('-date')
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/recipes.html', {
        'categories': RecipeCategory.objects.all(),
        'page': page,
    })
