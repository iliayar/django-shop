from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=20, default='Unknown')
    has_description = models.BooleanField(default=True)

class Product(models.Model):
    title = models.CharField(max_length=100, default='')
    img_cnt = models.IntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    specification = models.JSONField(default=dict)
    description = models.TextField(default='')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=None)
