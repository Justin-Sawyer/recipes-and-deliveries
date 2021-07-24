from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_home, name='blog-home'),
    path('articles', views.all_blog_articles, name='blog-articles'),
]
