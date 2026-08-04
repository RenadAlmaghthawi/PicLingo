const inputTxt = document.getElementById("caption");
const image = document.getElementById("image");
const button = document.getElementById("btn");
const loading = document.getElementById("loading");
const errorAlert = document.getElementById("error-alert");
const Fav_button = document.getElementById("Fav_button");
const category = document.getElementById("category");
const sucAlert = document.getElementById("sucsses_alert");





async function query() {
    const response = await fetch(
        "https://router.huggingface.co/hf-inference/models/runwayml/stable-diffusion-v1-5",
        {
            headers: { Authorization: `Bearer ${token}` },
            method: "POST",
            body: JSON.stringify({"inputs": inputTxt.value}),
        }
    );
    const result = await response.blob();
    return result;
}

button.addEventListener('click', async function(){
    const text = inputTxt.value.trim();
    
    // Validate input
    if (text.length < 2) {
        showError("Please enter at least 2 characters.");
        return;
    }
    
    // Check if input contains non-English characters
    const regex = /^[a-zA-Z\s]*$/; // Regular expression to match only English characters and spaces
    if (!regex.test(text)) {
        showError("Please enter an English sentence.");
        return;
    }
    
    // Hide any previous error messages
    hideError();
    hideSucsses();
    
    // Show loading spinner
    loading.style.display = "block";
    // Hide image
    image.style.display = "none";

//////////////////// Send caption and Image to the backend (Flask) ///////////////////////////



///////////////////////////////////////////////////////////////////////////////////////////////


    query().then((response) => {
        const objectURL = URL.createObjectURL(response);
        image.onload = function() {
            // Hide loading spinner when image is loaded
            loading.style.display = "none";
            // Show image
            image.style.display = "block";
						buttons.style.display = "block";
        };
        image.src = objectURL;
    });
});

function showError(message) {
    // Set error message
    errorAlert.textContent = message;
    // Show error alert
    errorAlert.style.display = "block";
}

function hideError() {
    // Hide error alert
    errorAlert.style.display = "none";
}

function showSucsses(message) {
    // Set error message
    sucAlert.textContent = message;
    // Show error alert
    sucAlert.style.display = "block";
}

function hideSucsses() {
    // Hide error alert
    sucAlert.style.display = "none";
}



// Function to download the image
function downloadImage() {
	// Check if the image source is empty
	if (!image.src || image.src === "") {
			console.error("Image source is empty.");
			return;
	}

	// Create an anchor element
	const anchor = document.createElement("a");
	// Set the href attribute to the image source
	anchor.href = image.src;
	// Set the download attribute to specify the filename for the downloaded file
	anchor.download = "generated_image.png";
	// Programmatically trigger a click event on the anchor element
	anchor.click();
}

// Add event listener to the download button
document.getElementById("downloadBtn").addEventListener("click", downloadImage);

/////////////////////////////////////////////////

function addToFavorite(){
    
    query().then((response) => {
        const formData = new FormData();
        formData.append('caption', inputTxt.value);  // Add caption to form data
        formData.append('image', response);  // Add image to form data
        formData.append('category', category.value);

        fetch('/auth/save-image', {
            method: 'POST',
            body: formData
        }).then(response => {
            if (!response.ok) {
                throw new Error('Failed to save image');
            }else{
                showSucsses("Image saved in your favorite list!")
            }
        }).catch(error => {
            showError('Error: ' + error.message);
        }).finally(() => {
            loading.style.display = "none";
            image.style.display = "block";
        });
    });

}
document.getElementById("Fav_button").addEventListener("click", addToFavorite);