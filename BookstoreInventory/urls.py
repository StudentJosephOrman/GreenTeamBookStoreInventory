from django.urls import path
from . import views, apis
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register', views.user_register, name='user_register'),
    path('login', views.user_login, name='user_login'),
    path('logout', views.user_logout, name='user_logout'),

    path('', views.dashboard, name='dashboard'),
    path('accountBase', views.accountBase, name='accountBase'),
    path('accountBase/details', views.details, name='account_details'),
    path('accountBase/settings', views.settings, name='account_settings'),
    path('inventory', views.inventory, name='inventory'),
    path('inventory/search/<str:query>', views.inventory_search, name='inventory_search'),
    path('inventory/manage/<int:book_isbn>', views.manage_book, name='manage_book'),
    path('transactions', views.transactions, name='transactions'),
    path('shipments', views.shipments, name='shipments'),


    # APIS
    path('books', apis.books, name='books'), # Viewing books
    path('api/books/<int:isbn>', apis.get_book, name='get_book'), # Get data of a book
    path('api/books/<int:isbn>/changestock/<int:value>', apis.change_book_stock,)

    # path('inventory')
    #...
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
