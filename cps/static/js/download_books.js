$(document).ready(function() {
    const searchProgress = $(`
        <div id="searchProgress" class="search-progress" style="display: none">
            <div class="progress-bar">
                <div class="progress-bar-fill"></div>
            </div>
            <div class="search-status">Searching...</div>
        </div>
        <div id="downloadProgress" class="search-progress" style="display: none">
            <div class="search-status">Downloading...</div>
        </div>
    `).insertAfter('#searchFORABUNCHOFBOOKS');

    $('#searchFORABUNCHOFBOOKS').on('submit', function(event) {
        event.preventDefault();
        const title = $('#bookTitle').val();
        const author = $('#bookAuthor').val();
        const category = $('#bookCategory').val();

        console.log("Search Libgen");
        // Disable the search button and show progress
        $('#searchFORABUNCHOFBOOKS button[type="submit"]').prop('disabled', true);
        $('#searchProgress').show();
        $('.progress-bar-fill').css('width', '0%');
        
        search_books(title, author, category);
    });
});

function search_books(title, author, category) {
    // Create a fake progress simulation since we can't get real progress
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += 5;
        if (progress <= 90) { // Only go up to 90% until we get actual results
            $('.progress-bar-fill').css('width', progress + '%');
        }
    }, 200);

    $.ajax({
        type: 'POST',
        url: '/search_books',
        contentType: 'application/json',
        data: JSON.stringify({ title: title, author: author, category: category }),
        
        success: function(data) {
            console.log("Success");
            // Complete the progress bar
            clearInterval(progressInterval);
            $('.progress-bar-fill').css('width', '100%');
            
            // Hide progress and enable button after a short delay
            setTimeout(() => {
                $('#searchProgress').hide();
                $('#searchFORABUNCHOFBOOKS button[type="submit"]').prop('disabled', false);
                list_books(data);
            }, 500);
        },
        
        error: function(xhr, status, error) {
            console.error("Search failed:", error);
            clearInterval(progressInterval);
            $('.search-status').text('Search failed: ' + error);
            $('.progress-bar-fill').css('background-color', '#ff4444');
            
            setTimeout(() => {
                $('#searchProgress').hide();
                $('#searchFORABUNCHOFBOOKS button[type="submit"]').prop('disabled', false);
            }, 2000);
        }
    });
}

function list_books(data) {
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

function download_book(book) {
    $('#downloadProgress').show();
    $.ajax({
        type: 'POST',
        url: '/download_book',
        contentType: 'application/json',
        data: JSON.stringify({ book: book }),
        
        success: function(data) {
            console.log(data);
            $('#downloadProgress').hide();
        }
    });
}