import re
import os
from flask import current_app
import unicodedata
from werkzeug.utils import secure_filename


# Cette fonction utilise une expression régulière pour vérifier si l'URL fournie est un lien YouTube valide. 
# def is_youtube_video_url(video_url):
#     return 'https://www.youtube.com/embed/' in video_url
def is_embeded_youtube_video_url(video_url):
    pattern = r'^https://www\.youtube\.com/embed/([\w-]+)\?.*$'
    return bool(re.match(pattern, video_url))

def is_youtube_video_valid_url(video_url):
    # Modèle pour correspondre aux liens YouTube spécifiques fournis
    pattern = r'^https?://youtu\.be/[\w\-]+\?si=[\w\-]+$'
    return bool(re.match(pattern, video_url))



# Cette fonction utilise une expression régulière pour extraire l'id unique de l'url Youtube
def extract_video_id(video_url):
    # Modèle regex pour correspondre à l'identifiant de la vidéo YouTube
    pattern = r"(?<=youtu\.be/)[\w-]+"
    match = re.search(pattern, video_url)
    if match:
        return match.group(0)
    else:
        # Gérer le cas où l'URL fournie n'est pas valide
        return None

def clean_filename(filename):
    """
    Normalise la chaîne de caractères Unicode, supprime les caractères spéciaux et remplace les espaces par des underscores.
    Préserve l'extension du fichier.
    """
    name, ext = os.path.splitext(filename)
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    name = re.sub(r'[^\w\s-]', '', name).strip().lower()
    name = re.sub(r'[-\s]+', '_', name)
    return f"{name}{ext}"

def save_media(file):
    # Chemin vers le dossier static de votre projet Flask
    static_folder = current_app.static_folder

    # Détermine le dossier de destination en fonction de l'extension du fichier
    if file.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
        folder_name = 'img'
    elif file.filename.lower().endswith(('.mp4')):
        folder_name = 'videos'
    else:
        raise ValueError("Unsupported file format")

    # Vérifie si le dossier dans static existe, sinon, on le crée
    media_folder = os.path.join(static_folder, folder_name)
    os.makedirs(media_folder, exist_ok=True)

    # Génère un nom de fichier sécurisé et nettoyé
    original_filename = file.filename
    cleaned_filename = clean_filename(original_filename)
    filename = secure_filename(cleaned_filename)

    # Chemin complet du fichier à enregistrer
    file_path = os.path.join(media_folder, filename)

    # Copie du fichier dans le dossier img ou videos du dossier static
    file.save(file_path)

    # Retourne le chemin relatif du fichier copié
    return os.path.relpath(file_path, start=static_folder)


link =is_embeded_youtube_video_url("https://www.youtube.com/embed/M5g91Om0Wlg?autoplay=1")
print("is link : ", link)

print(clean_filename("""Grace notes over Tracy Chapman vibes 🎹  
                     “Fast Car” @tracychapmanonline  These are my kinds of progressions 😌  
                     #piano #pianist #pianomusic #pianolover #pianoplayer #musician 
                     # #beautifulpiano #pianopiano #pianocovers .mp4"""))