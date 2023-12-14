from django.apps import AppConfig

# This python script is a built-in DJango script, it automatically handles certain aspects of the database models, such as location
# and certain automatic fields in them.

class BookstoreinventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BookstoreInventory'
