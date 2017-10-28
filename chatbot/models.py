from django.db import models

# Create your models here.

class User(models.Model):
	fid = models.CharField(max_length=20)
	cxt = models.CharField(max_length=100)

