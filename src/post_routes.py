from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from .forms import PostForm, MediaForm, YoutubeForm
from .models import Post, Video, Photo
from .functions import save_media, clean_filename
from .feed_routes import socketio

post_bp = Blueprint('post', __name__)


@post_bp.route('/create-post', methods=['GET', 'POST'])
@login_required # Utilisé pour dire que la route est protégé et qu'on ne pourra y accèder qu'après connexion
def create_post():
    post_form = PostForm()
    media_form = MediaForm()
    youtube_form = YoutubeForm()
        
    if post_form.validate_on_submit():
        titre_post = post_form.titre.data
        content = post_form.content.data
        post = Post(titre_post, content)
        post.author = current_user  # Associez le post à l'utilisateur(ORM)
        post.save()
        return redirect(url_for('post.post_successfull')) # Dès qu'on enregistre, on le redirige vers la age de succès
    
    if not media_form.validate_on_submit():
        print(media_form.errors)
    
    else:
        title = media_form.titre.data # Récupération du champ titre du media
        media = media_form.media.data # Récupération du fichier selectionné
        save_media(media) # Enregistrement du média sélectionné dans le dossier static (img ou videos)
        saved_path = clean_filename(media.filename) # Nouveau nom nettoyé du fichier
         
        if saved_path.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            photo = Photo(saved_path)
            photo.save()
            
        elif saved_path.endswith(('.mp4')):
            video = Video(saved_path) # Création de l'objet Video avec la valeur du lien
            video.save() # Enregistrement de la video youtube en base de données
        
        post = Post(title) # Création de l'objet Post avec comme titre, le champ de titre media
        post.author = current_user  # Associez le post à l'utilisateur(ORM)
        if saved_path.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            post.addPhoto(photo)
        elif saved_path.endswith('.mp4'):
            post.addVideo(video) # Ajout de l'objet youtube_video (Video) dans l'objet Post
        post.save() # Enregistrement du post video youtube en base de données
        
        return redirect(url_for('post.post_successfull')) # Dès qu'on enregistre, on le redirige vers la age de succès

    if youtube_form.validate_on_submit():
        title = youtube_form.titre.data # Récupération du champ titre youtube
        youtube_link = youtube_form.youtube_link.data # Récupération du champ lien youtube
        
        youtube_video = Video(youtube_link) # Création de l'objet Video avec la valeur lien youtube
        youtube_video.save() # Enregistrement de la video youtube en base de données
        
        post = Post(title) # Création de l'objet Post avec comme titre, le champ de titre youtube
        post.addVideo(youtube_video) # Ajout de l'objet youtube_video (Video) dans l'objet Post
        post.author = current_user  # Associez le post à l'utilisateur(ORM)
        post.save() # Enregistrement du post video youtube en base de données
        
        return redirect(url_for('post.post_successfull')) # Dès qu'on enregistre, on le redirige vers la age de succès
    
    return render_template('client/create.post.html', post_form=post_form, media_form=media_form, youtube_form=youtube_form, user=current_user)


# Route qui retourne la page de succès de création de post
@post_bp.route('/post-successfull')
@login_required # Connexion requise pour accéder à cette route
def post_successfull():
    return render_template('client/post.success.page.html')