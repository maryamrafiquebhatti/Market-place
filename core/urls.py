from django.urls import path
from .views import (
    home, admin_login, admin_signup, activate_account,
    account_activation_sent, seller_signup, account_activation_invalid,
    seller_login ,buyer_signup ,buyer_login,buyer_logout,buyer_profile
)

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),  
    path('admin/login/', admin_login, name='admin_login'),  
    path('admin/signup/', admin_signup, name='admin_signup'),  
    path('activate/<uidb64>/<token>/', activate_account, name='activate_account'), 
    path('activation/sent/', account_activation_sent, name='account_activation_sent'),
    path('signup/seller/', seller_signup, name='seller_signup'), 
    path('activation/invalid/', account_activation_invalid, name='account_activation_invalid'),
    path('seller/login/', seller_login, name='seller_login'), 
    path('buyer/signup/', buyer_signup, name='buyer_signup'),
    path('buyer/login/', buyer_login, name='buyer_login'),
    path('buyer/logout/',buyer_logout, name='buyer_logout'),
    path('buyer/profile/',buyer_profile, name='buyer_profile'),
]



