from django.shortcuts import render
from django.http import JsonResponse
from .forms import EditBook
from django.db import IntegrityError
from BookstoreInventory.models import Book, Author, Publisher

# This python script is a built-in DJango script, but allows us to create our own python scripts and apis.


def books(request):
    pass

def get_book(request, isbn:int):
    try:
        book = Book.objects.get(isbn=isbn)

        author_names = []
        for author in book.authors.all():
            author_names.append(f"{author.first_name} {author.middle_name} {author.last_name}")

        return JsonResponse(
            {
                'isbn': book.isbn,
                'authors': author_names,
                'publisher': book.publisher.name,
                'summary': book.summary,
                'genre': book.genre,
                'title': book.title,
                'quantity': book.quantity,
                'cost': book.cost
            }
        )
    except:
        pass
def change_book_stock(request, isbn:int, value:int):
    response = {
        'msg': 'fail'
    }

    try:
        book = Book.objects.get(isbn=isbn)
        
        if(value > 0):
            book.quantity = value
            book.save()
        
    except: pass
