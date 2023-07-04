from django.urls import path

from main.views import ArticleCreateView, ArticleDeleteView, ArticleUpdateView, ArticleCategoryCreateView, \
     ArticleCategoryUpdateView, ArticleCategoryDeleteView
from recipes.views import RecipeDeleteView, RecipeUpdateView, ProductCreateView, ProductUpdateView, ProductDeleteView, \
     RecipeCategoryCreateView, RecipeCategoryUpdateView, RecipeCategoryDeleteView
from . import views

urlpatterns = [
     path('auth', views.RegisterView.as_view(), name='auth'),
     path('register', views.RegisterView.as_view(), name='register'),
     path('login', views.LoginView.as_view(), name='login'),
     path('logout', views.LogoutView.as_view(), name='logout'),

     path('main', views.get_about_me, name='about me'),
     path('update', views.ProfileAboutMeUpdateView.as_view(), name='update parameters'),
     path('edit', views.MainInfoProfileUpdateView.as_view(), name='edit main info'),

     path('my-recipes', views.my_recipes, name='my recipes'),
     path('delete-recipe/<int:id>', RecipeDeleteView.as_view(), name='delete recipe'),
     path('edit-recipe/<int:id>', RecipeUpdateView.as_view(), name='edit recipe'),

     path('my-articles', views.my_articles, name='my articles'),
     path('create-article', ArticleCreateView.as_view(), name='create article'),
     path('delete-article/<int:id>', ArticleDeleteView.as_view(), name='delete article'),
     path('edit-article/<int:id>', ArticleUpdateView.as_view(), name='edit article'),

     path('admin/users', views.admin_section_users, name='user management'),
     path('admin/change-role/<int:user_id>', views.change_role, name='change role'),
     path('admin/delete-user/<int:user_id>', views.delete_user, name='delete user'),

     path('admin/products', views.admin_section_products, name='product management'),
     path('admin/create-product', ProductCreateView.as_view(), name='create product'),
     path('admin/edit-product/<int:id>', ProductUpdateView.as_view(), name='edit product'),
     path('admin/delete-product/<int:id>', ProductDeleteView.as_view(), name='delete product'),

     path('admin/recipe-categories', views.admin_section_recipe_categories, name='recipe category management'),
     path('admin/create-recipe-category', RecipeCategoryCreateView.as_view(), name='create recipe category'),
     path('admin/edit-recipe-category/<int:id>', RecipeCategoryUpdateView.as_view(), name='edit recipe category'),
     path('admin/delete-recipe-category/<int:id>', RecipeCategoryDeleteView.as_view(), name='delete recipe category'),

     path('admin/article-categories', views.admin_section_article_categories, name='article category management'),
     path('admin/create-article-category', ArticleCategoryCreateView.as_view(), name='create article category'),
     path('admin/edit-article-category/<int:id>', ArticleCategoryUpdateView.as_view(), name='edit article category'),
     path('admin/delete-article-category/<int:id>', ArticleCategoryDeleteView.as_view(), name='delete article category'),
]
