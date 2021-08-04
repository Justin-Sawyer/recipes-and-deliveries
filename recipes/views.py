from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.core.paginator import Paginator
# from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower

from .models import Recipe, Ingredient
from .forms import RecipeForm, IngredientFormSet
from django.contrib.auth.models import User


def all_recipes(request):
    """ A view to return all recipes """
    recipes = Recipe.objects.all().order_by('-pk')
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
                recipes = recipes.annotate(lower_title=Lower('title'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            recipes = recipes.order_by(sortkey)

        # Sort blog articles by category
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            recipes = recipes.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        # Sort blog articles by tag
        if 'tag' in request.GET:
            tags = request.GET['tag'].split(',')
            recipes = recipes.filter(tag__tagname__in=tags)
            tags = Tag.objects.filter(tagname__in=tags)

        if 'author' in request.GET:
            authors = request.GET['author'].split(',')
            recipes = recipes.filter(author_id__username__in=authors)
            authors = User.objects.filter(username__in=authors)

    current_sorting = f'{sort}_{direction}'

    template = 'recipes/all_recipes.html'

    paginator = Paginator(recipes, 12)  # Show 12 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'recipes': recipes,
        'search_term': query,
        'current_categories': categories,
        'current_tags': tags,
        'current_sorting': current_sorting,
        'current_authors': authors,
        'page_obj': page_obj,
        'is_paginated': True,
    }
    return render(request, template, context)


def recipe(request, recipe_id):
    """ A view to show an individual recipe """
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    context = {
        'recipe': recipe,
    }

    return render(request, 'recipes/recipe.html', context)


@login_required
def add_recipe(request):
    """ Gets username as author """
    author = get_object_or_404(User, id=request.user.id)

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        form_temp = form.save(commit=False)

        """ Append user (post author) to form for submitting """
        form_temp.author = author
        if form.is_valid():
            recipe = form.save()
            formset = IngredientFormSet(request.POST, instance=recipe)
            if formset.is_valid():
                formset.save()
                messages.success(request, 'Successfully added recipe!')
            return redirect('/')
        else:
            messages.error(request, 'Failed to add your post \
                Please ensure the form is valid.')
    else:
        form = RecipeForm
        formset = IngredientFormSet
    
    template = 'recipes/create_recipe.html'

    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, template, context)
    

