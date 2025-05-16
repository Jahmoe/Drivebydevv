async function predictVehicle() {
    const fileInput = document.getElementById("imageUpload").files[0];
    const loadingElement = document.getElementById("loading");
    const resultElement = document.getElementById("result");
    const previewElement = document.getElementById("preview");

    // Check if a file is selected
    if (!fileInput) {
        alert("Please upload an image.");
        return;
    }

    // Display the preview of the uploaded image
    const reader = new FileReader();
    reader.onload = function (e) {
        previewElement.src = e.target.result;
        previewElement.style.display = "block";
    };
    reader.readAsDataURL(fileInput);

    // Show loading message
    loadingElement.style.display = "block";
    resultElement.innerText = "Processing...";

    try {
        const formData = new FormData();
        formData.append("file", fileInput);

        // Fetch prediction from backend
        const response = await fetch("/predict", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Prediction failed.");
        }

        const data = await response.json();
        if (data.prediction) {
            resultElement.innerText = "Predicted: " + data.prediction;
        } else if (data.error) {
            resultElement.innerText = "Error: " + data.error;
        } else {
            resultElement.innerText = "Unexpected response.";
        }
    } catch (error) {
        console.error("Error during prediction:", error);
        resultElement.innerText = "Error: " + error.message;
    } finally {
        // Hide loading message
        loadingElement.style.display = "none";
    }
}

document.getElementById("imageUpload").addEventListener("change", predictVehicle);
