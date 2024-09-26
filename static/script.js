// Function to update the horoscope content on the page
function updateHoroscope(data) {
    // Update the date
    document.querySelector('.date').innerText = data.date;

    // Update the horoscope message
    document.querySelector('.horoscope-message').innerText = data.message;

    // Update the overall rating stars
    const overallRatingContainer = document.querySelector('.overall-rating .stars');
    overallRatingContainer.innerHTML = '';  // Clear current stars
    for (let i = 0; i < data.overall_rating; i++) {
        overallRatingContainer.innerHTML += '<i class="fas fa-star"></i>';
    }

    // Update the love rating stars
    const loveRatingContainer = document.querySelector('.rating-block:nth-child(1) .stars');
    loveRatingContainer.innerHTML = '';  // Clear current stars
    for (let i = 0; i < data.love_rating; i++) {
        loveRatingContainer.innerHTML += '<i class="fas fa-star"></i>';
    }

    // Update the career rating stars
    const careerRatingContainer = document.querySelector('.rating-block:nth-child(2) .stars');
    careerRatingContainer.innerHTML = '';  // Clear current stars
    for (let i = 0; i < data.career_rating; i++) {
        careerRatingContainer.innerHTML += '<i class="fas fa-star"></i>';
    }

    // Update the health rating stars
    const healthRatingContainer = document.querySelector('.rating-block:nth-child(3) .stars');
    healthRatingContainer.innerHTML = '';  // Clear current stars
    for (let i = 0; i < data.health_rating; i++) {
        healthRatingContainer.innerHTML += '<i class="fas fa-star"></i>';
    }

    // Update the wealth rating stars
    const wealthRatingContainer = document.querySelector('.rating-block:nth-child(4) .stars');
    wealthRatingContainer.innerHTML = '';  // Clear current stars
    for (let i = 0; i < data.wealth_rating; i++) {
        wealthRatingContainer.innerHTML += '<i class="fas fa-star"></i>';
    }

    // Update lucky info
    document.querySelector('.lucky-info-container .lucky-item:nth-child(1) .lucky-detail').innerText = data.lucky_color;
    document.querySelector('.lucky-info-container .lucky-item:nth-child(2) .lucky-detail').innerText = data.lucky_number;
    document.querySelector('.lucky-info-container .lucky-item:nth-child(3) .lucky-detail').innerText = data.matching_sign;
}

// Event listeners for calendar items
document.querySelectorAll('.calendar-item').forEach(item => {
    item.addEventListener('click', function (event) {
        event.preventDefault();  // Prevent full page reload

        const url = this.href;  // Get the URL for the selected day

        // Fetch the horoscope data
        fetch(url)
            .then(response => response.json())
            .then(data => {
                // Update the content with the new horoscope data
                updateHoroscope(data);

                // Set the active state for the selected day
                document.querySelectorAll('.calendar-item').forEach(el => el.classList.remove('active'));
                this.classList.add('active');
            })
            .catch(error => console.error('Error fetching horoscope:', error));
    });
});
