function update_details_card(summary, authors, quantity, cost){
    var details_card = document.getElementById('id');

    if(details_card){
        document.getElementById('selected-book-summary').innerText = summary;
        document.getElementById('selected-book-authors').innerText = authors;
        document.getElementById('selected-book-summary').innerText = summary;
        document.getElementById('selected-book-summary').innerText = summary;
    }
}

// On book hover in book list
// Fetch book data and update details card
async function on_book_hover(event){
    if(event.target){
        var info = event.target.innerText.split(' | ');
        const isbn = info[0];
        const name = info[1];
        
        const response = await fetch(window.location.origin+`api/books/${isbn}/`);
        const data = response.json();

        if(data){
            console.log(data)
        }
    }
}