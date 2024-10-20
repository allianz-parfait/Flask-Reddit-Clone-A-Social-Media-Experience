from flask import Flask, Blueprint, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user

# from .feed_routes import app
from .models import User, login_manager
from .forms import LoginForm # Pour gérer les formulaires
    

auth_bp = Blueprint('auth', __name__)

# Cette méthode va nous envoyer vers le formulaire d'inscription
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm() # On instancie un Objet de la classe InscriptionForm
    if form.validate_on_submit(): # Si on soumet le formulaire
        # On récupère les données de chaque champs
        email = form.email.data
        pwd = form.password.data
        
        # Rechercher si l'utilisateur existe dans la base de données
        user = User.query.filter_by(email=email).first()
        
        # Si on trouve un user en BD et que son mdp correspond à celui saisi
        if user and user.check_password(pwd) and user.isActive == True:
            # On le connecte grace à 'login_user' qui est une méthode de Flask-Login. 
            # Ce qui l'ajoute aussi à la session
            login_user(user)
            print(f"Connected : {login_user(user)}")

            return redirect(url_for('feed.feedPage'))
        else:
            # Informer l'utilisateur que les informations de connexion sont incorrectes
            flash('Adresse e-mail ou mot de passe incorrect. Veuillez réessayer.', 'danger')
            return redirect(url_for('auth.login'))
        
        
    return render_template('client/login.html', form=form) # Puis on le passe au template
    # return redirect('client/inscription.html')
    
# @login_bp.route('/')
# def index():
    
@auth_bp.route('/logout')
def logout():
    logout_user() # On supprime l'utilisateur de la session (on le déconnecte)
    print(f"Disconnected : {logout_user()}")
    return redirect(url_for('feed.feedPage')) # Et on le redirige vers la page de connexion


# 'login_manager.login_view' est une propriété de configuration de l'objet LoginManager dans Flask-Login
# Cette propriété permet de spécifier le nom de la vue à laquelle les utilisateurs seront redirigés 
# lorsqu'ils tentent d'accéder à une route protégée sans être connectés
login_manager.login_view = "auth.login"