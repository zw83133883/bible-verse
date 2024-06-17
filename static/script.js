let audioPlaying = false;
let utterance;
const audioButton = document.querySelector('.audio-button');
function handleAudioStart() {
    audioPlaying = true;
}

function handleAudioStop() {
    audioPlaying = false;
    audioButton.classList.remove("playing")
}

function handleAudioPaused() {
    audioPlaying = false;
}

function handleClickPlayButton() {
    if (speechSynthesis.speaking) {
        speechSynthesis.cancel();
    } else {
        speechSynthesis.speak(utterance);
    }

    audioPlaying = speechSynthesis.speaking;
    if(audioPlaying)
        audioButton.classList.add("playing")
}

window.addEventListener('DOMContentLoaded', () => {
    const isOperaOnAndroid = navigator.userAgent.includes('Opera') && navigator.userAgent.includes('Android');
    const isWebviewOnAndroid = navigator.userAgent.includes('wv') && navigator.userAgent.includes('Android');

    if (isOperaOnAndroid || isWebviewOnAndroid) {
        document.querySelector('.audio-button').style.display = 'none';
    }
    const verseText = document.querySelector('.verse').innerText;
    const refText = document.querySelector('.reference').innerText;
    const text = refText + verseText
    utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;

    utterance.addEventListener('start', handleAudioStart);
    utterance.addEventListener('resume', handleAudioStart);
    utterance.addEventListener('pause', handleAudioPaused);
    utterance.addEventListener('end', handleAudioStop);
    utterance.addEventListener('error', handleAudioStop);

    window.addEventListener('beforeunload', () => speechSynthesis.cancel());

    document.querySelector('.audio-button').addEventListener('click', handleClickPlayButton);
});
