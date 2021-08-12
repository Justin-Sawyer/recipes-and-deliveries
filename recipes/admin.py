from django.contrib import admin
from .models import Recipe, Ingredient, Category, Tag


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
        'sku',
    )


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'tagname',
    )


class IngredientInline(admin.TabularInline):
    model = Ingredient


class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline, ]

    list_display = (
        'title',
        'author',
        'prep_time',
        'cook_time',
        'servings',
        'vote_count'
    )

    ordering = ('title',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
