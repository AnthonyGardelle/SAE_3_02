console.log("admin.js loaded");

function togglePopup(id) {
    let popup = document.getElementById("popup-overlay-" + id);

    if (popup) {
        popup.classList.toggle("open");
    } else {
        console.error('Popup not found with ID: ' + id);
    }
}

function validateForm(groupeId) {
    // Récupérer les valeurs des champs
    var hebergement = document.getElementById(groupeId + '_hebergement').value;

    // Vérifier si les champs sont vides
    if (hebergement == "") {
        alert("Veuillez specifiez un hebergement.");
        return false; // Empêcher l'envoi du formulaire
    }

    return true; // Autoriser l'envoi du formulaire
}