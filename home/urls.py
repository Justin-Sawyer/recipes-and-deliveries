from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('guarantee/', views.guarantee, name='guarantee'),
    # path('blog/', views.all_blog_articles, name='blog-home'),
]
