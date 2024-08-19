from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.mail import send_mail
from django.db import IntegrityError
from django.contrib.sites.shortcuts import get_current_site

from .forms import SellerSignupForm
from .tokens import account_activation_token

# Home view
def home(request):
    return render(request, 'home.html')

# Admin login view
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid credentials or not an admin'})
    return render(request, 'admin_login.html')

# Admin signup view
def admin_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username=username, password=password)
            user.is_staff = True  # Mark user as admin
            user.save()
            return redirect('admin_login')
        except IntegrityError:
            # This error will occur if the username already exists
            return render(request, 'admin_signup.html', {
                'error': 'Username already exists. Please choose a different username.'
            })
    return render(request, 'admin_signup.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .tokens import account_activation_token
from .forms import SellerSignupForm
from .models import User

def seller_signup(request):
    if request.method == 'POST':
        form = SellerSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Send activation email
            current_site = get_current_site(request)
            mail_subject = 'Activate your seller account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'protocol': request.is_secure() and "https" or "http",
                'activate_url': reverse('core:activate_account', kwargs={
                    'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user)
                }),
            })
            try:
                send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            except Exception as e:
                user.delete()
                messages.error(request, 'There was an error sending the activation email. Please try again.')
                return redirect('core:seller_signup')

            return redirect('core:account_activation_sent')
    else:
        form = SellerSignupForm()
    return render(request, 'seller_signup.html', {'form': form})

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('seller_profile')
    else:
        return render(request, 'account_activation_invalid.html')

def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')

def account_activation_invalid(request):
    return render(request, 'account_activation_invalid.html')

def seller_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_authenticated:
                login(request, user)
                messages.success(request, 'You are now logged in as a seller.')
                return redirect('seller_profile')
            else:
                messages.error(request, 'Invalid credentials.')
    else:
        form = AuthenticationForm(request)
    return render(request, 'seller_login.html', {'form': form})






from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

def buyer_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  
            return redirect('core:buyer_profile')
    else:
        form = UserCreationForm()
    return render(request, 'buyer_signup.html', {'form': form})

def buyer_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('core:buyer_profile')
    else:
        form = AuthenticationForm()
    return render(request, 'buyer_login.html', {'form': form})

def buyer_logout(request):
    auth_logout(request)
    return redirect('core:buyer_login')

@login_required
def buyer_profile(request):
    return render(request, 'buyer_profile.html')
