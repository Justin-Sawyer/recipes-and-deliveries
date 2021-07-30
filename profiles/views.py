from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserProfileForm

from blog.models import Post

from checkout.models import Order


@login_required
def profile(request):
    """ Display the user's profile """

    profile = get_object_or_404(UserProfile, user=request.user)
    user = get_object_or_404(User, id=request.user.id)
    # posts = Post.objects.all()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile successfully updated!')
        else:
            messages.error(request, 'Update failed. Please ensure \
                the form is valid.')

    # Populate the form with the user's profile info
    else:
        form = UserProfileForm(instance=profile)
    orders = profile.orders.all().order_by('-pk')
    user_posts = user.blog_posts.all().order_by('-pk')
    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
        # 'posts': posts,
        'user_posts': user_posts,
    }

    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    posts = Post.objects.all().order_by('-pk')

    messages.warning(request, (
        f'This is a past confirmation for order number {order_number}.'
        'A confirmation email was sent on the order date.'
    ))
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'posts': posts,
        'from_profile': True,
    }

    return render(request, template, context)
