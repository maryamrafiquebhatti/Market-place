from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Store(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stores')
    store_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.store_name



class Product(models.Model):
    name = models.CharField(max_length=255)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.IntegerField()

    def __str__(self):
        return self.name