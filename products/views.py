from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
from django.http import HttpResponseRedirect

from .models import Product, Category
from .forms import ProductForm, CommentForm
from django.contrib.auth.models import User

from random import shuffle


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all().order_by('-pk')
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        # Sort products via the dropdown menu
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        # Sort products by category
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

    current_sorting = f'{sort}_{direction}'

    paginator = Paginator(products, 12)  # Show 12 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'page_obj': page_obj,
        'is_paginated': True,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show all individual product details """

    product = get_object_or_404(Product, pk=product_id)
    comment_form = CommentForm
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        name = get_object_or_404(User, id=request.user.id)
        if name.is_superuser:
            name = "recipesanddeliveries"
        comment_form_temp = comment_form.save(commit=False)
        comment_form_temp.product = product
        comment_form_temp.name = name
        if comment_form.is_valid():
            comment_form.product = product
            comment_form.name = name
            comment_form.save()
            messages.success(request, 'Successfully added comment!')
            return HttpResponseRedirect(reverse(
                'product_detail', args=[str(product_id)]))
        else:
            messages.error(request, 'It seems that your comment cannot be \
                posted. Sorry!')
            return HttpResponseRedirect(reverse(
                'product_detail', args=[str(product_id)]))

    other_products = list(Product.objects.exclude(id=product.id))
    shuffle(other_products)

    context = {
        'product': product,
        'other_products': other_products,
        'comment_form': comment_form,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only storeowners can do that!')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        add_more_products = request.POST.getlist('add-more-products')
        if form.is_valid():
            form.save()
            messages.info(request, 'Successfully added product!')
            if add_more_products:
                return redirect(reverse('add_product'))
            else:
                return redirect(reverse('products'))
        else:
            messages.error(request, 'Failed to add product \
                Please ensure the form is valid.')
    else:
        form = ProductForm
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only storeowners can do that!')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.info(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to edit product \
                Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a products from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only storeowners can do that!')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.info(request, 'Product successfully deleted!')
    return redirect(reverse('products'))
