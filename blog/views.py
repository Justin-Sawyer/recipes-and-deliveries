from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Post, Category, Tag


def blog_home(request):
    """ A view to return the blog home page """
    return render(request, 'blog/blog-home.html')


def all_blog_articles(request):
    """ A view to return all blog articles """
    posts = Post.objects.all().order_by('-pk')
    categories = None
    tags = None
    sort = None
    direction = None
    search = None

    if request.GET:
        # Sort products via the dropdown menu
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'title':
                sortkey = 'lower_title'
                posts = posts.annotate(lower_title=Lower('title'))
            if sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            posts = posts.order_by(sortkey)

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
        
        # Searching articles by name or description
        if 'q' in request.GET:
            search = request.GET['q']
            if not search:
                messages.error(request,
                               "You didn't enter any search criteria!")
                return redirect(reverse('blog-articles'))

            queries = Q(title__icontains=search) | Q(
                content__icontains=search)
            posts = posts.filter(queries)
    
    current_sorting = f'{sort}_{direction}'

    template = 'blog/blog-articles.html'

    context = {
        'posts': posts,
        'search_term': search,
        'current_categories': categories,
        'current_tags': tags,
        'current_sorting': current_sorting,
    }
    return render(request, template, context)


def article(request, post_id):
    """ A view to show an individual blog article """
    post = get_object_or_404(Post, pk=post_id)

    context = {
        'post': post
    }

    return render(request, 'blog/article.html', context)
