from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login
from .forms import UserLogin, UserRegister
from django.db import IntegrityError
from BookstoreInventory.models import User




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


                return redirect(reverse('home')) # Redirect user to the home page
        
        error = "Incorrect email or password"


    # Else, give user the login form
    else:
        form = UserLogin()

    return render(request, 'authentication/login.html', context={'form': form, 'error': error, 'just_registered': just_registered})


def user_logout(request):
    request.session['user_id'] = None

    return redirect(reverse('home'))

def home(request):
    context = {}
    context.update(load_user_data(request.session)) # Add user data variables to context

    return render(request, 'bookstore/index.html', context=context)

def books(request):
    pass

def books(request, isbn:int):
    pass

def edit_book(request, isbn:int):
    pass

def search_books(request, query:str):
    pass