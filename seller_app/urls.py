
from django.urls import path
from . import views
app_name = 'seller_app'

urlpatterns = [

    path('manage_store/', views.manage_store, name='manage_store'),
    path('add_product/', views.add_product, name='add_product'),
    path('request_store/', views.request_store, name='request_store'),

    path('manage-products/', views.manage_products, name='manage_products'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('store_request_success/', views.store_request_success, name='store_request_success'),
]
    
    

