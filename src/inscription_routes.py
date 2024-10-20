from flask import Flask, Blueprint, render_template, redirect, url_for
from flask_login import LoginManager, login_required

# from .feed_routes import app
from .models import User
from .forms import InscriptionForm


inscription_bp = Blueprint('inscription', __name__)

# Cette méthode va nous envoyer vers le formulaire d'inscription
@inscription_bp.route('/create-account', methods=['GET', 'POST'])
def inscription():
    form = InscriptionForm() # On instancie un Objet de la classe InscriptionForm
    if form.validate_on_submit(): # Si on soumet le formulaire
        # On récupère les données de chaque champs
        firstname = form.firstname.data
        lastname = form.lastname.data
        username = form.username.data
        telephone = form.telephone.data
        email = form.email.data
        pwd = form.password.data
        print(firstname, lastname, username, telephone, email, pwd)
        # pwd2 = form.password2.data
        user = User(firstname, lastname, telephone, username, email, pwd) # On passe les données à l'objet User
        user.save() # On enregistre les données de l'objet dans la base de données
        return redirect(url_for('inscription.inscription_reussie'))
    return render_template('client/inscription.html', form=form) # Puis on le passe au template
    # return redirect('client/inscription.html')
    
@inscription_bp.route('/signup_succesfull')
@login_required # Connexion requise pour accéder à cette route
def inscription_reussie():
    return render_template("client/success.signup.html")