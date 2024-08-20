# ecommerce/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', include('admin_app.urls')),  
    path('buyer/', include('buyer_app.urls')),  
    path('', include('core.urls',namespace='core')),  
    path('seller/', include('seller_app.urls' ,namespace='seller_app')),  

]
