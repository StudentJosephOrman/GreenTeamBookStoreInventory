from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import Http404, JsonResponse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import UserLogin, UserRegister, EditBook
from django.db import IntegrityError
from BookstoreInventory.models import User, Transaction, Book, Author, Publisher




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

        # Needed for inventory searches
        'books': [],
        'query': '',
        #############
    }
    context.update(load_user_data(request.session)) # Add user data variables to context

    return render(request, 'bookstore/inventory.html', context=context)

def inventory_search(request, query:str):
    context = {
        'currentpage': "Inventory",
        'books': [],
        'query': query
    }
    context.update(load_user_data(request.session))


    # Query all books matching specified filters
    filters = ['isbn', 'title', 'genre']

    for book in Book.objects.all():
        match = False
        for filter in filters:
            if match: break # End comparisons if match was already found
            
            if query in str(getattr(book, filter)):
                match = True

        if match:
            context['books'].append(book)

    return render(request, 'bookstore/inventory.html', context=context)

    

def manage_book(request, book_isbn:int):
    context = {
        'currentpage': f"Inventory -> Manage book (isbn: {book_isbn})"
    }
    context.update(load_user_data(request.session))

    # Query book
    book = Book.objects.get(isbn = book_isbn)

    if request.method == 'POST':
        # Check if form is valid
        form = EditBook(request.POST)
        if form.is_valid():
            # Set book data to that from form
            book.isbn = form.cleaned_data['isbn']

            author_ids = form.cleaned_data['author_ids'].split(';')
            book.authors.set(
                [Author.objects.get(id=int(id)) for id in author_ids]
            )

            book.publisher= Publisher.objects.get(id=int(form.cleaned_data['publisher_id']))
            book.summary=form.cleaned_data['summary']
            book.cost=form.cleaned_data['cost']

            book.save() # Save changes

            return redirect(reverse('inventory'))

    else:
        # Create a new form with book details already filled in
        form = EditBook(initial={
            'isbn': book.isbn,
            'title': book.title,
            'genre': book.genre,
            'summary': book.summary,
            'author_ids': ';'.join([str(author.id) for author in book.authors.all()]),
            'publisher_id': book.publisher.id,
            'cost': book.cost,
        })

    context['form'] = form
    context['book'] = book
    
    return render(request, 'bookstore/manage_book.html', context=context)


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
def accountBase(request):
    context = {
        'currentpage': "Account Details",
        'settings': []
    }
    context.update(load_user_data(request.session)) # Add user data variables to context

    return render(request, 'bookstore/accountBase.html', context=context)

def details(request):
    context = {
        'currentpage': "Account Details",
        'settings': []
    }
    context.update(load_user_data(request.session)) # Add user data variables to context

    return render(request, 'bookstore/details.html', context=context)
 
def settings(request):
    context = {
        'currentpage': "Settings",
        'settings': []
    }
    context.update(load_user_data(request.session)) # Add user data variables to context

    return render(request, 'bookstore/settings.html', context=context) 