from src import app
from src.feed_routes import feed_bp, socketio
from src.inscription_routes import inscription_bp
from src.auth_routes import auth_bp
from src.user_session_routes import user_session_bp
from src.post_routes import post_bp
from src.commentaire_routes import commentaire_bp
from src.admin_routes import admin_bp


# Après avoir défini un Blueprint, vous devez l'enregistrer dans votre application Flask principale
app.register_blueprint(feed_bp, url_prefix='/feed')
app.register_blueprint(inscription_bp, url_prefix='/inscription')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_session_bp, url_prefix='/user')
app.register_blueprint(post_bp, url_prefix='/post')
app.register_blueprint(commentaire_bp, url_prefix='/commentaire')
app.register_blueprint(admin_bp, url_prefix='/admin')


if __name__ == "__main__":
    app.run()
    socketio.run(app)
    
