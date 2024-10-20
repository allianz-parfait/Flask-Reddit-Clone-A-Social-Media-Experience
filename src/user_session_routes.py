from flask import Blueprint, render_template
from flask_login import LoginManager, current_user, login_required

from .models import User, login_manager

user_session_bp = Blueprint('user_session', __name__)


# Avec Flask Login plus besoin d'utiliser les sessions car elles sont peu sécurisés et adopte des 
# méthodes fastidieuses tandis que Flask Login permet de gérer plus facilement les sessions grace à
# des méthodes prédéfinis


# Récupérer l'utilisateur connecté
# Cette méthode prend en paramètre l'id de l'utilisateur connecté puis le recherche et le récupère en BD
# NB : Il faut toujours le décorer de 'user_loader' qui permet de récupérer le user connecté
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@user_session_bp.route('/see-profile')
@login_required
def see_profile():
    return render_template('client/user.profile.html', user=current_user)

# @user_session_bp.route('/')
# def render_logged_user():
    
# @user_session_bp.route('/profile')
# def profile():
#     return current_user
# @user_session_bp.route('/')
# def index():
#     if current_user.is_au
# Cette fonction, load_logged_in_user(), est un before_request handler qui est exécutée avant chaque 
# requête entrante dans l'application.
# Elle récupère l'identifiant de l'utilisateur connecté à partir de la session

# 'g' est un objet global dans Flask qui est utilisé pour stocker des données spécifiques à la requête
# en cours. Il est souvent utilisé pour stocker des informations telles que l'utilisateur connecté, 
# la base de données actuellement utilisée, etc.
# @user_session_bp.before_app_request
# def load_logged_in_user():
#     user_id = session.get('connectedUser')
#     g.user = User.query.get(user_id) if user_id else None



# Cette fonction, inject_user(), est un context processor qui ajoute des variables au contexte de rendu 
# Jinja pour chaque template rendu.
# Elle retourne un dictionnaire contenant les variables que vous souhaitez injecter dans le contexte 
# Jinja. Ici, elle injecte l'utilisateur connecté (g.user) sous le nom user.
# Ainsi, dans vos templates Jinja, vous aurez accès à la variable user contenant l'utilisateur connecté.

# @user_session_bp.context_processor
# def inject_user():
#     return dict(user=g.user)

# print(inject_user())