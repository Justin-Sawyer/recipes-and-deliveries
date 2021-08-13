from django.db import models
from django.contrib.auth.models import User
# from products.models import Category
from datetime import datetime
from django.utils import timezone

from ckeditor.fields import RichTextField


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('sku',)

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, default="", blank=True)
    sku = models.CharField(max_length=254, default="", blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name.title()


class Tag(models.Model):

    class Meta:
        verbose_name_plural = 'Tags'
        ordering = ('tagname',)

    tagname = models.CharField(max_length=254)

    def __str__(self):
        return self.tagname.capitalize()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts')
    title = models.CharField(max_length=254)
    category = models.ManyToManyField('Category', blank=True)
    tag = models.ManyToManyField('Tag', blank=True)
    tagline = models.CharField(max_length=254)
    image = models.ImageField(null=True, blank=True)
    image_credit = models.CharField(max_length=254, default="", blank=True)
    # content = models.TextField()
    content = RichTextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    date_posted = models.DateTimeField(null=True,
                                       blank=True,
                                       default=timezone.now)
    date_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="")
    body = models.TextField(default="")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)
