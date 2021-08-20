from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.db.models import Q

from blog.models import Post, Category, Tag
from products.models import Product
from recipes.models import Recipe
from django.contrib.auth.models import User


def index(request):
    """ A view to return the index page """
    return render(request, 'home/index.html')


def guarantee(request):
    """ A view to return the guarantee page """
    return render(request, 'home/guarantee.html')


def search_result(request):
    """ A view to return the search page """
    posts = Post.objects.all().order_by('-pk')
    recipes = Recipe.objects.all().order_by('-pk')
    blog_categories = Category.objects.all().order_by('-pk')
    tags = Tag.objects.all().order_by('-pk')
    users = User.objects.all().order_by('-pk')
    products = Product.objects.all().order_by('-pk')

    post_query = None
    product_query = None
    recipe_query = None

    if request.GET:
        # Search
        if 'q' in request.GET:
            post_query = request.GET['q']
            product_query = request.GET['q']
            recipe_query = request.GET['q']
            if not post_query and not product_query and not recipe_query:
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

            recipe_queries = Q(title__icontains=recipe_query) | Q(
                intro__icontains=recipe_query)
            recipes = recipes.filter(recipe_queries)

    context = {
        'posts': posts,
        'recipes': recipes,
        'users': users,
        'blog_categories': blog_categories,
        'tags': tags,
        'products': products,
        'post_search_term': post_query,
        'product_search_term': product_query,
        'recipe_search_term': recipe_query,
    }
    return render(request, 'home/search_result.html', context)
