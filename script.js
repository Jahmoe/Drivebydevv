// Updated JS for Drive by Devs Navigation

// Toggle navigation visibility
const navToggle = document.getElementById('navi-toggle');
const navBackground = document.querySelector('.navigation__background');
const navList = document.querySelector('.navigation__list');

navToggle.addEventListener('change', function () {
  if (navToggle.checked) {
    navBackground.style.transform = 'scale(80)';
    navList.style.opacity = '1';
    navList.style.width = '100%';
  } else {
    navBackground.style.transform = 'scale(1)';
    navList.style.opacity = '0';
    navList.style.width = '0';
  }
});

// Fetch available vehicles from the backend and populate the dropdown
window.onload = async function() {
    const response = await fetch("http://localhost:5000/api/vehicles");
    const vehicles = await response.json();
    const vehicleSelect = document.getElementById("vehicle");
    vehicles.forEach(vehicle => {
        const option = document.createElement("option");
        option.value = vehicle.id;
        option.textContent = `${vehicle.make} ${vehicle.model} - $${vehicle.price}`;
        vehicleSelect.appendChild(option);
    });
};

// Handle form submission
document.getElementById("purchaseForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const vehicleId = document.getElementById("vehicle").value;
    const customerName = document.getElementById("customerName").value;
    const customerEmail = document.getElementById("customerEmail").value;

    if (!vehicleId || !customerName || !customerEmail) {
        alert("Please fill out all fields.");
        return;
    }

    const response = await fetch("http://localhost:5000/api/purchase", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            vehicleId,
            customerName,
            customerEmail
        })
    });

    const result = await response.json();
    document.getElementById("confirmation").innerText = result.message;
});
