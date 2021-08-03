from django.db import models


class Recipe(models.Model):
    title = models.CharField(max_length=150)
    intro = models.CharField(max_length=254)
    prep_time = models.DurationField()
    cook_time = models.DurationField()
    servings = models.IntegerField()

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    quantity = models.FloatField()
    unit = models.CharField(max_length=15)
    name = models.CharField(max_length=150)
    preparation = models.CharField(max_length=150, default="", blank=True)

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')

    def __str(self):
        return self.name

