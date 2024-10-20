from flask import Flask, render_template, Blueprint, jsonify, request, send_from_directory
from flask_login import LoginManager, current_user
from flask_socketio import SocketIO


app = Flask(__name__)

# Permet de configurer la communication bidirectionnelle entre le navigateur et le serveur en realtime
socketio = SocketIO(app)

app.config.from_pyfile('../config.py')

from .models import Post


feed_bp = Blueprint('feed', __name__)

# Cette méthode va nous envoyer vers la page des feeds
# @feed_bp.route('/')
# def feedPage():
#     posts = Post.findAll()
#     return render_template('client/feed-page.html', posts=posts)

@socketio.on('message')
def handle_message(message):
    print('Message received: ' + message)
    # Traitez le message selon vos besoins
    # Par exemple, vous pouvez le diffuser à tous les clients connectés
    socketio.emit('message', message)

# Cette méthode va nous envoyer vers la page des feeds
@feed_bp.route('/')
def feedPage():
    posts = Post.query.order_by(Post.date_creation.desc()).all() # On trie les posts dans l'ordre du plus récent au plus ancien
    # Vérifiez si la demande est une demande JSON
    if request.is_json:
        # Transformez les publications en un format JSONable
        posts_json = [{
            'id': post.id,
            'titre_post': post.titre_post,
            'photo_profil': post.photo_profil,
            'author': post.author.username,
            'photos': post.photos,
            'videos': post.videos,
            'type' : post.type.name,
            # Ajoutez d'autres champs si nécessaire
        } for post in posts]
        
        # Retournez les publications au format JSON
        return jsonify(posts_json)
    else:
        # On récupère l'utilisateur actuellement connecté, qu'on rend
        user = current_user
        # render_feed_page = render_template('client/feed-page.html', posts=posts)
        # render_navbar_changes = render_template('shared/navbar.html', user=user)
        # Retournez les publications sous forme de rendu HTML
        return render_template('client/feed.page.html', posts=posts, user=user)
    
# @app.route('/video/<path:filename>')
# def serve_video(filename):
#     return send_from_directory('static/videos', filename)