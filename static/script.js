// Function to make a color slightly darker
function darkenColor(color, percent) {
    const rgb = color.match(/\d+/g); // Extract the RGB values
    const r = Math.max(0, Math.min(255, parseInt(rgb[0]) - (255 * percent / 100)));
    const g = Math.max(0, Math.min(255, parseInt(rgb[1]) - (255 * percent / 100)));
    const b = Math.max(0, Math.min(255, parseInt(rgb[2]) - (255 * percent / 100)));
    return `rgb(${r}, ${g}, ${b})`;
}

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
    

    // Update lucky info and background colors
    const luckyColorItem = document.querySelector('.lucky-info-container .lucky-item:nth-child(1)');
    luckyColorItem.querySelector('.lucky-circle').innerText = data.lucky_color; // Update text inside the circle
    luckyColorItem.style.backgroundColor = data.lucky_color_rect_color; // Update background color
    luckyColorItem.querySelector('.lucky-circle').style.color = darkenColor(data.lucky_color_rect_color, 30); // Darken the text color
    luckyColorItem.querySelector('.lucky-label').style.color = darkenColor(data.lucky_color_rect_color, 30); // Darken the label color

    const luckyNumberItem = document.querySelector('.lucky-info-container .lucky-item:nth-child(2)');
    luckyNumberItem.querySelector('.lucky-circle').innerText = data.lucky_number; // Update text inside the circle
    luckyNumberItem.style.backgroundColor = data.lucky_number_rect_color; // Update background color
    luckyNumberItem.querySelector('.lucky-circle').style.color = darkenColor(data.lucky_number_rect_color, 30); // Darken the text color
    luckyNumberItem.querySelector('.lucky-label').style.color = darkenColor(data.lucky_number_rect_color, 30); // Darken the label color

    const matchingSignItem = document.querySelector('.lucky-info-container .lucky-item:nth-child(3)');
    matchingSignItem.querySelector('.lucky-circle').innerText = data.matching_sign; // Update text inside the circle
    matchingSignItem.style.backgroundColor = data.matching_sign_rect_color; // Update background color
    matchingSignItem.querySelector('.lucky-circle').style.color = darkenColor(data.matching_sign_rect_color, 30); // Darken the text color
    matchingSignItem.querySelector('.lucky-label').style.color = darkenColor(data.matching_sign_rect_color, 30); // Darken the label color

        // **Update the background image**
    document.querySelector('.horoscope-container').style.backgroundImage = `url('/static/${data.image_path}')`;

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
                // Log fetched data
                console.log('Fetched Data:', data);

                // Update the content with the new horoscope data
                updateHoroscope(data);

                // Set the active state for the selected day
                document.querySelectorAll('.calendar-item').forEach(el => el.classList.remove('active'));
                this.classList.add('active');
            })
            .catch(error => console.error('Error fetching horoscope:', error));
    });
});
