from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import StoreRequest, Product
from .forms import ProductForm

# seller_app/views.py
from django.shortcuts import render, redirect
from .forms import StoreRequestForm
from seller_app.models import Store
from django.contrib.auth.decorators import login_required


# @login_required
# def request_store(request):
#     # Check if the user has pending requests
#     if StoreRequest.objects.filter(seller=request.user, is_approved=False).exists():
#         return render(request, 'store_request_pending.html')

#     if request.method == 'POST':
#         form = StoreRequestForm(request.POST)
#         if form.is_valid():
#             store_request = form.save(commit=False)
#             store_request.seller = request.user
#             store_request.save()
#             return redirect('store_request_success')
#     else:
#         form = StoreRequestForm()

#     return render(request, 'request_store.html', {'form': form})





from django.shortcuts import render, redirect
from .forms import StoreRequestForm
from .models import StoreRequest
from django.contrib.auth.decorators import login_required

@login_required
def request_store(request):
    if StoreRequest.objects.filter(seller=request.user, is_approved=False).exists():
        return render(request, 'store_request_pending.html')

    if request.method == 'POST':
        form = StoreRequestForm(request.POST)
        if form.is_valid():
            store_request = form.save(commit=False)
            store_request.seller = request.user
            store_request.save()
            return redirect('store_request_success')
    else:
        form = StoreRequestForm()

    return render(request, 'request_store.html', {'form': form})

@login_required
def store_request_success(request):
    return render(request, 'store_request_success.html')









@login_required
def manage_store(request):
    store = Store.objects.filter(seller=request.user).first()
    if not store:
        return redirect('store_request')
    
    products = Product.objects.filter(store=store)
    return render(request, 'manage_store.html', {'products': products, 'store': store})

@login_required
def add_product(request):
    store = get_object_or_404(Store, seller=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            return redirect('manage_store')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

# @login_required
# def seller_profile(request):
#     store = Store.objects.filter(seller=request.user, is_approved=True).first()
#     if not store:
#         store_request = StoreRequest.objects.filter(seller=request.user, is_approved=False).first()
#         if store_request:
#             return render(request, 'store_request_pending.html')
#         else:
#             return redirect('request_store')

#     products = Product.objects.filter(store=store)
#     total_stock = sum(product.stock for product in products)
#     return render(request, 'seller_profile.html', {'total_stock': total_stock, 'store': store})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import StoreRequest, Store, Product

@login_required
def seller_profile(request):
    # Check if the seller has an approved store
    store = Store.objects.filter(seller=request.user, is_approved=True).first()
    
    if store:
        # Store is approved, display seller profile with store details
        products = Product.objects.filter(store=store)
        total_stock = sum(product.stock for product in products)
        return render(request, 'seller_profile.html', {
            'total_stock': total_stock,
            'store': store,
            'products': products,
        })
    else:
        # Check if there is a pending store request
        store_request = StoreRequest.objects.filter(seller=request.user, is_approved=False).first()
        if store_request:
            return render(request, 'store_request_pending.html', {'store_request': store_request})
        else:
            return redirect('request_store')  # Redirect to store request form if no request is made yet









@login_required
def manage_products(request):
    store = get_object_or_404(Store, seller=request.user)
    products = Product.objects.filter(store=store)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            return redirect('seller_app:manage_products')
    else:
        form = ProductForm()

    context = {
        'products': products,
        'form': form,
    }
    return render(request, 'manage_products.html', context)

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, store__seller=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('seller_app:manage_products')
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'edit_product.html', context)

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, store__seller=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('seller_app:manage_products')

    context = {
        'product': product,
    }
    return render(request, 'delete_product.html', context)
