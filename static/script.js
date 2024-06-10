// Define toggleAudio in the global scope
function toggleAudio() {
    const audio = document.getElementById('myAudio');
    const audioButton = document.getElementById('audioButton');

    if (audio.paused) {
        audio.play();
        audioButton.classList.add('playing');
    } else {
        audio.pause();
        audioButton.classList.remove('playing');
    }
}

// Add event listeners when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const audio = document.getElementById('myAudio');
    const audioButton = document.getElementById('audioButton');

    // Event listener for when audio ends
    audio.addEventListener('ended', () => {
        audioButton.classList.remove('playing');
    });
});