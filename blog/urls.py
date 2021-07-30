from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_home, name='blog-home'),
    path('articles/', views.all_blog_articles, name='blog-articles'),
    path('<int:post_id>/', views.article, name='article'),
    path('add/', views.add_post, name='add_post'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
]
