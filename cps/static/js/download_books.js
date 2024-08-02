$(document).ready(function() {
    $('#searchFORABUNCHOFBOOKS').on('submit', function(event) {
        event.preventDefault();
        const title = $('#bookTitle').val();
        const author = $('#bookAuthor').val();
        const category = $('#bookCategory').val();

        console.log("Search Libgen");
        search_books(title, author, category);
    });
});

function search_books(title, author, category) {
    $.ajax({
        type: 'POST',
        url: '/search_books',
        contentType: 'application/json',
        data: JSON.stringify({ title: title, author: author, category: category }),
        
        success: function(data){
            console.log("Success");
            list_books(data);
        }
    });
}

function list_books(data){
    console.log("SUCCESS");
    $('#list_results tbody').empty();
    if (data.length === 0) {
        console.log("EMPTY");
        $('#list_results tbody').append('<tr><td colspan="3">No books found</td></tr>');
    } else {
        console.log(data);
            data.forEach(function(book, index) {
                const row = $('<tr></tr>').append(
                    $('<td></td>').text(book.Title),
                    $('<td></td>').text(book.Author),
                    $('<td></td>').text(book.File)
                );
                row.on('click', function() {
                    console.log(book);
                    download_book(book);
                });
                $('#list_results tbody').append(row);
            });
    }
}

function download_book(book){
    $.ajax({
        type: 'POST',
        url: '/download_book',
        contentType: 'application/json',
        data: JSON.stringify({ book: book }),
        
        success: function(data){
            console.log(data);
        }
    });
}
