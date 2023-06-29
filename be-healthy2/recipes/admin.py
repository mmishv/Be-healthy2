from django.contrib import admin

from recipes.models import Recipe, Ingredient, Product, RecipeCategory


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', 'moderated', )


admin.site.register(Ingredient)
admin.site.register(Product)
admin.site.register(RecipeCategory)
