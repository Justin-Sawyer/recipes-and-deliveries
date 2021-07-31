from django.db import models
from django.contrib.auth.models import User
# from products.models import Category
from datetime import datetime
from django.utils import timezone


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, default="", blank=True)
    sku = models.CharField(max_length=254, default="", blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Tag(models.Model):

    class Meta:
        verbose_name_plural = 'Tags'
        ordering = ('tagname',)

    tagname = models.CharField(max_length=254)

    def __str__(self):
        return self.tagname.capitalize()

    def get_friendly_name(self):
        return self.tagname


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=254)
    category = models.ManyToManyField('Category')
    tag = models.ManyToManyField('Tag')
    tagline = models.CharField(max_length=254)
    image = models.ImageField(null=True, blank=True)
    image_credit = models.CharField(max_length=254, default="", blank=False)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    date_posted = models.DateTimeField(null=True,
                                       blank=True,
                                       default=timezone.now)
    date_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
