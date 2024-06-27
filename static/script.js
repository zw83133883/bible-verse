let audioPlaying = false;
let utterance;
const audioButton = document.querySelector('.audio-button');
const languageSelect = document.getElementById('languageSelect')
const verseElement = document.querySelector('.verse');
const refText = document.querySelector('.reference').innerText;
let voices = []; // Declare voices here

function populateLanguageDropdown() {
    // Add event listener to populate dropdown when voices change
    speechSynthesis.onvoiceschanged = () => {
        voices = speechSynthesis.getVoices();
        if (voices.length === 0) {
            console.error("No voices found.");
            return;
        }

        languageSelect.innerHTML = ''; // Clear existing options
        const uniqueLanguages = Array.from(new Set(voices.map(voice => voice.lang)));

        uniqueLanguages.forEach(lang => {
            const option = document.createElement('option');
            option.value = lang;
            option.text = lang; 
            languageSelect.add(option);
        });

        // Set default language and update the verse content
        languageSelect.value = 'en-US'; 
        updateVerseAndUtterance('en-US'); 
    };
}
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
function updateVerseAndUtterance(selectedLanguage) {
    const originalVerseText = verseElement.textContent;
    const originalRefText = refText; // Get the reference text from its variable

    // Translate both verse and reference
    Promise.all([
        translateVerse(originalVerseText, selectedLanguage),
        translateVerse(originalRefText, selectedLanguage)
    ])
        .then(([translatedVerse, translatedRef]) => {
            verseElement.textContent = translatedVerse;
            document.querySelector('.reference').textContent = translatedRef; // Update the reference element

            utterance = new SpeechSynthesisUtterance(translatedRef + translatedVerse);
            utterance.lang = selectedLanguage;

            const availableVoices = voices.filter(voice => voice.lang.startsWith(selectedLanguage));
            if (availableVoices.length > 0) {
                utterance.voice = availableVoices[0];
            }
        })
        .catch(error => {
            console.error('Translation error:', error);
        });
}
function getVoices() {
    voices = speechSynthesis.getVoices();
    populateLanguageDropdown(voices); // Immediately populate once voices are fetched
}
async function translateVerse(text, targetLanguage) {
    const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=${targetLanguage}&dt=t&q=${encodeURI(text)}`;
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data[0][0][0];
    } catch (error) {
        console.error('Translation error:', error);
        return text; // Return original text if translation fails
    }
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
    populateLanguageDropdown(); 
});

languageSelect.addEventListener('change', () => {
    updateVerseAndUtterance(languageSelect.value);
    handleClickPlayButton();
});
