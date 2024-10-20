document.querySelectorAll('a, button').forEach(function(el) {
    el.addEventListener('mouseover', function() {
    let tooltip = el.querySelector('.absolute');
    if (tooltip) { // S'assure que l'élément existe avant de tenter de modifier sa classe
        tooltip.classList.remove('hidden');
    }
    });
    el.addEventListener('mouseout', function() {
    let tooltip = el.querySelector('.absolute');
    if (tooltip) {
        tooltip.classList.add('hidden');
    }
    });
});


// document.addEventListener('DOMContentLoaded', function() {
//     var socket = io.connect('http://127.0.0.1:5000');

//     socket.on('connect', function() {
//         console.log('Connected');
//     });

//     socket.on('message', function(data) {
//         console.log('Message received: ' + data);
//         var messageContainer = document.getElementById('messageContainer');
//         if (messageContainer) {
//             messageContainer.innerHTML += '<p>' + data + '</p>';
//         } else {
//             console.error('Element with ID "messageContainer" not found');
//         }
//     });

//     document.getElementById('messageForm').addEventListener('submit', function(event) {
//         event.preventDefault(); // Prevent default form submission
//         sendMessage(); // Call sendMessage function when form is submitted
//     });

//     function sendMessage() {
//         var message = document.getElementById('messageInput').value;
//         socket.emit('message', message);
//         document.getElementById('messageInput').value = ''; // Clear input field after sending message
//     }
// });
