from django.db import models
from django.utils import timezone


class Contact(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255, default="",
                            null=False, blank=False)
    subject = models.CharField(max_length=255, default="",
                               null=False, blank=False)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

