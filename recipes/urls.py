from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.blog_home, name='blog-home'),
    path('create_recipe/', views.create_recipe, name='create_recipe'),
]