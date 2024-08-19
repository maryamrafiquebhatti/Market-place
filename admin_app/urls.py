from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/edit/', views.user_update, name='user_update'),
    path('users/delete/<int:pk>/', views.delete_user, name='delete_user'),
    path('store_requests/<int:pk>/approve/', views.approve_store_request, name='approve_store_request'),
    path('store_requests/', views.store_requests, name='store_requests'),

]
