from django.db import models


class Contact(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255, default="",
                            null=False, blank=False)
    subject = models.CharField(max_length=255, default="",
                               null=False, blank=False)
    message = models.TextField()

    def __str__(self):
        return self.email

