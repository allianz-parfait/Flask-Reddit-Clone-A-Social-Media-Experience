# C'est ici que je teste mes Fonctions et Objets

# from .models import User

# users = User.findAll()
# for usr in users:
#     print(usr.__repr__)
    
# from .models import User, Video, Photo, Post

# # Création d'un nouvel utilisateur
# user = User("Ayra", "Star", "+221763560978", "ayra_star", "ayra@gmail.com", "ayramovie")

# # Création d'une nouvelle vidéo associée à un post
# video = Video("https://youtu.be/hykb5RC-DZs?si=CMdbug-5hkSd2oXO")
# "https://youtu.be/EJg_NClKaaE?si=z760vdWv9VQi3jG9"
# video.save()  # Sauvegarde de la vidéo en base de données

# # Création d'un nouveau post associé à l'utilisateur
# post = Post("Chris Brown New Song With Bryson Tyller")
# post.addVideo(video)
# post.author = user  # Associez le post à l'utilisateur
# post.save()  # Sauvegarde du post en base de données

# # Sauvegarde de l'utilisateur en base de données (si nécessaire)
# user.save()

# user = User("Tyler", "McLenan", "+221703900978", "Ty.M", "mclenan@gmail.com", "mclenan2")

# # Création d'une nouvelle vidéo associée à un post
# video = Video("C:/Users/Alliance/3D Objects/reddit/src/static/img/Le dernier bastion de l'humanité - L'Attaque des Titans Saison Finale.mp4")
# video.save()  # Sauvegarde de la vidéo en base de données

# # Création d'un nouveau post associé à l'utilisateur
# post = Post("Attack On Titan Last Movie")
# post.addVideo(video)
# post.author = user  # Associez le post à l'utilisateur
# post.save()  # Sauvegarde du post en base de données

# # Sauvegarde de l'utilisateur en base de données (si nécessaire)
# user.save()


# # Création d'un nouvel utilisateur
# user = User("James", "Nolan", "+221784563780", "j.nol", "nolanjames@gmail.com", "passer@123")

# # Création d'une nouvelle vidéo associée à un post
# photo = Photo("https://media.architecturaldigest.com/photos/63079fc7b4858efb76814bd2/16:9/w_4000,h_2250,c_limit/9.%20DeLorean-Alpha-5%20%5BDeLorean%5D.jpg")
# photo.save()  # Sauvegarde de la vidéo en base de données

# # Création d'un nouveau post associé à l'utilisateur
# post = Post("New Best Car Flow")
# post.addPhoto(photo)
# post.author = user  # Associez le post à l'utilisateur
# post.save()  # Sauvegarde du post en base de données

# # Sauvegarde de l'utilisateur en base de données (si nécessaire)
# user.save()
# from flask import current_app

# import os
# from werkzeug.utils import secure_filename
# from werkzeug.datastructures import FileStorage


# def save_media(file):        
#     # Chemin vers le dossier static de votre projet Flask
#     static_folder = current_app.static_folder

#     # Détermine le dossier de destination en fonction de l'extension du fichier
#     if file.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
#         folder_name = 'img'
#     elif file.filename.lower().endswith(('.mp4')):
#         folder_name = 'videos'
#     else:
#         raise ValueError("Unsupported file format")

#     # Vérifie si le dossier dans static existe, sinon, on le crée
#     media_folder = os.path.join(static_folder, folder_name)
#     os.makedirs(media_folder, exist_ok=True)

#     # Génère un nom de fichier sécurisé
#     filename = secure_filename(file.filename)

#     # Chemin complet du fichier à enregistrer
#     file_path = os.path.join(media_folder, filename)

#     # Copie du fichier dans le dossier img ou videos du dossier static
#     file.save(file_path)

#     # Retourne le chemin relatif du fichier copié
#     return os.path.relpath(file_path, start=static_folder)


# def test_save_media(real_file_path):
#     from .feed_routes import app

#     with app.app_context():
#         # Ouvrir le fichier réel
#         with open(real_file_path, 'rb') as f:
#             file = FileStorage(stream=f, filename=os.path.basename(real_file_path), content_type='video/mp4')

#             static_folder = current_app.static_folder
#             os.makedirs(static_folder, exist_ok=True)

#             try:
#                 saved_path = save_media(file)
#                 expected_path = os.path.join('videos', os.path.basename(real_file_path))
#                 assert saved_path == expected_path, f"Expected path: {expected_path}, but got: {saved_path}"
#                 assert os.path.exists(os.path.join(static_folder, saved_path)), "File not found at expected location"
#                 print("Test passed!")
#             finally:
#                 # Nettoyage
#                 os.system(f'rm -rf {os.path.join(static_folder, "videos")}')


# if __name__ == '__main__':
#     # Chemin d'accès au fichier que vous voulez tester
#     real_file_path = 'C:/Users/Alliance/Downloads/Video/Stories • Instagram.mp4'
#     test_save_media(real_file_path)