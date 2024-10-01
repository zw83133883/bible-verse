const zodiacVideos = {
    aries: { videoId: 'OHpMh4_Zx7o', startTime: 101, title: 'Aries: The Golden Ram (March 21 - April 19)' },
    leo: { videoId: 'OHpMh4_Zx7o', startTime: 294, title: 'Leo: Hercules and the Nemean Lion (July 23 - August 22)' },
    taurus: { videoId: 'OHpMh4_Zx7o', startTime: 147, title: 'Taurus: Zeus and Europa (April 20 - May 20)' },
    gemini: { videoId: 'OHpMh4_Zx7o', startTime: 191, title: 'Gemini: Castor and Pollux (May 21 - June 20)' },
    cancer: { videoId: 'OHpMh4_Zx7o', startTime: 234, title: 'Cancer: Hercules and the Hydra (June 21 - July 22)' },
    virgo: { videoId: 'OHpMh4_Zx7o', startTime: 266, title: 'Virgo: Astraea, the Goddess of Justice (August 23 - September 22)' },
    libra: { videoId: 'OHpMh4_Zx7o', startTime: 328, title: 'Libra: The Scales of Themis (September 23 - October 22)' },
    scorpio: { videoId: 'OHpMh4_Zx7o', startTime: 359, title: 'Scorpio: Orion and the Scorpion (October 23 - November 21)' },
    sagittarius: { videoId: 'OHpMh4_Zx7o', startTime: 396, title: 'Sagittarius: The Wisdom of Chiron (November 22 - December 21)' },
    capricorn: { videoId: 'OHpMh4_Zx7o', startTime: 424, title: 'Capricorn: Pan and the Sea-Goat (December 22 - January 19)' },
    aquarius: { videoId: 'OHpMh4_Zx7o', startTime: 466, title: 'Aquarius: Ganymede, Cupbearer of the Gods (January 20 - February 18)' },
    pisces: { videoId: 'OHpMh4_Zx7o', startTime: 502, title: 'Pisces: Eros and Aphrodite as Fish (February 19 - March 20)' }
};


const zodiacStories = {
    aries: `
    The sign of Aries is symbolized by the ram and is rooted in the ancient Greek myth of Phrixus and Helle. According to legend, Phrixus, a prince of Boeotia, was the target of a conspiracy by his stepmother, Ino, who wanted him killed. His mother, Nephele, prayed for her children’s safety, and Hermes sent a golden ram to rescue Phrixus and his sister Helle. As they flew through the sky on the ram, Helle tragically fell into the sea, creating the body of water known as Hellespont. Phrixus safely reached Colchis and sacrificed the ram in gratitude, hanging its prized Golden Fleece in a sacred grove, which later became the target of Jason and the Argonauts.<br><br>

    <strong>Highlights:</strong><br><br>
    🐏 Phrixus is rescued by the golden ram.<br><br>
    🌊 Helle falls into the sea, creating the Hellespont.<br><br>
    🌌 The golden ram is placed in the sky as the Aries constellation.<br><br>

    <strong>Key Insights:</strong><br><br>
    💔 <strong>Tragic Loss</strong>: Helle’s fall into the sea symbolizes the fragility of life and fate.<br><br>
    🐏 <strong>Rescue and Sacrifice</strong>: The story reflects themes of divine intervention and the cost of salvation.<br><br>
    🌌 <strong>Legacy</strong>: The Golden Fleece and the ram's placement among the stars emphasize the lasting impact of heroic deeds.
    `,
    taurus: `
    The sign of Taurus represents Zeus's metamorphosis into a bull to attract and abduct the princess Europa. In his bovine form, Zeus approached the princess, and she was delighted with the beautiful animal. Europa climbed onto the bull, which took her for a ride. Initially, Europa enjoyed riding the waves, but Zeus took her to the island of Crete against her will. The couple united and gave birth to noble offspring, including King Minos, who ruled Crete, the land of the Fearsome Minotaur. The constellation Taurus marked another of Zeus's ruses.<br><br>

    <strong>Highlights:</strong><br><br>
    🐂 Zeus transforms into a majestic bull.<br><br>
    🌊 Europa is carried across the sea to Crete.<br><br>
    👑 The union results in the birth of King Minos.<br><br>

    <strong>Key Insights:</strong><br><br>
    💔 <strong>Abduction</strong>: The myth underscores Zeus's power and deception in love.<br><br>
    🌊 <strong>Transformation</strong>: Zeus's use of disguise to achieve his goals highlights the fluidity of power.<br><br>
    👑 <strong>Royal Lineage</strong>: The birth of Minos links the story to Crete’s royal heritage.
    `,

    gemini: `
    The sign of Gemini is associated with the myth of the brothers Castor and Pollux, brothers of Helen of Troy and sons of Leda and Zeus. Zeus transformed into a swan to seduce Leda, and the twins were born from an egg. The twins became great heroes, but Castor died in Pollux's arms after a fight with rivals. Distraught, Pollux asked Zeus to bring his brother back to life. Zeus proposed that the brothers rotate their days on Earth, and the twins began to live alternately in the same body. The Gemini constellation symbolizes the brotherly love between the two sons of Zeus.<br><br>

    <strong>Highlights:</strong><br><br>
    👥 Castor and Pollux are great heroes.<br><br>
    ⚔️ Castor dies in battle.<br><br>
    🌌 Pollux shares his immortality with his brother.<br><br>

    <strong>Key Insights:</strong><br><br>
    👥 <strong>Brotherly Love</strong>: The bond between the twins reflects deep familial love and sacrifice.<br><br>
    🌌 <strong>Immortality</strong>: Their story shows how loyalty can transcend mortality.<br><br>
    ⚔️ <strong>Duality</strong>: Gemini represents the balance between life and death, and the merging of opposites.
    `,

    cancer: `
    The sign of Cancer is symbolized by a crab. The creature is associated with the myth of Hercules, who was battling the powerful Hydra of Lerna. Hera, the goddess, sent the crab to aid the Hydra in its fight against Hercules. Despite its efforts, the crab could not measure up to Hercules and was defeated. In honor of the creature's efforts, the goddess placed the crab among the stars in the constellation of Cancer.<br><br>

    <strong>Highlights:</strong><br><br>
    🦀 Hera sends a crab to aid the Hydra.<br><br>
    🗡️ Hercules crushes the crab during his battle.<br><br>
    🌌 The crab is honored in the stars by Hera.<br><br>

    <strong>Key Insights:</strong><br><br>
    🦀 <strong>Loyalty</strong>: The crab’s sacrifice represents loyalty and courage in the face of overwhelming odds.<br><br>
    🗡️ <strong>Divine Opposition</strong>: The myth reflects the struggles between mortals and gods.<br><br>
    🌌 <strong>Constellation Creation</strong>: Hera’s decision to place the crab in the stars shows how even small efforts can be immortalized.
    `,

    leo: `
    The sign of Leo is associated with the myth of Hercules and his twelve famous labors. The Nemean Lion terrorized the region, and Hercules was sent to confront the creature, which had an impenetrable hide that no weapon could harm. Hercules faced the beast with courage in a fierce fight and eventually strangled the lion. He went on to wear the Nemean Lion's skin as a cloak. This victory was eternalized in the stars in the form of the constellation Leo.<br><br>

    <strong>Highlights:</strong><br><br>
    🦁 The Nemean Lion terrorizes the region.<br><br>
    💪 Hercules defeats the lion with his strength.<br><br>
    🌌 The lion is honored in the sky as Leo.<br><br>

    <strong>Key Insights:</strong><br><br>
    🦁 <strong>Strength and Courage</strong>: Hercules’s battle with the Nemean Lion symbolizes bravery.<br><br>
    🌌 <strong>Endurance</strong>: The story reflects how challenges, when faced head-on, can lead to immortality in the stars.<br><br>
    💪 <strong>Victory</strong>: The myth is a testament to human resilience and strength.
    `,

    virgo: `
    The sign of Virgo is associated with the goddess Astraea, daughter of Themis, the goddess of justice. Astraea personified purity and innocence and was considered a just and impartial deity. She initially lived among humans, trying to promote justice. However, during the Iron Age, humanity became so corrupt that the goddess decided to leave Earth and ascended to the heavens, where she became the constellation of Virgo.<br><br>

    <strong>Highlights:</strong><br><br>
    ⚖️ Astraea represents purity and justice.<br><br>
    🌍 She leaves the Earth due to mankind’s wickedness.<br><br>
    🌌 She becomes the constellation Virgo.<br><br>

    <strong>Key Insights:</strong><br><br>
    ⚖️ <strong>Justice</strong>: Astraea’s departure symbolizes the loss of innocence in the world.<br><br>
    🌌 <strong>Purity</strong>: The myth reflects the importance of moral and spiritual integrity.<br><br>
    🌍 <strong>Ascension</strong>: Her ascension into the stars represents hope that purity and justice will return.
    `,

    libra: `
    The sign of Libra is symbolized by the scales of Themis, the Greek goddess of justice and balance. The goddess is known for her wisdom in dispensing justice, being merciful to the good and unforgiving to criminals. In later depictions, Themis appeared with a blindfold over her eyes, signifying that all are equal before justice and that her judgment is unbiased. The scales of the goddess remain in the heavens in the form of the constellation Libra.<br><br>

    <strong>Highlights:</strong><br><br>
    ⚖️ Themis is the goddess of justice.<br><br>
    🌍 She ensures balance and fairness.<br><br>
    🌌 Her scales are placed among the stars as Libra.<br><br>

    <strong>Key Insights:</strong><br><br>
    ⚖️ <strong>Justice</strong>: The scales symbolize fairness and balance in all things.<br><br>
    🌌 <strong>Equality</strong>: Libra reminds us that all are equal before the law and the stars.<br><br>
    🌍 <strong>Balance</strong>: The myth reflects the universal need for balance and equilibrium.
    `,

    scorpio: `
    The sign of Scorpio is associated with the myth of Orion and Artemis. Orion was a giant and a great hunter, and he had a close relationship with Artemis, the goddess of the hunt. According to some versions of the myth, their relationship seemed almost romantic. Apollo, Artemis's brother, sent a scorpion to kill Orion to preserve his sister's purity. Both Orion and the scorpion died in battle and were immortalized in the constellations of Orion and Scorpio.<br><br>

    <strong>Highlights:</strong><br><br>
    🦂 Gaia sends a scorpion to kill Orion.<br><br>
    🏹 Orion dies in battle with the scorpion.<br><br>
    🌌 Both are immortalized as constellations.<br><br>

    <strong>Key Insights:</strong><br><br>
    🦂 <strong>Vengeance</strong>: The scorpion represents retribution and the power of the natural world.<br><br>
    🏹 <strong>Mortality</strong>: Orion’s death reflects the inevitability of fate.<br><br>
    🌌 <strong>Immortality in the Stars</strong>: The myth emphasizes the enduring nature of conflict, both celestial and human.
    `,
    capricorn: `
    The sign of Capricorn is symbolized by a fish-tailed goat, associated with the myth of Pan, the wild god. During the battle with Typhon, many gods transformed into animals to escape. Pan jumped into the sea to escape and developed a fishtail to flee. Although this seems like a cowardly act, Pan was one of the few gods who returned to help Zeus defeat Typhon. The constellation of Capricorn represents Pan's transformation.<br><br>

    <strong>Highlights:</strong><br><br>
    🐐 Pan transforms into a sea-goat to escape the monster Typhon.<br><br>
    🌊 He flees into the sea, growing a fishtail.<br><br>
    🌌 Pan is immortalized as the constellation Capricorn.<br><br>

    <strong>Key Insights:</strong><br><br>
    🐐 <strong>Survival</strong>: Capricorn represents the instinct to adapt and survive against overwhelming odds.<br><br>
    🌊 <strong>Transformation</strong>: Pan’s story reflects the theme of change and metamorphosis.<br><br>
    🌌 <strong>Endurance</strong>: Capricorn’s place in the stars reminds us of the strength to overcome adversity.
    `,

    aquarius: `
    The sign of Aquarius evokes the myth of the abduction of the beautiful Ganymede, who was so handsome that Zeus kidnapped him to serve the gods on Olympus. Ganymede replaced Hebe as the cupbearer of the gods, tasked with filling their cups with the nectar of immortality. Ganymede's parents were devastated by their son's disappearance, so Zeus created the constellation Aquarius to comfort them, reminding them of their son.<br><br>

    <strong>Highlights:</strong><br><br>
    🌊 Ganymede is abducted by Zeus due to his beauty.<br><br>
    🍷 He becomes the cupbearer of the gods.<br><br>
    🌌 Ganymede is placed in the sky as the constellation Aquarius.<br><br>

    <strong>Key Insights:</strong><br><br>
    🌊 <strong>Service</strong>: Aquarius symbolizes selfless service and duty.<br><br>
    🍷 <strong>Honor</strong>: Ganymede’s abduction reflects how divine favor can elevate even the most ordinary mortal.<br><br>
    🌌 <strong>Immortality</strong>: His placement among the stars shows how selfless service is honored for eternity.
    `,

    pisces: `
    The sign of Pisces is symbolized by two fish, representing the gods of love, Passions, Eros, and Aphrodite. When the powerful monster Typhon defeated Zeus, many gods fled Olympus, including Aphrodite and her son Eros. To escape, they transformed themselves into fish and swam to Egypt, where their divinity was recognized. Their escape was inscribed in the stars as the constellation of Pisces.<br><br>

    <strong>Highlights:</strong><br><br>
    🐟 Aphrodite and Eros transform into fish to flee from Typhon.<br><br>
    🌊 They swim to safety in the river Euphrates.<br><br>
    🌌 They are immortalized as the constellation Pisces.<br><br>

    <strong>Key Insights:</strong><br><br>
    🐟 <strong>Adaptability</strong>: Pisces represents the power of transformation and quick thinking in the face of danger.<br><br>
    🌊 <strong>Escape</strong>: The story emphasizes how survival sometimes requires retreat.<br><br>
    🌌 <strong>Duality</strong>: The two fish represent the duality of existence, balancing between the physical and spiritual realms.
    `,
    sagittarius: `
    The sign of Sagittarius is symbolized by a centaur with a pointed bow, representing Chiron, the wisest of the centaurs and a great trainer of heroes like Achilles and Jason. Chiron was accidentally wounded by Hercules and, although immortal, suffered great pain. He chose to die and was transformed into the constellation Sagittarius. Chiron's wisdom and heroic deeds were forever etched into the stars.<br><br>

    <strong>Highlights:</strong><br><br>
    🏹 Chiron is a wise centaur and teacher.<br><br>
    💫 He trains great heroes like Achilles and Jason.<br><br>
    🌌 Chiron is immortalized as the constellation Sagittarius.<br><br>

    <strong>Key Insights:</strong><br><br>
    🏹 <strong>Wisdom and Guidance</strong>: Chiron symbolizes the importance of mentorship and learning.<br><br>
    🌌 <strong>Immortality through Teaching</strong>: His legacy continues through the heroes he trained.<br><br>
    💫 <strong>Legacy</strong>: Sagittarius shows how wisdom and teaching endure through time, creating lasting change.
`
};

// Function to make a color slightly darker
function darkenColor(color, percent) {
    const rgb = color.match(/\d+/g); // Extract the RGB values
    const r = Math.max(0, Math.min(255, parseInt(rgb[0]) - (255 * percent / 100)));
    const g = Math.max(0, Math.min(255, parseInt(rgb[1]) - (255 * percent / 100)));
    const b = Math.max(0, Math.min(255, parseInt(rgb[2]) - (255 * percent / 100)));
    return `rgb(${r}, ${g}, ${b})`;
}
function toggleAudio() {
    const audioPlayer = document.getElementById('audioPlayer');
    const audioButton = document.querySelector('.audio-button i');

    if (audioPlayer.paused) {
        audioPlayer.play();
        audioButton.classList.remove('fa-volume-up');
        audioButton.classList.add('fa-volume-mute');
    } else {
        audioPlayer.pause();
        audioButton.classList.remove('fa-volume-mute');
        audioButton.classList.add('fa-volume-up');
    }
}


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
    luckyColorItem.querySelector('.lucky-circle').style.color = darkenColor(data.lucky_color_rect_color, 60); // Darken the text color
    luckyColorItem.querySelector('.lucky-label').style.color = darkenColor(data.lucky_color_rect_color, 60); // Darken the label color

    const luckyNumberItem = document.querySelector('.lucky-info-container .lucky-item:nth-child(2)');
    luckyNumberItem.querySelector('.lucky-circle').innerText = data.lucky_number; // Update text inside the circle
    luckyNumberItem.style.backgroundColor = data.lucky_number_rect_color; // Update background color
    luckyNumberItem.querySelector('.lucky-circle').style.color = darkenColor(data.lucky_number_rect_color, 60); // Darken the text color
    luckyNumberItem.querySelector('.lucky-label').style.color = darkenColor(data.lucky_number_rect_color, 60); // Darken the label color

    const matchingSignItem = document.querySelector('.lucky-info-container .lucky-item:nth-child(3)');
    matchingSignItem.querySelector('.lucky-circle').innerText = data.matching_sign; // Update text inside the circle
    matchingSignItem.style.backgroundColor = data.matching_sign_rect_color; // Update background color
    matchingSignItem.querySelector('.lucky-circle').style.color = darkenColor(data.matching_sign_rect_color, 60); // Darken the text color
    matchingSignItem.querySelector('.lucky-label').style.color = darkenColor(data.matching_sign_rect_color, 60); // Darken the label color

// Use template literals and ensure url() is properly wrapped in backticks
    document.querySelector('.horoscope-container').style.backgroundImage = `url('/static/${data.image_path}')`;
    document.body.style.backgroundImage = `url('/static/${data.image_path}')`;

}

document.querySelectorAll('.calendar-item').forEach(item => {
    item.addEventListener('click', function (event) {
        event.preventDefault();  // Prevent full page reload

        const selectedDay = this.getAttribute('data-day');
        const titleText = document.title;
        const sign = titleText.split(' ')[0].toLowerCase(); // Assuming the title starts with the zodiac sign


        // If 'Story' is selected, display dynamic content based on the zodiac sign
        if (selectedDay === 'story') {
            const story = zodiacStories[sign] || "The story for this zodiac sign is not available.";
            const videoData = zodiacVideos[sign];

            // Hide horoscope containers
            document.querySelector('.lucky-info-container').style.display = 'none';
            document.querySelector('.rating-container').style.display = 'none';
            document.querySelector('.characteristics-container').style.display ='none';
            document.querySelector('.message-container').style.display = 'block';
            document.querySelector('.date-container').style.display = 'block';

            // Show the story content
            document.querySelector('.horoscope-message').innerHTML = story;
            document.querySelector('.date').innerHTML = videoData.title.replace('(', '<br>(');

            if (videoData) {
                document.getElementById('player-container').style.display = 'block';
                loadYouTubeVideo(videoData.videoId, videoData.startTime);  // Call function to load video
            } else {
                document.getElementById('player-container').style.display = 'none';
            }
        }else if (selectedDay === 'characteristics') {
            stopYouTubeVideo();
            // Fetch the JSON file with zodiac characteristics
            fetch('/static/horoscope-json/zodiacCharacteristics.json')
                .then(response => response.json())
                .then(data => {
                    const characteristics = data[sign] || "Characteristics for this zodiac sign are not available.";
                    
                    // Hide other horoscope content
                    document.querySelector('.lucky-info-container').style.display = 'none';
                    document.querySelector('.rating-container').style.display = 'none';
                    document.querySelector('.story-container').style.display = 'none'; // Hide story container
                    document.querySelector('.message-container').style.display = 'none';
                    document.querySelector('.date-container').style.display = 'none';
                    document.getElementById('player-container').style.display = 'none';
                    
                    // Show characteristics content
                    document.querySelector('.characteristics-container').style.display = 'block';
                    document.querySelector('#horoscope-characteristics').innerHTML = `
                        <strong>Element:</strong> ${characteristics.element || 'Unknown'}<br><br>
                        <strong>Ruling Planet:</strong> ${characteristics.rulingPlanet || 'Unknown'}<br><br>
                        <strong>Positive Traits:</strong> ${characteristics.positiveTraits || 'Unknown'}<br><br>
                        <strong>Negative Traits:</strong> ${characteristics.negativeTraits || 'Unknown'}<br><br>
                        <strong>Compatible Signs:</strong> ${characteristics.compatibleSigns || 'Unknown'}<br><br>
                        <strong>Description:</strong> ${characteristics.description || 'Unknown'}
                    `;
                })
                .catch(error => console.error('Error fetching zodiac characteristics:', error));
        } else {
            const url = this.href;  // Get the URL for the selected day

            // Fetch the horoscope data for the selected day
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    // Update the content with the new horoscope data
                    updateHoroscope(data);

                    // Show lucky info and rating containers again when a horoscope is selected
                    document.querySelector('.lucky-info-container').style.display = 'flex';
                    document.querySelector('.rating-container').style.display = 'block';
                    document.querySelector('.characteristics-container').style.display ='none';
                    document.querySelector('.date-container').style.display = 'block';
                    document.querySelector('.message-container').style.display = 'block';

                    // Hide the YouTube player and clear the video
                    document.getElementById('player-container').style.display = 'none';
                    stopYouTubeVideo();  // Call function to stop video
                })
                .catch(error => console.error('Error fetching horoscope:', error));
        }

        // Set the active state for Story
        document.querySelectorAll('.calendar-item').forEach(el => el.classList.remove('active'));
        this.classList.add('active');
    });
});

// Function to load a YouTube video by setting the src attribute dynamically
function loadYouTubeVideo(videoId, startTime) {
    document.getElementById('player').src = `https://www.youtube.com/embed/${videoId}?start=${startTime}`;
}

// Function to stop the YouTube video by clearing the src attribute
function stopYouTubeVideo() {
    document.getElementById('player').src = '';
}
