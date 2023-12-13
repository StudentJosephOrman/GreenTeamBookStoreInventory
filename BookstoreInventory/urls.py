from django.urls import path
from . import views, apis

urlpatterns = [
    path('register', views.user_register, name='user_register'),
    path('login', views.user_login, name='user_login'),
    path('logout', views.user_logout, name='user_logout'),

    path('', views.dashboard, name='dashboard'),
    path('accountDetails', views.accountDetails, name='accountDetails'),
    path('settings', views.settings, name='settings'),
    path('inventory', views.inventory, name='inventory'),
    path('inventory/search/<str:query>', views.inventory_search, name='inventory_search'),
    path('inventory/edit/<int:book_isbn>', views.inventory_edit, name='inventory_edit'),
    path('transactions', views.transactions, name='transactions'),
    path('shipments', views.shipments, name='shipments'),


    # APIS
    path('books', apis.books, name='books'), # Viewing books
    path('api/books/<int:isbn>', apis.get_book, name='get_book'), # Get data of a book

    # path('inventory')
    #...
]
