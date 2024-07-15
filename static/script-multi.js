let audioPlaying = false;
let utterance;
const audioButton = document.querySelector('.audio-button');
const languageSelect = document.getElementById('languageSelect')
const verseElement = document.querySelector('.verse').innerText;
const refText = document.querySelector('.reference').innerText;
let voices = []; // Declare voices here

function populateLanguageDropdownWindows() {
    const languagesToInclude = [
        { code: 'en-US', name: 'English' },
        { code: 'en-GB', name: 'English (UK)' },
        { code: 'es-ES', name: 'Español (España)' },
        { code: 'es-MX', name: 'Español (México)' },
        { code: 'zh-CN', name: '中文（简体）' },
        { code: 'zh-HK', name: '中文（香港）' },
        { code: 'zh-TW', name: '中文（台湾）' }, // Added Chinese (Taiwan)
        { code: 'fr-FR', name: 'Français (France)' },
        { code: 'de-DE', name: 'Deutsch (Deutschland)' },
        { code: 'it-IT', name: 'Italiano (Italia)' },
        { code: 'pt-PT', name: 'Português (Portugal)' },
        { code: 'ru-RU', name: 'Русский (Россия)' },
        { code: 'ja-JP', name: '日本語 (日本)' },
        { code: 'ko-KR', name: '한국어 (대한민국)' }
        // Add more languages as needed
    ];

    // Populate dropdown with predefined languages
    languagesToInclude.forEach(lang => {
        const option = document.createElement('option');
        option.value = lang.code;
        option.textContent = lang.name; 
        languageSelect.add(option);
    });

    // Set default language and update the verse content
    languageSelect.value = 'en-US'; 
    updateVerseAndUtterance('en-US'); 
}

function populateLanguageDropdownMobile() {
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

// Example function to load voices asynchronously (replace with actual implementation)
async function loadVoices() {
    return new Promise(resolve => {
        setTimeout(() => {
            const voices = speechSynthesis.getVoices();
            resolve(voices); // Resolve with voices
        }, 1000); // Simulated delay; adjust as needed
    });
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

    // Update play button state based on speech synthesis status
    utterance.onstart = () => {
        audioPlaying = true;
        audioButton.classList.add("playing");
    };

    utterance.onend = () => {
        audioPlaying = false;
        audioButton.classList.remove("playing");
    };

    utterance.onerror = () => {
        audioPlaying = false;
        audioButton.classList.remove("playing");
    };

    audioPlaying = speechSynthesis.speaking;
    if (!audioPlaying) {
        audioButton.classList.remove("playing");
    }
}
function updateVerseAndUtterance(selectedLanguage) {
    const originalVerseText = verseElement;
    console.log(originalVerseText);
    const originalRefText = refText; // Get the reference text from its variable

    // Translate both verse and reference
    Promise.all([
        translateVerse(originalVerseText, selectedLanguage),
        translateVerse(originalRefText, selectedLanguage)
    ])
        .then(([translatedVerse, translatedRef]) => {
            document.querySelector('.verse').innerText = translatedVerse;
            document.querySelector('.reference').innerText = translatedRef; // Update the reference element

            utterance = new SpeechSynthesisUtterance(translatedRef + translatedVerse);
            utterance.rate = 1;
            utterance.lang = selectedLanguage;

            const availableVoices = voices.filter(voice => voice.lang.includes(selectedLanguage));
            if (availableVoices.length > 0) {
                utterance.voice = availableVoices[0];
            }
        })
        .catch(error => {
            console.error('Translation error:', error);
            utterance.text = "Your device does not support this language";
            speechSynthesis.speak(utterance);
        });
}
async function translateVerse(text, targetLanguage) {
    const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=${targetLanguage}&dt=t&q=${encodeURI(text)}`;
    try {
        const response = await fetch(url);
        const data = await response.json();

        // Extract and concatenate all translated segments
        let translatedText = '';
        if (data && data.length > 0) {
            data[0].forEach(segment => {
                if (segment && segment[0]) {
                    translatedText += segment[0];
                }
            });
        }

        return translatedText.trim(); // Trim to remove any extra spaces
    } catch (error) {
        console.error('Translation error:', error);
        return text; // Return original text if translation fails
    }
}

window.addEventListener('DOMContentLoaded', () =>  {
    const isSpeechSynthesisSupported = 'speechSynthesis' in window;

    const isOperaOnAndroid = navigator.userAgent.includes('Opera') && navigator.userAgent.includes('Android');
    const isWebviewOnAndroid = navigator.userAgent.includes('wv') && navigator.userAgent.includes('Android');

    if (isOperaOnAndroid || isWebviewOnAndroid) {
        document.querySelector('.audio-button').style.display = 'none';
    }

    if(isSpeechSynthesisSupported){
        // Check if the user agent indicates a mobile device
        // const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        // const isAndroid = navigator.userAgent.includes('Android');
        // if (!isMobile || isAndroid) {
        //     const event = new Event('populateLanguageDropdown');
        //     window.dispatchEvent(event);
        // } else {
        //     populateLanguageDropdownMobile();
        // }
        populateLanguageDropdownWindows();
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
        languageSelect.addEventListener('change', () => {
            updateVerseAndUtterance(languageSelect.value);
            handleAudioStop();
            speechSynthesis.cancel();
        });
    }else{
        document.querySelector('.audio-button').style.display = 'none';
    }
});

// Event listener for custom event to populate language dropdown
window.addEventListener('populateLanguageDropdown', () => {
    populateLanguageDropdownWindows();
});


