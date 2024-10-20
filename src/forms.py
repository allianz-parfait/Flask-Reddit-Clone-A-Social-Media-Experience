from flask import render_template
from flask_wtf import FlaskForm # importer le formulaire
from wtforms import StringField, PasswordField, EmailField, TextAreaField, SubmitField, ValidationError # importer les champs du formualaire (StringField = input tye text)
from flask_wtf.file import FileField, FileRequired # Pour gérer les fichiers vidéos et images
from wtforms.validators import InputRequired, DataRequired, Email, EqualTo, ValidationError, Length
# from wtforms.fields import FileField
from werkzeug.security import check_password_hash

from .models import User
from .functions import is_youtube_video_valid_url
# from .feed_routes import app
# On doit avoir une clé secrète

class LoginForm(FlaskForm):
    
    email = EmailField('Email', validators=[InputRequired("Le champ est requis!"), Email()])
    password = PasswordField('Password', validators=[InputRequired("Le champ est requis!"), Length(min=8, max=10)])
    submit = SubmitField('Se connecter')
    
    def validate_account(self, email):
        user = User.filterByEmail(email)
        if user:
            if user.isActive==False:
                raise ValidationError("Votre compte a été désactivé par l'administarteur!")
    
    

class InscriptionForm(LoginForm):
    
    firstname = StringField('Firstname', validators=[InputRequired("Le champ est requis!"), Length(min=7, message="Saisir au moins 7 caractères!")])
    lastname = StringField('Lastname', validators=[InputRequired("Le champ est requis!"), Length(min=4, max=15, message="Saisir au moins 7 caractères!")])
    username = StringField('Username', validators=[InputRequired("Le champ est requis!"), Length(min=7, max=10, message="Saisir entre 7 et 10 caractères!")])
    telephone = StringField('Telephone', validators=[InputRequired("Le champ est requis!"), Length(min=7, max=14, message="Saisir entre 7 et 10 caractères!")])
    password2 = PasswordField('Confirm Password', validators=[InputRequired("Le champ est requis!"), Length(min=8, max=10), EqualTo('password', message='Les mots de passe doivent correspondre')])
    submit = SubmitField('S\'inscrire')

    def validate_password(self, password):
        # user = User.query.filter_by(password=password.data)
        user = User.filterByPassword(password)
        if user:
            raise ValidationError("Ce mot de passe est déjà utilisé. Veuillez en choisir un autre!")


class PostForm(FlaskForm):
    title = StringField('Titre', validators=[InputRequired("Le champ est requis!"), Length(min=10, message="Saisir au moins 10 caractères!")])
    content = TextAreaField('Content', validators=[InputRequired("Le champ est requis!"), Length(min=15, message="Saisir au moins 15 caractères!")])
    submit = SubmitField('Poster')
# Beaucoup de personnes cherchent à vouloir réussir sans faire d'éfforts considérables, cela est le signe de paresse et de faiblesse...

class MediaForm(FlaskForm):
    titre = StringField('Titre', validators=[InputRequired("Le champ est requis!"), Length(min=10, max=70, message="Saisir au moins entre 10 à 70 caractères max!")])
    media = FileField('Télécharger des Médias', validators=[FileRequired()])
    add_media_btn = SubmitField('Ajouter des Medias', render_kw={'id' : 'add-media-button', 'class' : 'mt-3 text-lg font-semibold bg-orange-500 text-white rounded-lg px-6 py-3 block shadow-xl cursor-pointer hover:text-white hover:bg-orange-700', 'type' : 'button'})
    submit = SubmitField('Poster')
    
    
class CommentaireForm(FlaskForm):
    text_area = TextAreaField(validators=[InputRequired("Le champ est requis!"), Length(min=3, message="Saisir au moins 3 caractères!")])
    submit = SubmitField('Commenter')
    
    # def validate_media(self, field):
    #     if not field.data.filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4')):
    #         raise ValidationError('Ce fichier n\'est pas pris en charge.')

class YoutubeForm(FlaskForm):
    
    titre = StringField('Titre', validators=[InputRequired("Le champ est requis!"), Length(min=10, max=70)])
    youtube_link = StringField('YouTube Video Link', validators=[InputRequired("Le champ est requis!"), Length(min=48, max=48)])
    
    # Méthode permettant de valider si le lien saisi dans le champ lien (Youtube) est valide
    # Elle utilise la fonction 'is_youtube_video_valid_url' pour vérifier si le lien est valide ou pas
    def validate_youtube_link(self, field):
        if not is_youtube_video_valid_url(field.data):
            raise ValidationError('Le lien YouTube est invalide.')
    
    submit = SubmitField('Poster')
