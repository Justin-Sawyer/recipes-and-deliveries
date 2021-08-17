from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404

from products.models import Product
from recipes.models import Recipe
from django.contrib.auth.models import User



def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    discount = 0
    # grand_total = 0
    user_recipes = 0
    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():
        # Just getting quantity, no gf_option
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            product = get_object_or_404(Product, pk=item_id)
            for gf_option, quantity in item_data['diet_requirements'].items():
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'gf_option': gf_option
                })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    grand_total = total + delivery

    if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        user_recipes = user.recipe_posts.all()
        if user_recipes:
            for recipe in user_recipes:
                if recipe.discount_code != "":
                    discount = total * Decimal(settings.VOTE_THRESHOLD_PERCENTAGE / 100) or 0
            grand_total = total + delivery - discount
        else:
            grand_total = total + delivery

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'vote_threshold_precentage': settings.VOTE_THRESHOLD_PERCENTAGE,
        'grand_total': grand_total,
        'discount': discount,
        'user_recipes': user_recipes,
    }

    return context
