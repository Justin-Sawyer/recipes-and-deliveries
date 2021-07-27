from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from blog.models import Post, Category, Tag
from products.models import Product
from django.contrib.auth.models import User


def index(request):
    """ A view to return the index page """
    return render(request, 'home/index.html')


def guarantee(request):
    """ A view to return the R&D guarantee page """
    return render(request, 'home/guarantee.html')

def search_result(request):
    """ A view to return the R&D guarantee page """
    posts = Post.objects.all().order_by('-pk')
    blog_categories = Category.objects.all().order_by('-pk')
    tags = Tag.objects.all().order_by('-pk')
    users = User.objects.all().order_by('-pk')
    products = Product.objects.all().order_by('-pk')

    post_query = None
    product_query = None

    if request.GET:
        # Sort blog articles by category
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            posts = posts.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
            
        # Sort blog articles by tag
        if 'tag' in request.GET:
            tags = request.GET['tag'].split(',')
            posts = posts.filter(tag__tagname__in=tags)
            tags = Tag.objects.filter(tagname__in=tags)

        if 'author' in request.GET:
            authors = request.GET['author'].split(',')
            posts = posts.filter(author_id__username__in=authors)
            authors = User.objects.filter(username__in=authors)

        if 'q' in request.GET:
            post_query = request.GET['q']
            product_query = request.GET['q']
            if not post_query and not product_query:
                messages.error(request,
                               "You didn't enter any search criteria!")
                return redirect(reverse('home'))

            post_queries = Q(title__icontains=post_query) | Q(
                tagline__icontains=post_query) | Q(
                content__icontains=post_query)
            posts = posts.filter(post_queries)

            product_queries = Q(name__icontains=product_query) | Q(
                description__icontains=product_query)
            products = products.filter(product_queries)

    context = {
        'posts': posts,
        'users': users,
        'blog_categories': blog_categories,
        'tags': tags,
        'products': products,
        'post_search_term': post_query,
        'product_search_term': product_query,
    }
    return render(request, 'home/search_result.html', context)
