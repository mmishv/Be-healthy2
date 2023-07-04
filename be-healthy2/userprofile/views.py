from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from main.forms import CreateArticleCategoryForm
from main.models import Article, ArticleCategory
from recipes.forms import CreateProductForm, CreateRecipeCategoryForm
from recipes.models import Recipe, Product, RecipeCategory
from userprofile.forms import LoginForm, RegistrationForm, AboutMeProfileForm, MainInfoProfileForm
from userprofile.models import Profile, RoleOptions

from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test


class AdminUserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.profile.role == RoleOptions.ADMIN

    def handle_no_permission(self):
        return JsonResponse({'message': 'Only administrators have access to this view'}, status=403)


def is_admin(user):
    return user.profile.role == RoleOptions.ADMIN


@login_required
def get_about_me(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    return render(request, 'userprofile/general/about_me.html', {'profile': profile,
                                                                 'form': AboutMeProfileForm(),
                                                                 'modal_form': MainInfoProfileForm()})


class ProfileAboutMeUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = AboutMeProfileForm
    success_url = '/profile/main'
    template_name = 'userprofile/auth.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.save()
        return super().form_valid(form)


class MainInfoProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = MainInfoProfileForm
    success_url = '/profile/main'
    template_name = 'userprofile/auth.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        return self.request.user.profile


class RegisterView(View):
    def get(self, request):
        return render(request, 'userprofile/auth.html',
                      {'reg_form': RegistrationForm(), 'log_form': LoginForm()})

    def post(self, request):
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('/profile/main')
        return render(request, 'userprofile/auth.html',
                      {'reg_form': form, 'log_form': LoginForm()})


class LoginView(View):
    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/profile/main')
        else:
            return render(request, 'userprofile/auth.html',
                          {'reg_form': RegistrationForm(), 'log_form': LoginForm(request.POST)})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('auth')


@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(author_id=request.user.id).order_by('-date')
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'userprofile/general/my_recipes.html', {'page': page, 'my_recipes': True})


@login_required
def my_articles(request):
    articles = Article.objects.filter(author_id=request.user.id).order_by('-date')
    paginator = Paginator(articles, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'userprofile/general/my_articles.html', {'page': page})


@user_passes_test(lambda u: is_admin(u))
def admin_section_users(request):
    users = User.objects.all().order_by('username')
    return render(request, 'userprofile/admin/users.html', {'users': users, 'my_id': request.user.id})


@user_passes_test(lambda u: is_admin(u))
def change_role(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.profile.role = 'A' if user.profile.role == 'U' else 'U'
    user.profile.save()
    return redirect(reverse_lazy('user management'))


@user_passes_test(lambda u: is_admin(u))
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect(reverse_lazy('user management'))


@user_passes_test(lambda u: is_admin(u))
def admin_section_products(request):
    items = Product.objects.all().order_by('name')
    form = CreateProductForm()
    return render(request, 'userprofile/admin/categories-products.html', {'items': items, 'form': form,
                                                                          'products': True, "color": "#98e294"})


@user_passes_test(lambda u: is_admin(u))
def admin_section_recipe_categories(request):
    items = RecipeCategory.objects.all().order_by('name')
    form = CreateRecipeCategoryForm()
    return render(request, 'userprofile/admin/categories-products.html', {'items': items, 'form': form,
                                                                          'recipe_categories': True,
                                                                          "color": "#e2c894"})


@user_passes_test(lambda u: is_admin(u))
def admin_section_article_categories(request):
    items = ArticleCategory.objects.all().order_by('name')
    form = CreateArticleCategoryForm()
    return render(request, 'userprofile/admin/categories-products.html', {'items': items, 'form': form,
                                                                          'article_categories': True,
                                                                          "color": "#e2c894"})


@user_passes_test(lambda u: is_admin(u))
def admin_section_articles(request):
    items = Article.objects.all().order_by('title')
    return render(request, 'userprofile/admin/recipes-articles.html', {'items': items, 'articles': True,
                                                                       "color": "#dab4e4"})


@user_passes_test(lambda u: is_admin(u))
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.delete()
    return redirect(reverse_lazy('articles management'))


@user_passes_test(lambda u: is_admin(u))
def admin_section_recipes(request):
    items = Recipe.objects.all().order_by('title')
    return render(request, 'userprofile/admin/recipes-articles.html', {'items': items, 'recipes': True,
                                                                       "color": "#a5a6db"})


@user_passes_test(lambda u: is_admin(u))
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.delete()
    return redirect(reverse_lazy('recipes management'))
