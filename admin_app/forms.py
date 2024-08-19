from django import forms
from .models import Product, StoreRequest
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock']

class StoreRequestForm(forms.ModelForm):
    class Meta:
        model = StoreRequest
        fields = ['store_name', 'description']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff', 'is_active']
