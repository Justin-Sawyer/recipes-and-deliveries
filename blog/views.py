from django.shortcuts import render
# from django.http import HttpResponse


def all_blog_articles(request):
    """ A view to return the blog page """
    # template = 'blog/blog-articles.html'
    # context = {}
    return render(request, 'blog/blog-home.html')
