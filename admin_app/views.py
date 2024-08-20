# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.models import User
# from .forms import UserForm
# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from seller_app.models import Store , Product

# User = get_user_model()

# def admin_dashboard(request):
#     total_products = Product.objects.count()
#     pending_store_requests = Store.objects.filter(is_approved=False).count()
#     total_users = User.objects.count()
#     total_sellers = User.objects.filter(groups__name='Sellers').count()  

#     context = {
#         'total_products': total_products,
#         'pending_store_requests': pending_store_requests,
#         'total_users': total_users,
#         'total_sellers': total_sellers,
#     }
#     return render(request, 'admin_dashboard.html', context)


# def product_list(request):
#     products = Product.objects.all()
#     return render(request, 'product_list.html', {'products': products})


# def user_list(request):
#     users = User.objects.all()
#     return render(request, 'user_list.html', {'users': users})

# def user_update(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     if request.method == 'POST':
#         form = UserForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('user_list')
#     else:
#         form = UserForm(instance=user)
#     return render(request, 'user_form.html', {'form': form})

# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
# from django.contrib.auth import get_user_model
# from django.contrib.auth.decorators import login_required

# @login_required
# def delete_user(request, pk):
#     user = get_object_or_404(User, pk=pk)
#     if request.method == 'POST':
#         if request.user == user:
#             messages.error(request, 'You cannot delete your own account.')
#             return redirect('user_list')
#         user.delete()
#         messages.success(request, 'User has been deleted successfully.')
#         return redirect('user_list')
#     return render(request, 'confirm_delete_user.html', {'user': user})




# # @login_required
# # def store_requests(request):
# #     requests = StoreRequest.objects.filter(is_approved=False)
# #     # print(requests)
# #     return render(request, 'store_requests.html', {'requests': requests})

# # @login_required
# # def approve_store_request(request, pk):
# #     store_request = get_object_or_404(StoreRequest, pk=pk)
# #     if request.method == 'POST':
# #         store_request.is_approved = True
# #         store_request.save()

# #         Store.objects.create(
# #             seller=store_request.seller,
# #             store_name=store_request.store_name,
# #             is_approved=True
# #         )

# #         messages.success(request, 'Store request approved successfully.')
# #         return redirect('store_requests')
# #     return render(request, 'approve_store_request.html', {'store_request': store_request})



# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import user_passes_test
# from seller_app.models import Store

# @user_passes_test(lambda u: u.is_staff)
# def store_approval_list(request):
#     stores = Store.objects.filter(is_approved=False)
#     return render(request, 'store_approval_list.html', {'stores': stores})

# @user_passes_test(lambda u: u.is_staff)
# def approve_store(request, store_id):
#     store = get_object_or_404(Store, id=store_id)
#     if request.method == 'POST':
#         store.is_approved = True
#         store.save()
#         return redirect('admin:store_approval_list')
#     return render(request, 'approve_store.html', {'store': store})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from seller_app.models import Store, Product
from django.contrib.auth.decorators import user_passes_test
from .forms import UserForm

User = get_user_model()

def admin_dashboard(request):
    total_products = Product.objects.count()
    pending_store_requests = Store.objects.filter(is_approved=False).count()
    total_users = User.objects.count()
    total_sellers = User.objects.filter(groups__name='Sellers').count()

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

@login_required
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if request.user == user:
            messages.error(request, 'You cannot delete your own account.')
            return redirect('user_list')
        user.delete()
        messages.success(request, 'User has been deleted successfully.')
        return redirect('admin_app:user_list')
    return render(request, 'confirm_delete_user.html', {'user': user})

# @user_passes_test(lambda u: u.is_staff)
# def store_approval_list(request):
#     stores = Store.objects.filter(is_approved=False)
#     return render(request, 'store_approval_list.html', {'stores': stores})

# @user_passes_test(lambda u: u.is_staff)
# def approve_store(request, store_id):
#     store = get_object_or_404(Store, id=store_id)
#     if request.method == 'POST':
#         store.is_approved = True
#         store.save()
#         return redirect('admin_app:store_approval_list')
#     return render(request, 'approve_store.html', {'store': store})
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth import get_user_model
# from django.contrib.auth.decorators import user_passes_test
# from seller_app.models import Store
# from django.contrib import messages

# User = get_user_model()

# @user_passes_test(lambda u: u.is_staff)
# def store_approval_list(request):
#     stores = Store.objects.filter(is_approved=False)
#     return render(request, 'store_approval_list.html', {'stores': stores})

# @user_passes_test(lambda u: u.is_staff)
# def approve_store(request, store_id):
#     store = get_object_or_404(Store, id=store_id)
#     if request.method == 'POST':
#         store.is_approved = True
#         store.save()

#         # Redirect the seller to their dashboard
#         seller = store.user  # Use the `user` field if that's how you identify the seller
#         messages.success(request, 'Store request approved successfully.')
#         return redirect('seller_app:dashboard')  # Redirect to the seller's dashboard

#     return render(request, 'approve_store.html', {'store': store})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from seller_app.models import Store
from django.contrib.auth import get_user_model

User = get_user_model()

@user_passes_test(lambda u: u.is_staff)
def store_approval_list(request):
    stores = Store.objects.filter(is_approved=False)
    return render(request, 'store_approval_list.html', {'stores': stores})

@user_passes_test(lambda u: u.is_staff)
def approve_store(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    if request.method == 'POST':
        store.is_approved = True
        store.save()
        
        # Redirect the seller to their dashboard
        seller = store.user  # Assuming the store has a foreign key to the user
        messages.success(request, 'Store request approved successfully.')

        # Redirect admin to the admin dashboard
        return redirect('admin_app:admin_dashboard')  # Adjust this to your actual admin dashboard URL

    return render(request, 'approve_store.html', {'store': store})
