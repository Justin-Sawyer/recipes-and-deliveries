from django.contrib import admin
from .models import Recipe, Ingredient


class IngredientInline(admin.TabularInline):
    model = Ingredient



class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline, ]

    list_display = (
        'title',
        'intro',
        'prep_time',
        'cook_time',
        'servings',
    )

    ordering = ('title',)


admin.site.register(Recipe, RecipeAdmin)
