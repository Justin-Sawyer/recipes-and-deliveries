from django.shortcuts import render


def index(request):
    """ A view to return the index page """
    return render(request, 'home/index.html')


def guarantee(request):
    """ A view to return the R&D guarantee page """
    return render(request, 'home/guarantee.html')


"""
def all_blog_articles(request):
    "" A view to return the blog intro page ""
    return render(request, 'home/blog-home.html')
"""
