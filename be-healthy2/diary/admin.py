from django.contrib import admin

from diary.models import Meal, MealProduct


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('user', 'date')


admin.site.register(MealProduct)

