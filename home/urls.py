from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('guarantee/', views.guarantee, name='guarantee'),
    path('search-result/', views.search_result, name='search_result'),
    # path('blog/', views.all_blog_articles, name='blog-home'),
]
