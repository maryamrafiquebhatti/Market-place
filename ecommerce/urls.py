# ecommerce/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', include('admin_app.urls')),  # Admin app URLs
    path('seller/', include('seller_app.urls')),  # Seller app URLs
    path('buyer/', include('buyer_app.urls')),  # Buyer app URLs
    path('', include('core.urls')),  # Core app URLs
]
