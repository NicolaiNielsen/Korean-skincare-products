from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    buy_link = models.CharField(max_length=2083)
    image_url = models.CharField(max_length=2083)
    ranking = models.IntegerField()


