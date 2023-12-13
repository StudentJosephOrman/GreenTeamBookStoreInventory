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