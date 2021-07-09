from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product


def view_bag(request):
    """ A view to return the shopping bag contents page """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    gf_option = None
    if 'gluten_free_option' in request.POST:
        gf_option = request.POST['gluten_free_option']
    bag = request.session.get('bag', {})

    if gf_option:
        if item_id in list(bag.keys()):
            if gf_option in bag[item_id]['diet_requirements'].keys():
                bag[item_id]['diet_requirements'][gf_option] += quantity
                messages.success(request, f'''Updated {gf_option.upper()}
                                 {product.name} quantity to {bag[item_id][
                                     "diet_requirements"][gf_option]}''')
            else:
                bag[item_id]['diet_requirements'][gf_option] = quantity
                messages.success(request, f'''Added {gf_option.upper()}
                                 {product.name} to your bag''')
        else:
            bag[item_id] = {'diet_requirements': {gf_option: quantity}}
            messages.success(request, f'''Added {gf_option.upper()}
                             {product.name} to your bag''')
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'''Updated
                             {product.name} quantity to {bag[item_id]}''')
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag!')

    request.session['bag'] = bag

    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """
    Adjust the quantity of the specified product to the specified amount
    """
    product = get_object_or_404(Product, pk=item_id)

    quantity = int(request.POST.get('quantity'))
    gf_option = None
    if 'gluten_free_option' in request.POST:
        gf_option = request.POST['gluten_free_option']
    bag = request.session.get('bag', {})

    if gf_option:
        if quantity > 0:
            bag[item_id]['diet_requirements'][gf_option] = quantity
            messages.success(request, f'''Updated {gf_option.upper()}
                                 {product.name} quantity to {bag[item_id][
                                     "diet_requirements"][gf_option]}''')
        else:
            del bag[item_id]['diet_requirements'][gf_option]
            if not bag[item_id]['diet_requirements']:
                bag.pop(item_id)
            messages.success(request, f'''Removed {gf_option.upper()}
                                 {product.name} from your bag''')
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'''Updated 
                             {product.name} quantity to {bag[item_id]}''')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag

    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ Remove the specified product from the bag """

    try:
        product = get_object_or_404(Product, pk=item_id)
        gf_option = None
        if 'gluten_free_option' in request.POST:
            gf_option = request.POST['gluten_free_option']
        bag = request.session.get('bag', {})

        if gf_option:
            del bag[item_id]['diet_requirements'][gf_option]
            if not bag[item_id]['diet_requirements']:
                bag.pop(item_id)
            messages.success(request, f'''Removed {gf_option.upper()}
                                 {product.name} from your bag''')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
