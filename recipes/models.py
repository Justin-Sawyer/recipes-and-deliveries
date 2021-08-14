from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

from products.models import Product

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


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipe_posts',
                               default="",
                               blank=True,
                               null=True)
    title = models.CharField(max_length=150)
    intro = models.CharField(max_length=254)
    prep_time = models.CharField(max_length=20)
    cook_time = models.CharField(max_length=20, default="", blank=True)
    total_time = models.CharField(max_length=20, null=True, blank=False)
    servings = models.IntegerField()
    category = models.ManyToManyField('Category', blank=True)
    tag = models.ManyToManyField('Tag', blank=True)
    # directions = models.TextField(default="", blank=False)
    directions = RichTextField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    image_credit = models.CharField(max_length=254, default="", blank=True)
    date = models.DateTimeField(auto_now_add=True)
    date_posted = models.DateTimeField(null=True,
                                       blank=True,
                                       default=timezone.now)
    date_edited = models.DateTimeField(auto_now=True)
    recipe_box = models.OneToOneField(Product, related_name='box',
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      blank=True)
    vote_count = models.IntegerField(default=0)
    votes = models.ManyToManyField(User,
                                   related_name='recipe_post_votes',
                                   blank=True)

    def total_votes(self):
        return self.votes.count()

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    quantity = models.FloatField(default="", blank=True)
    unit = models.CharField(max_length=15, default="", blank=True)
    name = models.CharField(max_length=150, default="", blank=True)
    preparation = models.CharField(max_length=150, default="", blank=True)

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='ingredients')

    def __str(self):
        return self.name
    
    # If quantity is whole number, remove the decimal places
    # Credit: https://stackoverflow.com/a/4566018/14773450
    def get_quantity(self):
        if self.quantity == int(self.quantity):
            self.quantity = int(self.quantity)
        return self.quantity

