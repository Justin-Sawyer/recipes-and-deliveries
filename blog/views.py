from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower

from .models import Post, Category, Tag
from .forms import BlogPostForm, NewTagsForm, NewCategoriesForm
from profiles.models import UserProfile
from django.contrib.auth.models import User


def blog_home(request):
    """ A view to return the blog home page """
    return render(request, 'blog/blog-home.html')


def all_blog_articles(request):
    """ A view to return all blog articles """
    posts = Post.objects.all().order_by('-pk')
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

    template = 'blog/blog-articles.html'

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
    return render(request, template, context)


def article(request, post_id):
    """ A view to show an individual blog article """
    post = get_object_or_404(Post, pk=post_id)

    context = {
        'post': post
    }

    return render(request, 'blog/article.html', context)


@login_required
def add_post(request):
    """ Add a product to the store """
    if request.method == 'POST':
        """ Gets username as author """
        author = get_object_or_404(User, id=request.user.id)
        # new_tag_form = NewTagsForm(request.POST)
        posts_form = BlogPostForm(request.POST, request.FILES)
        form_temp = posts_form.save(commit=False)
        form_temp.author = author
        # Check button for adding further posts
        add_more_posts = request.POST.getlist('add-more-posts')
        # print(request.POST)
        if posts_form.is_valid():
            # form_temp = posts_form.save(commit=False)
            postsform = posts_form.save()
            new_post = Post.objects.get(id=postsform.id)
            new_tags_form = NewTagsForm(request.POST)
            if new_tags_form.data['tagname']:
                # x = new_tags_form.save(commit=False)
                # print(x.id)
                new_tagname = new_tags_form.data['tagname']
                # print(new_tagname)
                tagname_collection = Tag.objects.all()
                # print(tagname_collection)
                # existing_tagname = Tag.objects.get(tagname__in=new_tagname)
                # print(existing_tagname)
                existing_tagname = Tag.objects.filter(tagname=new_tagname)
                if existing_tagname:
                    existing_tagname_id = tagname_collection.get(id__in=existing_tagname)
                    new_post.tag.add(existing_tagname_id)
                # print(exisiting_tagname_id)
                if not existing_tagname:
                    # tagname_collection.insert_one(new_tagname)
                    new_tags_form.is_valid()
                    newtag = new_tags_form.save()
                # print(newtag.id)
                    new_post.tag.add(newtag)
                # else:
                    # new_post.tag.add(existing_tagname_id)
                    # new_post.tag.add(exisiting_tagname_id)
                    # new_post.tag.add(existing_tagname)
                # postsform.save()
                # tagname = new_tags_form.data['tagname']
                # NewTagsForm.save()
                # new_tags_form =
            # new_tag_form = NewTagsForm(request.POST)
            # new_tag_form.GET.
            # print(new_tag_form.tagname)
            # NewTagsForm(request.POST)
            # print(NewTagsForm)
            # print(request.POST)
            # if new_tag_form.is_valid():
                # new_tag = new_tag_form.save(commit=False)
                # tagname = Post.objects.create(new_tag)
                # form_temp.tag.add(tagname)
                # print(new_tag)
                # print(new_tag.id)
                # newtag = new_tag.id
                # print(newtag)
                # new_tag_id = Tag.objects.get(id=new_tag.id)
                # print(new_tag_id)
                # form_temp.tag = new_tag_form
                # new_tag = request.new_tag_form.get("tagname")
                # new_tag = get_object_or_404(Tag, id=request.tagname)
                # form_temp.tag.add(new_tag.id)
                # print(form_temp.tag)
                # form.tag.add(newtag)
                # saved_form = posts_form.save()
                # if newtag is None:
                # posts_form.save()
                # new_tag_form.save()
                # saved_form.tag.add(newtag)
                # new_tag.delete
            # else:
                # posts_form.save()
                # saved_form = posts_form.save()
                # new_tag_form.save()
                # saved_form.tag.add(newtag)
            new_category_form = NewCategoriesForm(request.POST)
            if new_category_form.data['friendly_name']:
                """new_category_form.is_valid()
                newcategory = new_category_form.save()
                new_post.category.add(newcategory)"""
                new_category_name = new_category_form.data['friendly_name']
                category_collection = Category.objects.all()
                existing_category_name = (
                    Category.objects.filter(friendly_name=new_category_name))
                if existing_category_name:
                    existing_category_name_id = (
                        category_collection.get(id__in=existing_category_name))
                    new_post.category.add(existing_category_name_id)
                if not existing_category_name:
                    new_category_form.is_valid()
                    newcategory = new_category_form.save()
                    new_post.category.add(newcategory)
            messages.success(request, 'Successfully added post!')
            if add_more_posts:
                return redirect(reverse('add_post'))
            else:
                return redirect(reverse('blog-articles'))
        else:
            messages.error(request, 'Failed to add your post \
                Please ensure the form is valid.')
    else:
        new_category_form = NewCategoriesForm
        new_tag_form = NewTagsForm
        posts_form = BlogPostForm
    template = 'blog/add_post.html'
    context = {
        'posts_form': posts_form,
        'new_tag_form': new_tag_form,
        'new_category_form': new_category_form,
    }

    return render(request, template, context)


@login_required
def edit_post(request, post_id):
    """ Edit a product in the store """

    author = get_object_or_404(User, id=request.user.id)
    user = request.user
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.author or request.user.is_superuser:
        if request.method == 'POST':
            new_tag_form = NewTagsForm(request.POST)
            posts_form = BlogPostForm(request.POST,
                                      request.FILES,
                                      instance=post)
            if posts_form.is_valid():
                postsform = posts_form.save()
                new_post = Post.objects.get(id=postsform.id)
                new_tags_form = NewTagsForm(request.POST)
                if new_tags_form.data['tagname']:
                    new_tagname = new_tags_form.data['tagname']
                    tagname_collection = Tag.objects.all()
                    existing_tagname = Tag.objects.filter(tagname=new_tagname)
                    if existing_tagname:
                        existing_tagname_id = tagname_collection.get(id__in=existing_tagname)
                        new_post.tag.add(existing_tagname_id)
                    if not existing_tagname:
                        new_tags_form.is_valid()
                        newtag = new_tags_form.save()
                        new_post.tag.add(newtag)
                    """new_tags_form.is_valid()
                    newtag = new_tags_form.save()
                    new_post.tag.add(newtag)
                    new_tagname = new_tags_form.data['tagname']
                    # list = [new_tagname][0].split()
                    # print(list)
                    tagname_collection = Tag.objects.all()
                    if existing_tagname:
                        existing_tagname_id = tagname_collection.get(id__in=existing_tagname)
                        new_post.tag.add(existing_tagname_id)
                    for word in list:
                        # print(word)
                        # existing_tagname = [Tag.objects.filter(tagname=word)]
                        # print(existing_tagname)
                        if existing_tagname:
                            for tag in existing_tagname:
                                print(tag)
                                # tag_id = Tag.objects.get(id__in=tag)
                                print(Tag.objects.filter(tagname=tag))
                                # print(tag_id)
                            #for word in list:
                            # existing_tagname_id = [
                                # tagname_collection.get(pk__in=existing_tagname)][0].slice()
                            # print(existing_tagname_id)
                                # new_post.tag.add(existing_tagname_id)
                        if not existing_tagname:
                            for word in list:
                                new_tags_form.is_valid()
                                newtag = new_tags_form.save()
                                new_post.tag.add(newtag)
                                new_tag_form = NewTagsForm({'tagname': word}, instance=Tag())
                                newtag = new_tag_form.save()
                                new_post.tag.add(newtag)
                    # else:
                        # new_post.tag.add(existing_tagname_id)"""
                new_category_form = NewCategoriesForm(request.POST)
                if new_category_form.data['friendly_name']:
                    new_category_name = new_category_form.data['friendly_name']
                    category_collection = Category.objects.all()
                    existing_category_name = (
                        Category.objects.filter(friendly_name=new_category_name))
                    if existing_category_name:
                        existing_category_name_id = (
                            category_collection.get(id__in=existing_category_name))
                        new_post.category.add(existing_category_name_id)
                    if not existing_category_name:
                        new_category_form.is_valid()
                        newcategory = new_category_form.save()
                        new_post.category.add(newcategory)
                messages.success(request, 'Successfully updated post!')
                return redirect(reverse('article', args=[post.id]))
            else:
                messages.error(request, 'Failed to edit post \
                    Please ensure the form is valid.')
        else:
            new_category_form = NewCategoriesForm
            new_tag_form = NewTagsForm
            posts_form = BlogPostForm(instance=post)
            messages.warning(request, f'You are editing {post.title}')
    else:
        messages.error(request, 'Sorry, only the post author can do that!')
        return redirect(reverse('home'))

    template = 'blog/edit_post.html'
    context = {
        'posts_form': posts_form,
        'new_tag_form': new_tag_form,
        'new_category_form': new_category_form,
        'post': post,
        'edit_article': True,
    }

    return render(request, template, context)


@login_required
def delete_post(request, post_id):
    """ Delete a products from the store """
    """if not request.user.is_superuser:
        messages.error(request, 'Sorry, only storeowners can do that!')
        return redirect(reverse('home'))"""
    post = get_object_or_404(Post, pk=post_id)

    if request.user == post.author or request.user.is_superuser:
        post.delete()
        messages.success(request, 'Post successfully deleted!')
        return redirect(reverse('blog-articles'))
    else:
        messages.error(request, 'Sorry, only post authors can do that!')
        return redirect(reverse('home'))
