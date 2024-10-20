# 🌐 Clone de Reddit avec Flask

Bienvenue dans le clone de Reddit que j'ai développé en utilisant Python et Flask ! 🚀

## 📖 Description

Ce projet est une réplique fonctionnelle du célèbre réseau social Reddit. Les utilisateurs peuvent s'inscrire, se connecter et partager des contenus variés, allant de textes à des images, vidéos, et même des liens YouTube. L'application offre une expérience utilisateur fluide grâce à des fonctionnalités modernes et une interface élégante.

## 🛠️ Technologies Utilisées

- **Python** : Langage de programmation principal.
- **Flask** : Framework web pour Python.
- **JavaScript** : Pour des interactions dynamiques sur la page.
- **Tailwind CSS** : Pour le design et la mise en page.
- **WTForms** : Pour la gestion des formulaires et la validation CSRF.

## 📦 Modèles

Les principaux modèles utilisés dans l'application sont :

- **User** : Représente les utilisateurs du réseau social.
- **Post** : Peut être de type texte, photo ou vidéo.
- **Video** : Modèle pour les vidéos partagées.
- **Photo** : Modèle pour les images.
- **Commentaire** : Pour les commentaires sur les publications.
- **TypePost** : Énumération pour définir le type de post.

## 🔒 Fonctionnalités

### Authentification

- **Inscription** : Permet aux utilisateurs de créer un compte.
- **Connexion** : Permet aux utilisateurs de se connecter à leur compte.
- **Déconnexion** : Les utilisateurs peuvent se déconnecter de leur session.

### Interface Utilisateur

- **Navbar dynamique** : S'adapte en fonction de l'état de connexion de l'utilisateur.
  - Affiche l'avatar et une icône verte en ligne pour les utilisateurs connectés.
  - Affiche un bouton de connexion pour les utilisateurs non connectés.

### Publications

- **Liste des posts** : Affiche les posts avec le temps écoulé depuis leur publication et le nom de l'auteur.
- **Création de posts** :
  - Possibilité de poster des textes, images, vidéos ou des liens YouTube.
  - Visualisation des médias avant publication.

### Gestion des Médias

- **Sélection asynchrone** : Utilisation de JavaScript pour sélectionner plusieurs médias sans recharger la page.

### Interface de Création de Post

- **Formulaire multi-onglets** : Trois onglets pour faciliter la création de posts :
  - Texte
  - Médias
  - YouTube

### Tableau de Bord Admin

- **Gestion des utilisateurs** : Options pour bloquer ou supprimer des comptes utilisateurs.
- **Actions asynchrones** : Les actions admin se font sans recharger la page grâce à JavaScript.

