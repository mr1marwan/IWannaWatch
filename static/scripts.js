document.addEventListener("DOMContentLoaded", function() {
    // Format vote averages on initial page load
    formatVoteAverages();

    document.getElementById('form').addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the form from submitting the traditional way

        const selectedGenre = document.getElementById('genre').value;
        const searchInput = document.getElementById('search_term').value;
        const actorName = document.getElementById('search_actor').value;
        const yearRelease = document.getElementById('release_year').value;
        const pop_Button = document.getElementById('pop_button');

        if (selectedGenre || searchInput || yearRelease || actorName || pop_Button.name === 'pop_button') {
            document.getElementById('form').submit();
        }
    });

    function formatVoteAverages() {
        // Format vote averages on initial page load and after form submission
        const voteAverageElements = document.querySelectorAll('.vote_average');
        voteAverageElements.forEach(function(element) {
            var voteAverageText = element.textContent;
            var voteAverageFloat = parseFloat(voteAverageText);
            if (!isNaN(voteAverageFloat)) {
                var formattedVoteAverage = voteAverageFloat.toFixed(1);
                element.textContent = formattedVoteAverage;
            }
        });
    }
});

function openmovie(movieId) {
    console.log("it's clicked");
    var newPageUrl = 'templates/movie.html/' + movieId;
    window.location.href = newPageUrl;
}


    // Get the modal and video frame elements
var modal = document.getElementById('myModal');
var videoFrame = document.getElementById('videoFrame'); 
    // Function to open the modal and set the video source
function openModal(trailerLink) {
      modal.style.display = 'block';
      videoFrame.src = trailerLink;
}
// Function to close the modal and stop the video
function closeModal() {
    modal.style.display = 'none';
    videoFrame.src = '';
}
function fetchAndOpenTrailer(movieId) {
    fetch(`/get_trailer/${movieId}`)
        .then(response => response.json())
        .then(data => {
            if (data.trailer_link) {
                openModal(data.trailer_link);
            } else {
                alert('Trailer not available.');
            }
        })
        .catch(error => {
            console.error('Error fetching trailer:', error);
            alert('Error fetching trailer.');
        });
}

    // Attach click event listeners to all trailer buttons
    var trailerButtons = document.querySelectorAll('.rating-trailer .buttonT');
    trailerButtons.forEach(function(button) {
        button.addEventListener('click', function() {
        var trailerLink = button.getAttribute('data-trailer');
        openModal(trailerLink);
      });
     });
