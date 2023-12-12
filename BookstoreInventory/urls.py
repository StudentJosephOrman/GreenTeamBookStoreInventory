from django.urls import path
from . import views

urlpatterns = [
    path('register', views.user_register, name='user_register'),
    path('login', views.user_login, name='user_login'),
    path('logout', views.user_logout, name='user_logout'),

    path('', views.dashboard, name='dashboard'),

    path('books', views.books, name='books'), # Viewing books
    path('books/<int:isbn>', views.books, name='book'), # View specific book
    path('books/<int:isbn>/edit', views.edit_book, name='edit_book'),
    path('search/<str:query>', views.search_books, name='search_book')

    # path('inventory')
    #...
]
