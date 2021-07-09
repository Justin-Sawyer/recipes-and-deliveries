from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages

from products.models import Product


def view_bag(request):
    """ A view to return the shopping bag contents page """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = Product.objects.get(pk=item_id)

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
            else:
                bag[item_id]['diet_requirements'][gf_option] = quantity
        else:
            bag[item_id] = {'diet_requirements': {gf_option: quantity}}
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag!')

    request.session['bag'] = bag

    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """
    Adjust the quantity of the specified product to the specified amount
    """

    quantity = int(request.POST.get('quantity'))
    gf_option = None
    if 'gluten_free_option' in request.POST:
        gf_option = request.POST['gluten_free_option']
    bag = request.session.get('bag', {})

    if gf_option:
        if quantity > 0:
            bag[item_id]['diet_requirements'][gf_option] = quantity
        else:
            del bag[item_id]['diet_requirements'][gf_option]
            if not bag[item_id]['diet_requirements']:
                bag.pop(item_id)
    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)

    request.session['bag'] = bag

    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ Remove the specified product from the bag """

    try:
        gf_option = None
        if 'gluten_free_option' in request.POST:
            gf_option = request.POST['gluten_free_option']
        bag = request.session.get('bag', {})

        if gf_option:
            del bag[item_id]['diet_requirements'][gf_option]
            if not bag[item_id]['diet_requirements']:
                bag.pop(item_id)
        else:
            bag.pop(item_id)

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)
