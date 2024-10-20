document.addEventListener('DOMContentLoaded', () => {
    // Fonction pour afficher les messages
    const messageContainer = document.getElementById('message-container');
    function showMessage(message, isSuccess) {
      if (messageContainer) {
        messageContainer.textContent = message;
        messageContainer.className = `p-4 rounded ${isSuccess ? 'bg-green-500 text-white' : 'bg-red-500 text-white'} mt-4`;
        messageContainer.classList.remove('hidden');
      }
    }
  
    // Fonction pour mettre à jour le statut de l'utilisateur
    function updateUserStatus(userId, isActive) {
        const statusElement = document.getElementById(`status-${userId}`);
        if (statusElement) {
        statusElement.className = `w-6 h-6 ${isActive ? 'bg-green-500' : 'bg-red-500'} rounded-full mr-2`;
        const statusText = document.querySelector(`#status-${userId} + p`);
        if (statusText) {
            statusText.className = isActive ? 'text-green-500 font-semibold' : 'text-red-500 font-semibold';
            statusText.textContent = isActive ? 'Active' : 'Inactive';
        }
        }
    }

    // Gestion des actions de l'utilisateur (bloquer/débloquer)
    async function handleUserAction(event, action) {
      const userId = event.target.dataset.userId;
      try {
        const response = await fetch(`/admin/dashboard/user/${userId}/${action}`, { method: 'POST' });
        const result = await response.json();
        if (response.ok) {
          showMessage(result.message, true);
          updateUserStatus(userId, action === 'unblock-user');
        } else {
          showMessage(result.message, false);
        }
      } catch (error) {
        showMessage('Une erreur est survenue lors du traitement de la demande.', false);
      }
    }
  
    // Ajouter des écouteurs d'événements pour les boutons de blocage et de déblocage s'ils existent
    const blockUserBtn = document.querySelector('.block-user-btn');
    if (blockUserBtn) {
      blockUserBtn.addEventListener('click', (event) => {
        handleUserAction(event, 'block-user');
      });
    }
  
    const unblockUserBtn = document.querySelector('.unblock-user-btn');
    if (unblockUserBtn) {
      unblockUserBtn.addEventListener('click', (event) => {
        handleUserAction(event, 'unblock-user');
      });
    }
  
    // Code existant pour la fonctionnalité de suppression d'utilisateur
    document.querySelectorAll('.delete-btn').forEach(button => {
      button.addEventListener('click', async (event) => {
        event.preventDefault();
        const userId = button.closest('form').dataset.userId;
        const form = button.closest('form');
        
        try {
          const response = await fetch(`/admin/dashboard/user/${userId}/remove`, {
            method: 'DELETE'
          });
          
          if (!response.ok) {
            throw new Error('La réponse réseau n\'était pas correcte');
          }
    
          // Supprimer la ligne de l'utilisateur du tableau
          document.getElementById(`user-${userId}`).remove();
        } catch (error) {
          console.error('Il y a eu un problème avec l\'opération fetch :', error);
          // Revenir à la soumission du formulaire si fetch échoue
          form.submit();
        }
      });
    });
  });
  