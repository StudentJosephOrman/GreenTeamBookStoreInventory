function update_details_card(book_data){
    const manage_btn = document.getElementById('manage-selected-book');

    // Enable manage button
    if(manage_btn){
        manage_btn.setAttribute('class', '');
    }

    const details_card = document.getElementById('details');

    if(details_card){
        details_card.style.display = 'inline';
        document.getElementById('selected-book-title').innerText = book_data['title'];
        document.getElementById('selected-book-genre').innerText = book_data['genre'];
        document.getElementById('selected-book-summary').innerText = book_data['summary'];
        document.getElementById('selected-book-authors').innerText = book_data['authors'].join('\n');
        // Publisher
        document.getElementById('selected-book-quantity').innerText = book_data['quantity'];
        document.getElementById('selected-book-cost').innerText = book_data['cost'];
    }
}

// When user clicks on book result
// Fetch book data and update details card
async function on_book_select(event){
    if(event.target){
        var info = event.target.innerText.substring(1).split('] ');
        const isbn = info[0];
        
        const response = await fetch(`/api/books/${isbn}`);
        const book_data = await response.json();

        if(book_data){
            update_details_card(book_data)
        }

        // Unset previously selected book item
        const selected_book_items = document.getElementsByClassName('book-item selected-item');
        if(selected_book_items){
            for (let el of selected_book_items) {
                el.setAttribute('class', 'book-item');
            }
        }

        // Set the 'selected book item' by adding the selected-item class
        event.target.setAttribute('class', 'book-item selected-item');
    }
}

function manage_book(event){
    // Get isbn from book-item that has the 'selected-item' class
    const selected_book_items = document.getElementsByClassName('selected-item');
    if(!selected_book_items) return;

    const info = selected_book_items[0].innerText.substring(1).split('] ');
    const isbn = info[0];
    
    // If isbn is empty, do nothing
    if(isbn.trim() == '') return;

    // Got to manage page for selected book
    window.location.replace(window.location.origin+`/inventory/manage/${isbn}`)
}

const search_bar = document.getElementById('search')
search_bar.onkeypress = function(event){
    // If user pressed enter and the search is not empty
    if(event.keyCode==13 && search_bar.value.trim() != ''){
        // Navigate to the search page passing in the query
        window.location.replace(window.location.origin+`/inventory/search/${search_bar.value}`)
    }
}