document.addEventListener('DOMContentLoaded', function() {
    var links = document.querySelectorAll('a[data-post-click-location="comments-button"]');
    links.forEach(function(link) {
        link.addEventListener('click', function() {
            NProgress.start();
        });
    });

    window.addEventListener('load', function() {
        NProgress.done();
    });

    // Optional: Handle AJAX navigation if you use it
    document.addEventListener('pjax:send', function() {
        NProgress.start();
    });
    document.addEventListener('pjax:complete', function() {
        NProgress.done();
    });
});

// Evénement permettant de soumettre le formulaire de commentaire sans recharger la page.
// Il utilise AJAX

document.getElementById('comment-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Empêche la soumission du formulaire traditionnelle

    const form = event.target;
    const formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        const messageDiv = document.getElementById('message');
        if (data.success) {
            messageDiv.innerText = 'Commentaire soumis avec succès';
            messageDiv.classList.add('text-green-500');
            document.getElementById('comment-textarea').value = '';
        } else {
            messageDiv.innerText = 'Une erreur s\'est produite: ' + data.message;
            messageDiv.classList.add('text-red-500');
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        const messageDiv = document.getElementById('message');
        messageDiv.innerText = 'Une erreur s\'est produite lors de la soumission du commentaire.';
        messageDiv.classList.add('text-red-500');
    });
});
