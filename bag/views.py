from django.shortcuts import render, redirect


def view_bag(request):
    """ A view to return the shopping bag contents page """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    gf_option = None
    if 'gluten_free_option' in request.POST:
        gf_option = request.POST['gluten_free_option']
    bag = request.session.get('bag', {})

    if gf_option:
        if item_id in list(bag.keys()):
            if gf_option in bag[item_id]['option'].keys():
                bag[item_id]['option'][gf_option] += quantity
            else:
                bag[item_id]['option'][gf_option] = quantity
        else:
            bag[item_id] = {'option': {gf_option: quantity}}
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    request.session['bag'] = bag

    return redirect(redirect_url)
