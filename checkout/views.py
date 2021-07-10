from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag yet")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51IvhlpI239UNMzSY9CVoqsfsTp1pW3hX2FGwUxr0cEd3HQxvMWasPGDBHY5Q8WsnOoduyEKFhNDXA66JtgxQOlsQ00f2yCIft4',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
