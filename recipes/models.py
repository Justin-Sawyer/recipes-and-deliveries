from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipe_posts', default="", blank=True, null=True)
    title = models.CharField(max_length=150)
    intro = models.CharField(max_length=254)
    prep_time = models.CharField(max_length=20)
    cook_time = models.CharField(max_length=20, default="", blank=True)
    total_time = models.CharField(max_length=20, null=True, blank=False)
    servings = models.IntegerField()
    directions = models.TextField(default="", blank=False)
    image = models.ImageField(null=True, blank=True)
    image_credit = models.CharField(max_length=254, default="", blank=True)
    date = models.DateTimeField(auto_now_add=True)
    date_posted = models.DateTimeField(null=True,
                                       blank=True,
                                       default=timezone.now)
    date_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    quantity = models.FloatField()
    unit = models.CharField(max_length=15)
    name = models.CharField(max_length=150)
    preparation = models.CharField(max_length=150, default="", blank=True)

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='ingredients')

    def __str(self):
        return self.name

