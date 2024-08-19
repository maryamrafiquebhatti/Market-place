from django import forms
from .models import  Product, StoreRequest
from seller_app.models import Store




class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock']


        
# seller_app/forms.py
from django import forms
from .models import StoreRequest

class StoreRequestForm(forms.ModelForm):
    class Meta:
        model = StoreRequest
        fields = ['store_name', 'description']
