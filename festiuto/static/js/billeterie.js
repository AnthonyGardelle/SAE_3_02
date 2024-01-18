console.log("billeterie.js loaded");

function togglePopup(id) {
    let popup = document.getElementById("popup-overlay-" + id);

    if (popup) {
        popup.classList.toggle("open");
    } else {
        console.error('Popup not found with ID: ' + id);
    }
}

function validateForm(typeBilletId) {
    // Récupérer les valeurs des champs
    var nom = document.getElementById(typeBilletId + '_nom').value;
    var prenom = document.getElementById(typeBilletId + '_prenom').value;
    var mail = document.getElementById(typeBilletId + '_mail').value;
    var dateDebut = document.getElementById(typeBilletId + '_date_debut').value;

    console.log("nom: " + nom);
    console.log("prenom: " + prenom);
    console.log("mail: " + mail);
    console.log("dateDebut: " + dateDebut);

    // Vérifier si les champs sont vides
    if (nom === "" || prenom === "" || mail === "" || dateDebut === "") {
        alert("Veuillez remplir tous les champs du formulaire.");
        return false; // Empêcher l'envoi du formulaire
    }

    return true; // Autoriser l'envoi du formulaire
}