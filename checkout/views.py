from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from bag.contexts import bag_contents
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from blog.models import Post
from recipes.models import Recipe
from django.contrib.auth.models import User

import stripe
import json


@require_POST
def cache_checkout_data(request):
    try:
        current_bag = bag_contents(request)
        discount = current_bag['discount']
        # first_recipe = current_bag['first_recipe'] or None
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
            'discount': discount,
            'first_recipe': request.POST.get('first_recipe') or "no_recipe",
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be processed right \
            now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    user_recipes = None
    first_discount_code = None
    checkout_user = None
    recipe_with_discount_code = None
    first_recipe = None

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'town_or_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'postcode': request.POST['postcode'],
            'country': request.POST['country'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            # Get client secret
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            current_bag = bag_contents(request)
            discount = current_bag['discount']
            order.vote_discount_applied = discount
            order.save()
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for gf_option, quantity in item_data[
                                'diet_requirements'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                diet_option=gf_option
                            )
                            order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in the bag isn't in our database. \
                        Please call us for assistance!"
                    ))
                    order.delete()
                    return redirect(reverse('view_bag'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success',
                                    args=[order.order_number]))
        else:
            messages.error(request, 'There was an error in your form. \
                Please double check your information.')

    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag yet")
            return redirect(reverse('products'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']

        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
        
        # Attempt to prefill the form with any info the
        # user maintains in their profile
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)

                order_form = OrderForm(initial={
                    'full_name': profile.default_full_name,
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })

                checkout_user = get_object_or_404(User, id=request.user.id)
                user_recipes = checkout_user.recipe_posts.all()
                code_list = []
                recipe_list = []
                if user_recipes:
                    for recipe in user_recipes:
                        if recipe.discount_code != "":
                            code = recipe.discount_code
                            code_list.append(code)
                            recipe_list.append(recipe)
                    # first_discount_code = code_list[0]
                    # first_recipe = recipe_list[0]
                    if recipe_list:
                        first_recipe = recipe_list[0]
                        # the_discount = request.POST.get('discount')
                        # print(the_discount)
                        # order.vote_discount_applied = discount or 0
                        # discount = current_bag['discount']
                        # print(discount)
                        """grand_total = current_bag['grand_total']
                        total = grand_total - discount
                        stripe_total = round(total * 100)
                        stripe.api_key = stripe_secret_key
                        intent = stripe.PaymentIntent.create(
                            amount=stripe_total,
                            currency=settings.STRIPE_CURRENCY,
                        )"""
                        # print(total)
                    # should be in checkout_success, the next 2 lines
                    # first_recipe.discount_code = ""
                    # first_recipe.save()
                """if user_recipes:
                    for recipe in user_recipes:
                        if recipe.discount_code != "":
                            code = recipe.discount_code
                            code_list.append(code)
                            first_discount_code = code_list[0]"""
                    # recipe_with_discount_code = Recipe.objects.get(discount_code=first_discount_code)
                    # recipe_with_discount_code.discount_code = ""
                    # recipe_with_discount_code.save()

            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'user_recipes': user_recipes,
        # 'vote_threshold_precentage': vote_threshold_precentage,
        'first_discount_code': first_discount_code,
        'checkout_user': checkout_user,
        'recipe_with_discount_code': recipe_with_discount_code,
        'first_recipe': first_recipe,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    posts = Post.objects.all().order_by('-pk')
    recipes = Recipe.objects.all().order_by('-pk')

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Get code for discount from recipe with votes
        checkout_user = get_object_or_404(User, id=request.user.id)
        user_recipes = checkout_user.recipe_posts.all()
        code_list = []
        recipe_list = []
        if user_recipes:
            for recipe in user_recipes:
                if recipe.discount_code != "":
                    code = recipe.discount_code
                    code_list.append(code)
                    recipe_list.append(recipe)
            if recipe_list:
                first_recipe = recipe_list[0]
                first_recipe.discount_code = ""
                first_recipe.save()

    if save_info:
        profile_data = {
            'default_full_name': order.full_name,
            'default_phone_number': order.phone_number,
            'default_country': order.country,
            'default_postcode': order.postcode,
            'default_town_or_city': order.town_or_city,
            'default_street_address1': order.street_address1,
            'default_street_address2': order.street_address2,
            'default_county': order.county,
        }
        user_profile_form = UserProfileForm(profile_data, instance=profile)
        if user_profile_form.is_valid():
            user_profile_form.save()

    messages.success(request, f'Order succesfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'posts': posts,
        'recipes': recipes,
    }

    return render(request, template, context)
