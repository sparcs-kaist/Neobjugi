from django.db import models


class Account(models.Model):
    fbid = models.CharField(max_length=100)
    context = models.CharField(max_length=100)
    status = models.IntegerField(default = -1)
