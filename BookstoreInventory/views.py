from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import UserLogin, UserRegister, EditBook
from django.db import IntegrityError
from BookstoreInventory.models import User, Transaction, Book, Author




#NOT A VIEW FUNCTION#
# Used to obtain user data via user.id
def load_user_data(session) -> dict:
    user_id = session.get('user_id', None)
    print(user_id)
    return {
        'user': User.objects.get(id=user_id) if user_id is not None else None
    }
#####################

# Create your views here.
def user_register(request):
    if request.method == 'POST': # If user has sent registration data
        form = UserRegister(request.POST)
        if form.is_valid():
            try:
                form.save(commit=True)
                return redirect(reverse('user_login'), just_registered=True) # Redirect user to login page
            except IntegrityError:
                form.add_error('email', 'An account with this email already exists!')
    
    # Else, give user the registration form
    else:
        form = UserRegister()

    return render(request, 'authentication/register.html', context={'form': form})

def user_login(request, just_registered=False):
    if just_registered:
        print("User just registered!")
    error = "" # Error msg

    if request.method == 'POST': # If user has sent login data
        form = UserLogin(request.POST)
        if form.is_valid():
            # Obtain login credentials from form
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Attempt to authenticate the user by given email and password
            user = authenticate(request, email=email, password=password)
            if user:
                
                # User credentials was correct
                # Assign user type by email whitelist or ...

                # Login the user
                auth_login(request, user)

                # Caching is not working properly
                request.session['user_id'] = user.id # Explicitly set user_id to session


                return redirect(reverse('dashboard')) # Redirect user to the home page
        
        error = "Incorrect email or password"


    # Else, give user the login form
    else:
        form = UserLogin()

    return render(request, 'authentication/login.html', context={'form': form, 'error': error, 'just_registered': just_registered})


def user_logout(request):
    request.session['user_id'] = None

    return redirect(reverse('dashboard'))

# @login_required
def dashboard(request):
    context = {
        'currentpage': "Dashboard",
        'statistics': [],
    }
    context.update(load_user_data(request.session)) # Add user data variables to context

    add_statistic = lambda label, value: context['statistics'].append({'label': label, 'value': value}) # Function to add statistics to context

    add_statistic('Orders today', 93)
    add_statistic('New books', 14)

    context['top_selling'] = [f'Book{i}' for i in range(10)]

    return render(request, 'bookstore/dashboard.html', context=context)

# @login_required
def inventory(request):
    context = {
        'currentpage': "Inventory",
        'books': []
    }
    context.update(load_user_data(request.session)) # Add user data variables to context

    return render(request, 'bookstore/inventory.html', context=context)

# @login_required
def shipments(request):
    context = {
        'currentpage': "Shipments",
        'shipments': []
    }
    context.update(load_user_data(request.session)) # Add user data variables to context

    return render(request, 'bookstore/shipments.html', context=context)

# @login_required
def transactions(request):
    context = {
        'currentpage': "Transactions",
        'transactions': [transaction for transaction in Transaction.objects.all()]
    }
    context.update(load_user_data(request.session)) # Add user data variables to context

    return render(request, 'bookstore/transactions.html', context=context)

# @login_required
def settings(request):
    context = {
        'currentpage': "Settings",
        'settings': []
    }
    context.update(load_user_data(request.session)) # Add user data variables to context

    return render(request, 'bookstore/settings.html', context=context)

# @login_required
def accountDetails(request):
    context = {
        'currentpage': "Account Details",
        'settings': []
    }
    context.update(load_user_data(request.session)) # Add user data variables to context

    return render(request, 'bookstore/accountDetails.html', context=context)