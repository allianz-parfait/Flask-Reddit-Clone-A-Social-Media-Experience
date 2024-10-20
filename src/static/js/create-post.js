document.addEventListener("DOMContentLoaded", function() {
    // Sélectionnez le champ de fichier et le bouton d'ajout de média
    var mediaField = document.querySelector("#media-form input[name='media']");
    var addMediaButton = document.getElementById("add-media-button");
    
    // Fonction pour créer un champ de fichier temporaire
    function createTempFileInput() {
        var tempInput = document.createElement("input");
        tempInput.type = "file";
        tempInput.accept = "image/*,video/*";
        tempInput.className = "hidden";
        tempInput.onchange = function() {
            // Copier le fichier sélectionné vers le champ de fichier du formulaire
            if (tempInput.files.length > 0) {
                mediaField.files = tempInput.files;
                previewMedia(mediaField);
            }
        };
        document.body.appendChild(tempInput);
        return tempInput;
    }

    // Ajouter un écouteur d'événement au bouton d'ajout de média
    addMediaButton.addEventListener("click", function(event) {
        event.preventDefault(); // Empêcher le comportement par défaut du bouton
        var tempFileInput = createTempFileInput();
        tempFileInput.click(); // Déclencher le clic sur le champ de fichier temporaire
    });

    // Ajouter un écouteur d'événement au champ de fichier pour afficher le fichier sélectionné
    mediaField.addEventListener("change", function() {
        // Code pour prévisualiser le fichier sélectionné
        var container = document.getElementById("media-container");
        container.innerHTML = ''; // Clear previous content
        previewMedia(mediaField);
    });
});

// Fonction pour prévisualiser le média sélectionné
function previewMedia(input) {
    var file = input.files[0];
    if (file) {
        var reader = new FileReader();
        reader.onload = function() {
            var mediaContainer = document.getElementById("media-container");
            var mediaPreview = document.createElement("div");
            mediaPreview.className = "relative flex justify-center items-center bg-gray-200 rounded-lg";
            var mediaType = file.type.split("/")[0];
            if (mediaType === "image") {
                mediaPreview.innerHTML = '<img src="' + reader.result + '" alt="File preview" class="w-full object-cover h-40 rounded-lg">';
            } else if (mediaType === "video") {
                mediaPreview.innerHTML = '<video src="' + reader.result + '" class="w-full h-40 rounded-lg" controls></video>';
            }
            // Ajout du bouton de suppression
            var deleteButton = document.createElement("button");
            deleteButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 absolute top-1 right-1 text-red-500 cursor-pointer" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M6.293 6.293a1 1 0 0 1 1.414 1.414L10 11.414l2.293-2.293a1 1 0 1 1 1.414 1.414L11.414 12l2.293 2.293a1 1 0 1 1-1.414 1.414L10 13.414l-2.293 2.293a1 1 0 0 1-1.414-1.414L8.586 12 6.293 9.707a1 1 0 0 1 0-1.414z"/></svg>';
            deleteButton.onclick = function() {
                mediaContainer.removeChild(mediaPreview);
                input.value = ''; // Réinitialisation de l'entrée de fichier
            };
            mediaPreview.appendChild(deleteButton);
            mediaContainer.appendChild(mediaPreview);
        };
        reader.readAsDataURL(file);
    }
}

// Fonction pour afficher l'onglet sélectionné
function showTab(event, tabId) {
    var tabContent = document.getElementsByClassName("tab-content");
    for (var i = 0; i < tabContent.length; i++) {
        tabContent[i].style.display = "none";
    }
    var tabLinks = document.getElementsByClassName("tab-link");
    for (var i = 0; i < tabLinks.length; i++) {
        tabLinks[i].className = tabLinks[i].className.replace(" border-b-2 border-gray-200", "");
    }
    document.getElementById(tabId).style.display = "block";
    event.currentTarget.className += " border-b-2 border-gray-200";
}

// Écouteur d'événement pour afficher l'onglet sélectionné
document.addEventListener("click", function(event) {
    if (event.target.classList.contains("tab-link")) {
        var tabId = event.target.getAttribute("data-tab");
        showTab(event, tabId);
    }
});

// Sélectionner l'onglet "Post" par défaut au chargement de la page
document.addEventListener("DOMContentLoaded", function() {
    document.querySelector(".tab-link:first-child").click();
});
