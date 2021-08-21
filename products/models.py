from django.db import models
# from django.contrib.auth.models import User
# from django.utils import timezone

from ckeditor.fields import RichTextField


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


class Product(models.Model):
    name = models.CharField(max_length=254)
    sku = models.CharField(max_length=254, null=False, blank=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True,
                                 blank=True)
    has_gluten = models.BooleanField(default=False, null=True, blank=True)
    gluten_free_option = models.BooleanField(default=False, null=True,
                                             blank=True)
    category = models.ManyToManyField('Category')
    description = RichTextField(blank=True, null=True)
    image_url = models.URLField(max_length=1024, default="", blank=True)
    image_credit = models.CharField(max_length=254, default="", blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments',
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=250, default="")
    body = models.TextField(default="")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.product.name, self.name)
