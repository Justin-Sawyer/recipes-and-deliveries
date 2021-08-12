from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
from django.http import HttpResponseRedirect

from .models import Recipe, Ingredient, Category, Tag
from .forms import (
    RecipeForm, IngredientFormSet, NewCategoriesForm,
    NewTagsForm)
from django.contrib.auth.models import User

from random import shuffle

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
    """ A view to show an individual recipe and random others in side bar """
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    # other_recipes = Recipe.objects.exclude(id=recipe.id).order_by('-pk')
    other_recipes = list(Recipe.objects.exclude(id=recipe.id))
    shuffle(other_recipes)

    votes = get_object_or_404(Recipe, id=recipe.id)
    total_votes = votes.total_votes()

    liked = False
    if votes.votes.filter(id=request.user.id).exists():
        liked = True

    context = {
        'recipe': recipe,
        'other_recipes': other_recipes,
        'total_votes': total_votes,
        'liked': liked,
    }

    return render(request, 'recipes/recipe.html', context)


@login_required
def vote(request, pk):
    recipe = get_object_or_404(Recipe, id=request.POST.get('recipe_id'))
    voted = False
    if recipe.votes.filter(id=request.user.id).exists():
        recipe.votes.remove(request.user)
        voted = False
    else:
        recipe.votes.add(request.user)
        voted = True
    return HttpResponseRedirect(reverse('recipe', args=[str(pk)]))


@login_required
def add_recipe(request):
    """ Gets username as author """
    author = get_object_or_404(User, id=request.user.id)

    """ Check button for adding further recipes """
    add_more_recipes = request.POST.getlist('add-more-recipes')

    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES)
        recipe_form_temp = recipe_form.save(commit=False)

        """ Append user (post author) to form for submitting """
        recipe_form_temp.author = author
        if recipe_form.is_valid():
            recipe = recipe_form.save()
            formset = IngredientFormSet(request.POST, instance=recipe)
            if formset.is_valid():
                formset.save()

            """ Handle new vs existing tags """
            new_tags_form = NewTagsForm(request.POST)
            if new_tags_form.data['tagname']:
                new_tagname = new_tags_form.data['tagname']
                tagname_collection = Tag.objects.all()
                existing_tagname = Tag.objects.filter(tagname=new_tagname)
                if existing_tagname:
                    existing_tagname_id = tagname_collection.get(id__in=existing_tagname)
                    recipe.tag.add(existing_tagname_id)
                if not existing_tagname:
                    new_tags_form.is_valid()
                    newtag = new_tags_form.save()
                    recipe.tag.add(newtag)

            """ Handle new vs exiting categories """
            new_category_form = NewCategoriesForm(request.POST)
            if new_category_form.data['friendly_name']:
                new_category_name = new_category_form.data['friendly_name']
                category_collection = Category.objects.all()
                existing_category_name = (
                    Category.objects.filter(friendly_name=new_category_name))
                if existing_category_name:
                    existing_category_name_id = (
                        category_collection.get(id__in=existing_category_name))
                    recipe.category.add(existing_category_name_id)
                if not existing_category_name:
                    new_category_form.is_valid()
                    newcategory = new_category_form.save()
                    recipe.category.add(newcategory)
                    
            messages.success(request, 'Successfully added recipe!')

            """ Handle redirect according to whether
            Further Recipes is checked or not """
            if add_more_recipes:
                return redirect(reverse('add_recipe'))
            else:
                return redirect(reverse('all_recipes'))
        else:
            messages.error(request, 'Failed to add your post \
                Please ensure the form is valid.')
    else:
        recipe_form = RecipeForm
        formset = IngredientFormSet
        new_category_form = NewCategoriesForm
        new_tag_form = NewTagsForm

    template = 'recipes/add_recipe.html'

    context = {
        'recipe_form': recipe_form,
        'formset': formset,
        'new_tag_form': new_tag_form,
        'new_category_form': new_category_form,
    }

    return render(request, template, context)


@login_required
def edit_recipe(request, recipe_id):

    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredient_count = recipe.ingredients.all().count()

    if request.user == recipe.author or request.user.is_superuser:
        if request.method == 'POST':
            recipe_form = RecipeForm(request.POST,
                                     request.FILES,
                                     instance=recipe)
            formset = IngredientFormSet(request.POST, instance=recipe)

            if recipe_form.is_valid():
                recipe = recipe_form.save()
                if formset.is_valid():
                    formset.save()

                """ Handle new vs existing tags """
                new_tags_form = NewTagsForm(request.POST)
                if new_tags_form.data['tagname']:
                    new_tagname = new_tags_form.data['tagname']
                    tagname_collection = Tag.objects.all()
                    existing_tagname = Tag.objects.filter(tagname=new_tagname)
                    if existing_tagname:
                        existing_tagname_id = tagname_collection.get(
                            id__in=existing_tagname)
                        recipe.tag.add(existing_tagname_id)
                    if not existing_tagname:
                        new_tags_form.is_valid()
                        newtag = new_tags_form.save()
                        recipe.tag.add(newtag)

                """ Handle new vs exiting categories """
                new_category_form = NewCategoriesForm(request.POST)
                if new_category_form.data['friendly_name']:
                    new_category_name = new_category_form.data['friendly_name']
                    category_collection = Category.objects.all()
                    existing_category_name = (
                        Category.objects.filter(
                            friendly_name=new_category_name))
                    if existing_category_name:
                        existing_category_name_id = (
                            category_collection.get(
                                id__in=existing_category_name))
                        recipe.category.add(existing_category_name_id)
                    if not existing_category_name:
                        new_category_form.is_valid()
                        newcategory = new_category_form.save()
                        recipe.category.add(newcategory)
                        
                messages.success(request, 'Successfully updated recipe!')
                return redirect(reverse('recipe', args=[recipe.id]))
            else:
                messages.error(request, 'Failed to edit your recipe \
                    Please ensure the form is valid.')
        else:
            recipe_form = RecipeForm(instance=recipe)
            formset = IngredientFormSet(instance=recipe)
            new_category_form = NewCategoriesForm
            new_tag_form = NewTagsForm
            messages.warning(request, f'You are editing {recipe.title}')
    else:
        messages.error(request, 'Sorry, only the recipe author can do that!')
        return redirect(reverse('home'))
    
    template = 'recipes/edit_recipe.html'

    context = {
        'recipe': recipe,
        'recipe_form': recipe_form,
        'formset': formset,
        'new_tag_form': new_tag_form,
        'new_category_form': new_category_form,
        'ingredient_count': ingredient_count,
    }

    return render(request, template, context)


@login_required
def delete_recipe(request, recipe_id):
    """ Delete a recipe """
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.user == recipe.author or request.user.is_superuser:
        recipe.delete()
        messages.success(request, 'Recipe successfully deleted!')
        return redirect(reverse('all_recipes'))
    else:
        messages.error(request, 'Sorry, only the recipe author can do that!')
        return redirect(reverse('home'))
