from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Recipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    recipes_name = models.CharField(max_length=100)
    recipes_description = models.TextField()
    recipes_image = models.ImageField(upload_to="recipes")