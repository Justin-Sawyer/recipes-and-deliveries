from django.shortcuts import render

from .models import Post, Category, Tag
# from django.http import HttpResponse

posts= [
    {
        'author': 'justins',
        'title': 'Blog Post 1',
        'categories': 'categories',
        'tags': 'how to',
        'tagline': 'A summary of the post',
        'image': '',
        'content': 'This is what the post is about',
        'date_posted':  'June 22nd, 1972',
    },
    {
        'author': 'justinsawyer',
        'title': 'Blog Post 2',
        'categories': 'categories',
        'tags': 'cooking tip',
        'tagline': 'Post summary',
        'image': '',
        'content': 'This is a post is about cooking',
        'date_posted':  'December 8th, 1986',
    }
]


def blog_home(request):
    """ A view to return the blog home page """
    return render(request, 'blog/blog-home.html')


def all_blog_articles(request):
    """ A view to return all blog articles """
    posts = Post.objects.all().order_by('-title')

    template = 'blog/blog-articles.html'

    context = {
        'posts': posts
    }
    return render(request, template, context)

