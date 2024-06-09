// Define toggleAudio in the global scope
function toggleAudio() {
    var audio = document.getElementById('myAudio');
    var audioButton = document.getElementById('audioButton');

    if (audio.paused) {
        audio.play();
        audioButton.classList.add('playing');
    } else {
        audio.pause();
        audioButton.classList.remove('playing');
    }
}

// Add the event listener (no need to redefine toggleAudio here)
document.addEventListener('DOMContentLoaded', function() {
    // You can do other setup tasks here if needed
});