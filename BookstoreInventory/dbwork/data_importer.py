"""
Author: Charles (12/4/2023)
    
To better maintain object information for the database, writing/reading from .csv sheets is a good option.
For simplicity, this script will only be responsible for reading .csv sheets for each object model
 and writing the data respective to each object model into the database.

This excludes the User model as such data will be managed through the Django system

The following object models are supported:
    Books
    Author
    Publisher
    Transaction
    Shipment
"""



import csv, os, sys
from datetime import datetime

this_dir = os.path.dirname(__file__)
project_dir = "\\".join(this_dir.split("\\")[:-2]) # Project directory is 2 directories back from this_dir

sys.path.append(project_dir) # Add project path to sys.paths

# Activate django env
import django

# Set the 'DJANGO_SETTINGS_MODULE' env variable for django to work
# Ability to find module depends on current directory
working_folder = os.path.abspath(os.curdir).split(os.path.sep)[-1]
if working_folder == 'GreenTeamBookStoreInventory':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'GreenTeamProject.GreenTeamProject.settings'
elif working_folder == 'GreenTeamProject':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'GreenTeamProject.settings'

django.setup()

from BookstoreInventory.models import (
    Author, Book, Publisher, Shipment, Transaction
)

csv_data_dir = os.path.join(this_dir, 'data')
AUTHORS_FILE = os.path.join(csv_data_dir, "authors.csv")
PUBLISHERS_FILE = os.path.join(csv_data_dir, "publishers.csv")
BOOKS_FILE = os.path.join(csv_data_dir, "books.csv")
TRANSACTIONS_FILE = os.path.join(csv_data_dir, "transactions.csv")
SHIPMENTS_FILE = os.path.join(csv_data_dir, "shipments.csv")


# Fancy ANSI color coding stuff
error_msg = lambda msg: f"\033[1;31;40m{msg}\033[0m"
warn_msg = lambda msg: f"\033[1;38;5;208m{msg}\033[0m"
success_msg = lambda msg: f"\033[0;32m{msg}\033[0m"
highlight_msg = lambda msg: f"\033[4;33m{msg}\033[0m"


def read_csv(fp:str) -> list[list]:
    """Returns a row data of the given .csv file"""

    read_data = []

    def to_datatypes(row_data:list[str]) -> list:
        """Modifies the array of data elements converted to appropriate datatypes

        Note: Int is automatically converted to float
        """
        row_idx = 0
        while row_idx < len(row_data):
            if not row_data[row_idx]: # Check empty field
                row_data[row_idx] = None
            elif row_data[row_idx].lower() in ('true', 'false'): # Check if boolean
                row_data[row_idx] = bool(row_data[row_idx])
            else:
                try:
                    as_num = float(row_data[row_idx])
                    as_num = int(as_num) if int(as_num) == as_num else as_num   # Check if float could be converted to integer without losing info
                    row_data[row_idx] = as_num
                except:
                    pass # Number conversion failed, keep the usual string

            row_idx += 1
    
    with open(fp, "r") as f:
        for row in csv.reader(f):
            to_datatypes(row) # Modifies elements in place
            read_data.append(row)

    return read_data


def import_authors(save_instances=False):
    """Loads records from authors.csv into database
        Expected headers/order:
            id, first_name, middle_name, last_name


        Saves to database if save_instances is true
    """

    _, *rows = read_csv(AUTHORS_FILE)

    for id, first_name, middle_name, last_name in rows:
        print(highlight_msg(f"Observing Publisher(id={id}, full_name={first_name, middle_name, last_name})"))

        author = Author(id=id, first_name=first_name, middle_name=middle_name, last_name=last_name)

        if save_instances:
            author.save()

        print(success_msg(f"\tImported: Author{first_name, middle_name, last_name}"), "(SAVED)" if save_instances else "(NOT SAVED)")


def import_publishers(save_instances=False):
    """Loads records from publishers.csv into database
        Expected headers/order:
            id, name, location

        Saves to database if save_instances is true
    """
    _, *rows = read_csv(PUBLISHERS_FILE)

    for id, name, location in rows:
        print(highlight_msg(f"Observing Publisher(id={id}, name={name})"))

        publisher = Publisher(
            id=id,
            name=name,
            location=location
        )

        if save_instances:
            publisher.save()

        print(success_msg(f"\tImported: Publisher({name})"), "(SAVED)" if save_instances else "(NOT SAVED)")


def import_books(save_instances=False):
    """Loads records from books.csv into database
        Expected headers/order:
            isbn, author_ids, publisher_id, title, genre, summary, quantity, cost

        Saves to database if save_instances is true
    """

    _, *rows = read_csv(BOOKS_FILE)
    for isbn, author_ids, publisher_id, title, genre, summary, quantity, cost in rows:
        print(highlight_msg(f"Observing Book(isbn={isbn}, title={title})"))

        authors:list[Author] = []
        if isinstance(author_ids, str):
            skip_book = False
            for id in author_ids.split(';'):
                try:
                    authors.append( Author.objects.get( id=int(id.strip()) ) )
                except:
                    print(error_msg(f"\tAuthor id ({id}) doesn't exist! Book skipped..."))
                    skip_book = True
                    break

            if skip_book:
                continue

        elif isinstance(author_ids, int): # One id was given
            try:
                authors.append( Author.objects.get(id=author_ids) )
            except Exception as e:
                print(e)
                print(error_msg(f"\tAuthor id ({author_ids}) doesn't exist! Book skipped..."))
                continue

        try:
            publisher = Publisher.objects.get(id=publisher_id)
        except:
            print(error_msg(f"\tPublisher id ({publisher_id}) doesn't exist! Book skipped..."))
            continue

        book = Book(
            isbn = isbn,
            publisher=publisher,
            title = title,
            genre = genre,
            summary = summary,
            quantity = quantity,
            cost = cost
        )

        if save_instances:
            book.save()

        # Must set authors after instance is saved
        book.authors.set(authors) # Required for many-to-many relationship assignment

        print(success_msg(f"\tImported: Book({title})"), "(SAVED)" if save_instances else "(NOT SAVED)")


### BELOW IS NOT PARTICULARILY TO BE USED FOR MANUAL ENTRIES###
# USE THESE FOR DATA RESTORE INSTEAD
def import_transactions(save_instances=False):
    """Loads records from transactions.csv into database
        Expected headers/order:
            id, book_isbn, date, quantity, cost

        Saves to database if save_instances is true
    """

    _, *rows = read_csv(TRANSACTIONS_FILE)
    for id, book_isbn, date, quantity, cost in rows:
        print(highlight_msg(f"Observing Transaction(id={id}, book_isbn={book_isbn})"))

        # Validate book_isbn?
        
        transaction = Transaction(
            id=id,
            book_isbn=book_isbn,
            date=datetime.strptime(date, "%m/%d/%Y %I:%M %p"),
            quantity=quantity,
            cost=cost
        )

        if save_instances:
            transaction.save()

        print(success_msg(f"\tImported: Transaction({id})"), "(SAVED)" if save_instances else "(NOT SAVED)")


def import_shipments(save_instances=False):
    """Loads records from shipments.csv into database
        Expected headers/order:
            id, company, expected_date, transaction_id, cost, delivered

        Saves to database if save_instances is true
    """
    _, *rows = read_csv(SHIPMENTS_FILE)

    for id, company, expected_date, transaction_id, cost, delivered in rows:
        try:
            transaction = Transaction.objects.get(id=transaction_id)
        except:
            print(error_msg(f"Transaction id ({transaction_id}) doesn't exist! Shipment skipped..."))
            continue

        shipment = Shipment(
            id=id,
            company=company,
            expected_date=datetime.strptime(expected_date, "%m/%d/%Y %I:%M %p"),
            transaction=transaction,
            cost=cost,
            delivered=delivered
        )

        if save_instances:
            shipment.save()

        print(success_msg(f"\tImported: Shipment({id})"), "(SAVED)" if save_instances else "(NOT SAVED)")

#################################################################
        



        

# import_authors(save_instances=True)
# import_publishers(save_instances=True)
# import_books(save_instances=True)
# import_transactions(save_instances=True)
# import_shipments(save_instances=True)