from django.contrib import admin

from main.models import ArticleCategory, Article


@admin.register(Article)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', 'moderated', )


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
