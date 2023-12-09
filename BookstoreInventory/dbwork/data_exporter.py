"""
Author: Charles (12/8/2023)
    
To better maintain object information for the database, writing/reading from .csv sheets is a good option.
Opposite to 'data_importer.py', this script will be responsible for selecting data from DB models
 writing data from various objects into the corresponding .csv

Processing of User model objects is not of interest and is excluded

The following object models are supported:
    Books
    Author
    Publisher
    Transaction
    Shipment
"""



import os, sys, shutil
from typing import Iterable

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
    Author, Book, Publisher, Shipment, Transaction, User
)

csv_data_dir = os.path.join(this_dir, 'data')
AUTHORS_FILE = os.path.join(csv_data_dir, "authors.csv")
PUBLISHERS_FILE = os.path.join(csv_data_dir, "publishers.csv")
BOOKS_FILE = os.path.join(csv_data_dir, "books.csv")
TRANSACTIONS_FILE = os.path.join(csv_data_dir, "transactions.csv")
SHIPMENTS_FILE = os.path.join(csv_data_dir, "shipments.csv")



def export_to_csv(fp:str, data_rows:list[list], key_columns:Iterable[int]=[]):
    """Exports each row of data into the given .csv file
    
        if key_columns is given, first existing row with matching data in specified columns will be replaced
        Leave key_columns empty to simply append rows
    """

    indexed_map = {} # Used to lookup rows by given key_columns
    if key_columns:
        data_rows = list(data_rows) # Create a copy of data_rows list to prevent modifying original list

        row_idx = len(data_rows)-1 # Rows are to be processed in reverse order
        while data_rows:
            row = data_rows.pop()
            row = list(map(str, row)) # Convert all elements to string (required)
            # Create a key that is a tuple of str(value) at indexed columns
            key = [str(row[i]) for i in key_columns] 

            # Set key in table to row
            # Also keeping track of row index to keep row order during export
            indexed_map[tuple(key)] = (row_idx, row) 
            row_idx -= 1

    if indexed_map:
        temp_fp = fp + ".tmp"
        # Open fp for read (utf-8-sig encoding to remove BOM https://docs.python.org/3/library/codecs.html#module-encodings.utf_8_sig)
        #   and open temp_fp for write
        with open(fp, "r", encoding="utf-8-sig") as f, open(temp_fp, "w") as temp_f:
            for line in f.readlines(): # Buffer through each line
                try:
                    data_row = line.rstrip().split(',') # Convert line to list
                    key = tuple([str(data_row[i]) for i     in key_columns])

                    # Write data to temp file
                    new_data = ",".join(indexed_map.pop(key, [])[1]) or line # Either pop new data found at matching index_cols key or original data
                    temp_f.write(new_data + "\n")

                except IndexError: # Likely due to overreached columns for key
                    temp_f.write(line) # Write original data

            # # Append any left over data_rows in indexed_map, keeping original order
            for _, data_row in sorted(indexed_map.values(), key=lambda v: v[0]):
                temp_f.write(",".join(data_row)+"\n")

        shutil.move(temp_fp, fp) # Replace original file with the temp file

    else:
        # Append data_rows
        with open(fp, "a") as f:
            for data_row in data_rows:
                # Convert all elements to string (required), then write to file
                f.write(    ",".join(   list(map(str, data_row))    ) + "\n" )


def export_authors():
    """Export authors in the column sequence: id, first_name, middle_name, last_name"""

    data_rows:list[list] = []
    data_rows.append(["id", "first_name", "middle_name", "last_name"]) # Add header

    for author in Author.objects.iterator():
        data_rows.append([
            author.id,
            author.first_name,
            author.middle_name,
            author.last_name
        ])

    export_to_csv(AUTHORS_FILE, data_rows, key_columns=(0,))

def export_publishers():
    """Export publishers in the column sequence: id, name, location"""

    data_rows:list[list] = []
    data_rows.append(["id", "name", "location"]) # Add header

    for publisher in Publisher.objects.iterator():
        data_rows.append([
            publisher.id,
            publisher.name,
            publisher.location
        ])

    export_to_csv(PUBLISHERS_FILE, data_rows, key_columns=(0,1,2))

def export_books():
    """Export books in the column sequence: isbn, author_ids, publisher_id, title, genre, summary, quantity, cost"""

    data_rows:list[list] = []
    data_rows.append(["isbn", "author_ids", "publisher_id", "title", "genre", "summary", "quantity", "cost"]) # Add header

    for book in Book.objects.iterator():
        author_ids = ";".join([str(author.id) for author in book.authors.all()])
        data_rows.append([
            book.isbn,
            ";".join([str(author.id) for author in book.authors.all()]), 
            book.publisher.id if book.publisher else "",
            book.title,
            book.genre,
            book.summary,
            book.quantity,
            book.cost
        ])

    export_to_csv(BOOKS_FILE, data_rows, key_columns=(0,))

def export_transactions():
    """Export transactions in the column sequence: id, book_isbn, date, quantity, cost"""

    data_rows:list[list] = []
    data_rows.append(["id", "book_isbn", "date", "quantity", "cost"]) # Add header

    for transaction in Transaction.objects.iterator():
        data_rows.append([
            transaction.id,
            transaction.book_isbn,
            transaction.date.strftime("%m/%d/%Y %I:%M %p") if transaction.date else "",
            transaction.quantity,
            transaction.cost
        ])

    export_to_csv(TRANSACTIONS_FILE, data_rows, key_columns=(0,1,2))

def export_shipments():
    """Export shipments in the column sequence: id, company, expected_date, transaction_id, cost, delivered"""

    data_rows:list[list] = []
    data_rows.append(["id", "company", "expected_date", "transaction_id", "cost", "delivered"]) # Add header

    for shipment in Shipment.objects.iterator():
        data_rows.append([
            shipment.id,
            shipment.company,
            shipment.expected_date.strftime("%m/%d/%Y %I:%M %p") if shipment.expected_date else "",
            shipment.transaction.id if shipment.transaction else "",
            shipment.cost,
            shipment.delivered

        ])

    export_to_csv(SHIPMENTS_FILE, data_rows, key_columns=(0,1,3))


# export_authors()
# export_publishers()
# export_books()
# export_transactions()
# export_shipments()