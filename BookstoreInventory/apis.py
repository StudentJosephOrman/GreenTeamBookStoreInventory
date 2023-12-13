from django.shortcuts import render
from django.http import JsonResponse
from .forms import EditBook
from django.db import IntegrityError
from BookstoreInventory.models import Book, Author, Publisher


def books(request):
    pass

def get_book(request, isbn:int):
    try:
        book = Book.objects.get(isbn=isbn)
        return JsonResponse(
            {
                'isbn': book.isbn,
                'author_ids': ';'.join([author.id for author in book.authors]),
                'publisher_id': book.publisher.id,
                'summary': book.summary,
                'genre': book.genre,
                'title': book.title,
                'cost':book.cost
            }
        )
    except:
        pass

def edit_book(request, isbn:int):
    # Query book
    book = Book.objects.get(isbn=isbn)

    if request.method == 'POST':
        # Set book data to that from form
        form = EditBook(request)
        if form.is_valid():
            book.isbn = form.cleaned_data['isbn']

            author_ids = form.cleaned_data['author_ids'].split(';')
            book.authors.set(
                [Author.objects.get(id=int(id)) for id in author_ids]
            )

            book.publisher= Publisher.objects.get(id=int(form.cleaned_data['publisher_id']))
            book.summary=form.cleaned_data['summary']
            book.quantity=form.cleaned_data['quantity']
            book.cost=form.cleaned_data['cost']
    else:
        # Create a new form with book details already filled in
        form = EditBook()
        form.isbn = book.isbn
        form.author_ids = ';'.join([str(author.id) for author in book.authors.all()])
        form.publisher_id = book.publisher.id
        form.summary = book.summary
        form.genre = book.genre
        form.title = book.title
        form.cost = book.cost
    
    return render(request, 'bookstore/edit_book.html', context={'form': form, 'book_isbn': isbn})

def search_books(request, query:int):
    print("Got", query)
    book_objs = []
    for book in Book.objects.all():
        book_objs.append({
            'isbn': book.isbn,
            'title': book.title,
            'genre': book.genre,
            'summary': book.summary,
            'author_ids': ';'.join([str(author.id) for author in book.authors.all()]),
            'publisher_id': book.publisher.id if book.publisher else '',
            'quantity': book.quantity,
            'cost': book.cost
        })

    return JsonResponse({
        'books': book_objs
    })