const languageSelect = document.getElementById('languageSelect');

// Select all elements that need translation
const elementsToTranslate = document.querySelectorAll('.verse, .horoscope-date, .ratings-row, .lucky-info div');

function populateLanguageDropdown() {
    const languagesToInclude = [
        { code: 'en-US', name: 'English' },
        { code: 'es-ES', name: 'Español (España)' },
        { code: 'zh-CN', name: '中文（简体）' },
        { code: 'fr-FR', name: 'Français (France)' },
        { code: 'de-DE', name: 'Deutsch (Deutschland)' },
        { code: 'it-IT', name: 'Italiano (Italia)' },
        { code: 'ja-JP', name: '日本語 (日本)' }
        // Add more languages as needed
    ];

    // Populate the language dropdown
    languagesToInclude.forEach(lang => {
        const option = document.createElement('option');
        option.value = lang.code;
        option.textContent = lang.name;
        languageSelect.add(option);
    });

    // Set default language to English
    languageSelect.value = 'en-US';
}

// Function to translate all text elements
function translatePageContent(selectedLanguage) {
    elementsToTranslate.forEach(element => {
        const originalText = element.innerText; // Get the original text
        translateVerse(originalText, selectedLanguage) // Translate the text
            .then(translatedText => {
                element.innerText = translatedText; // Update the element with the translated text
            })
            .catch(error => {
                console.error('Translation error:', error);
                element.innerText = originalText; // If translation fails, keep original text
            });
    });
}

// Function to handle language change
languageSelect.addEventListener('change', () => {
    const selectedLanguage = languageSelect.value;
    translatePageContent(selectedLanguage); // Call the translation function for the selected language
});

// Function to translate text using Google Translate API
async function translateVerse(text, targetLanguage) {
    const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=${targetLanguage}&dt=t&q=${encodeURIComponent(text)}`;
    
    try {
        const response = await fetch(url);
        const data = await response.json();

        // Extract and concatenate all translated segments
        let translatedText = '';
        if (data && data[0] && data[0].length > 0) {
            data[0].forEach(segment => {
                if (segment && segment[0]) {
                    translatedText += segment[0];
                }
            });
        }

        return translatedText.trim(); // Return the translated text
    } catch (error) {
        console.error('Translation error:', error);
        return text; // Return the original text if translation fails
    }
}


// Initialize the dropdown and translations
window.addEventListener('DOMContentLoaded', () => {
    populateLanguageDropdown();
});
