const toggleButton = document.getElementById('toggleButton');
const transcriptionOutput = document.getElementById('transcription');

const caption = document.getElementById('caption').textContent;
var Robot_image =document.getElementById('robot_image_tell');

const try_button = document.getElementById('try_button');

const successAlert = document.getElementById('successAlert');
const errorAlert = document.getElementById('errorAlert');

let recognition;

toggleButton.addEventListener('click', () => {
    if (toggleButton.textContent.trim() === "Start Talking") {
        toggleButton.innerHTML = '<i class="bi bi-mic-mute"></i> Stop Talking';
        Robot_image.src="static/images/robot_listen.svg"
        startRecording();
    } else {
        toggleButton.innerHTML = '<i class="bi bi-mic"></i> Start Talking';
        stopRecording();
    }
});

function startRecording() {
    transcriptionOutput.textContent = '';
    // Reinitialize the recognition object
    recognition = new window.webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    // Set up event handlers
    recognition.onresult = async (event) => {
        const audioContent = event.results[0][0].transcript;
        transcriptionOutput.textContent = audioContent;

        // Send audio content to the server for transcription
        const response = await fetch('/transcribe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ audioContent })
        });

        const data = await response.json();
        console.log(data.transcription);
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
    };

    recognition.onend = () => {
        const similarityScore = computeCosineSimilarity(transcriptionOutput.textContent, caption);
        redirectBasedOnSimilarity(similarityScore);
    };

    // Start speech recognition
    recognition.start();
}


function stopRecording() {
    if (recognition) {
        recognition.stop();
    }
}

// Function to compute cosine similarity
function computeCosineSimilarity(sentence1, sentence2) {
    // This part of the code is the same as your Python function
    const words1 = preprocessText(sentence1);
    const words2 = preprocessText(sentence2);

    const vector1 = createWordFrequencyVector(words1);
    const vector2 = createWordFrequencyVector(words2);

    const dotProduct = computeDotProduct(vector1, vector2);
    const magnitude1 = computeMagnitude(vector1);
    const magnitude2 = computeMagnitude(vector2);

    const similarity = dotProduct / (magnitude1 * magnitude2);

    return similarity;
}

function preprocessText(text) {
    return text.toLowerCase().split(/[^\w']+/).filter(Boolean);
}

function createWordFrequencyVector(words) {
    return words.reduce((acc, word) => {
        acc[word] = (acc[word] || 0) + 1;
        return acc;
    }, {});
}

function computeDotProduct(vector1, vector2) {
    return Object.keys(vector1).reduce((acc, key) => {
        if (key in vector2) {
            acc += vector1[key] * vector2[key];
        }
        return acc;
    }, 0);
}

function computeMagnitude(vector) {
    return Math.sqrt(Object.values(vector).reduce((acc, val) => acc + val * val, 0));
}

function resetPage() {
    // Reset the toggleButton text and image
    toggleButton.innerHTML = '<i class="bi bi-mic"></i> Start Talking';

    // Reset the Robot_image source
    Robot_image.src = "static/images/robot_tell.svg";

    // Reset the transcription output
    transcriptionOutput.textContent = '';

    // Hide the success and error alerts
    successAlert.style.display = 'none';
    errorAlert.style.display = 'none';
    try_button.style.display = 'none' ; 
}


// Function to hide success alert after a specified delay
function hideSuccessAlert() {
    successAlert.style.display = 'none';
}

// Function to hide error alert after a specified delay
function hideErrorAlert() {
    errorAlert.style.display = 'none';
}

// Function to redirect user based on similarity score
function redirectBasedOnSimilarity(similarityScore) {
    const threshold = 0.3;

    if (similarityScore >= threshold) {
        Robot_image.src = "static/images/congrats_robot.svg";
        successAlert.style.display = 'block';
        try_button.style.display = 'none' ; 
        // Hide success alert after 5 seconds 
        setTimeout(hideSuccessAlert, 8000);

    } else {
        Robot_image.src = "static/images/robot_tryAgain.svg";
        errorAlert.style.display = 'block';
        try_button.style.display = 'block' ; 
        // Hide error alert after 5 seconds 
        setTimeout(hideErrorAlert, 8000);
    }
}


try_button.addEventListener('click', resetPage);