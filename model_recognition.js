// Vehicle Make and Model Recognition Script

async function predictVehicle() {
    const fileInput = document.getElementById("imageUpload").files[0];
    if (!fileInput) {
        alert("Please upload an image.");
        return;
    }

    const reader = new FileReader();
    reader.onload = async function (event) {
        const imgElement = document.getElementById("preview");
        imgElement.src = event.target.result;
        imgElement.style.display = "block";

        // Show loading animation
        const loadingElement = document.getElementById("loading");
        loadingElement.style.display = "block";

        try {
            const formData = new FormData();
            formData.append("image", fileInput);

            const response = await fetch("http://localhost:5000/vehicle_detection_api", {
                method: "POST",
                body: formData
            });

            if (!response.ok) throw new Error("Prediction failed.");

            const data = await response.json();
            document.getElementById("result").innerText = "Predicted: " + data.prediction;
        } catch (error) {
            console.error("Error:", error);
            document.getElementById("result").innerText = "Error in prediction.";
        } finally {
            loadingElement.style.display = "none";
        }
    };
    reader.readAsDataURL(fileInput);
}

// Auto-trigger prediction when an image is uploaded
document.getElementById("imageUpload").addEventListener("change", predictVehicle);
