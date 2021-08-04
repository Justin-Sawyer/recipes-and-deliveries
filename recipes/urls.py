from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_recipes, name='all_recipes'),
    path('<int:recipe_id>/', views.recipe, name='recipe'),
    path('add/', views.add_recipe, name='add_recipe'),
]