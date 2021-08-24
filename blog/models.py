from django.db import models
from django.contrib.auth.models import User
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
        self.friendly_name = self.friendly_name.capitalize()
        return self.friendly_name

    def save(self):
        # Credit: https://stackoverflow.com/a/31094863/14773450
        # set name to be friendly name
        self.name = self.friendly_name
        super().save(self)


class Tag(models.Model):

    class Meta:
        verbose_name_plural = 'Tags'
        ordering = ('tagname',)

    tagname = models.CharField(max_length=254)

    def __str__(self):
        self.tagname = self.tagname.capitalize()
        return self.tagname


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts')
    title = models.CharField(max_length=254)
    category = models.ManyToManyField('Category', blank=True)
    tag = models.ManyToManyField('Tag', blank=True)
    tagline = models.CharField(max_length=254)
    image = models.ImageField(null=True, blank=True)
    image_credit = models.CharField(max_length=254, default="", blank=True)
    content = RichTextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    date_posted = models.DateTimeField(null=True,
                                       blank=True,
                                       default=timezone.now)
    date_edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments',
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=250, default="")
    body = models.TextField(default="")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)
