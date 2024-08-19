from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, StoreRequest 
from django.contrib.auth.models import User
from .forms import UserForm
from .models import Product, StoreRequest
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from .models import StoreRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from seller_app.models import Store

User = get_user_model()

def admin_dashboard(request):
    total_products = Product.objects.count()
    pending_store_requests = StoreRequest.objects.filter(is_approved=False).count()
    total_users = User.objects.count()
    total_sellers = User.objects.filter(groups__name='Sellers').count()  # Assuming sellers are grouped

    context = {
        'total_products': total_products,
        'pending_store_requests': pending_store_requests,
        'total_users': total_users,
        'total_sellers': total_sellers,
    }
    return render(request, 'admin_dashboard.html', context)


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'user_form.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

@login_required
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if request.user == user:
            messages.error(request, 'You cannot delete your own account.')
            return redirect('user_list')
        user.delete()
        messages.success(request, 'User has been deleted successfully.')
        return redirect('user_list')
    return render(request, 'confirm_delete_user.html', {'user': user})




@login_required
def store_requests(request):
    requests = StoreRequest.objects.filter(is_approved=False)
    # print(requests)
    return render(request, 'store_requests.html', {'requests': requests})

@login_required
def approve_store_request(request, pk):
    store_request = get_object_or_404(StoreRequest, pk=pk)
    if request.method == 'POST':
        store_request.is_approved = True
        store_request.save()

        Store.objects.create(
            seller=store_request.seller,
            store_name=store_request.store_name,
            is_approved=True
        )

        messages.success(request, 'Store request approved successfully.')
        return redirect('store_requests')
    return render(request, 'approve_store_request.html', {'store_request': store_request})
