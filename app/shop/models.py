from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=100, default='')
    img_cnt = models.IntegerField(default=0)
    price = models.PositiveIntegerField()
    accessories = models.BooleanField(default=False)
