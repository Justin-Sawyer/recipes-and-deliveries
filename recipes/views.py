from django.shortcuts import render, redirect
from .forms import RecipeForm, IngredientFormSet


def all_recipes(request):
    """ A view to return all recipes """
    """posts = Post.objects.all().order_by('-pk')
    authors = None
    categories = None
    tags = None
    sort = None
    direction = None
    query = None

    if request.GET:
        # Sort products via the dropdown menu
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'title':
                sortkey = 'lower_title'
                posts = posts.annotate(lower_title=Lower('title'))

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

        if 'author' in request.GET:
            authors = request.GET['author'].split(',')
            posts = posts.filter(author_id__username__in=authors)
            authors = User.objects.filter(username__in=authors)

    current_sorting = f'{sort}_{direction}'

    template = 'recipes/all_recipes.html'

    paginator = Paginator(posts, 12)  # Show 12 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'search_term': query,
        'current_categories': categories,
        'current_tags': tags,
        'current_sorting': current_sorting,
        'current_authors': authors,
        'page_obj': page_obj,
        'is_paginated': True,
    }
    return render(request, template, context)"""


def create_recipe(request):
    if request.method == 'GET':
        form = RecipeForm
        formset = IngredientFormSet
        return render(request,
                      'recipes/create_recipe.html',
                      {'form': form, 'formset': formset})

    elif request.method =='POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save()
            formset = IngredientFormSet(request.POST, instance=recipe)
            if formset.is_valid():
                formset.save()
            return redirect('/')
        else:
            return render(request, 'recipes/create_recipe.html', {'form': form})
