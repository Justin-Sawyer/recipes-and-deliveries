from django.shortcuts import render

from .models import Post, Category, Tag


def blog_home(request):
    """ A view to return the blog home page """
    return render(request, 'blog/blog-home.html')


def all_blog_articles(request):
    """ A view to return all blog articles """
    posts = Post.objects.all()

    template = 'blog/blog-articles.html'

    context = {
        'posts': posts
    }
    return render(request, template, context)
