# from django.db import models
# from django.conf import settings
# from django.utils import timezone

# class Store(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , default= 'seller')
#     name = models.CharField(max_length=255)
#     description = models.TextField(default='default')
#     is_approved = models.BooleanField(default=False)
#     created_at = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return self.name

# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     description = models.TextField()
#     stock = models.IntegerField()  

#     def __str__(self):
#         return self.name




from django.db import models
from django.conf import settings
from django.utils import timezone

class Store(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(default='default')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.IntegerField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE, default=1)  # Example default, adjust as needed

    def __str__(self):
        return self.name
