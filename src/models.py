# Ici, on a les modèles
import requests
from enum import Enum
from typing import List
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# Permet de gérer les sessions utilisateurs après connexion
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash # permet de hasher les mots de passes
# pip install flask-bcrypt: Pour pouvoir hacher les mots de passes des users


from .feed_routes import app
from .functions import is_youtube_video_valid_url, is_embeded_youtube_video_url, extract_video_id

app.app_context().push()

# Initialiser la base de données avec l'application Flask
db = SQLAlchemy(app)

from .BaseMixin import BaseMixin

# Génerer la migration de la base de données avec l'application Flask et l'instance (db) de base de données
migrate = Migrate(app, db)

# Configurer le LoginManager (pour gérer les sessions utilisateurs)
login_manager = LoginManager(app)


# Fonction pour initialiser la base de données
def init_db():
    with app.app_context():
        db.create_all()
    
    
# Modèle de la table d'association pour représenter la relation many-to-many entre les utilisateurs
association_table = db.Table('UserFollowsAssociationTable',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followee_id', db.Integer, db.ForeignKey('users.id'))
)

# Classe qui va se charger de créer et gérer les utilisateurs
# On fait hériter la classe User de UserMixin qui se chargera de gérer les utilisateurs
class User(BaseMixin, UserMixin, db.Model): # Il hérite de db.Model, ce qui va créer sa table en Base de données
    
    # Pour changer le nom de la table
    __tablename__ = 'users'
    
    # Les Colonnes de la base de données
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(10), nullable=False, unique=True)
    telephone = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(15), nullable=False, unique=True) # Ce champ stockera les mots de passes utilisateurs mais hashés
    photo_profil = db.Column(db.String(255), default='no_profil.png')  # Chemin vers l'image de profil
    isActive = db.Column(db.Boolean, default=True)
    date_creation = db.Column(db.DateTime)
    posts = db.relationship('Post', back_populates='author')  # Changer le nom de la relation inverse
    commentaires = db.relationship('Commentaire', backref='user', lazy=True)  # Relation One-to-Many avec les commentaires
    votes = db.relationship('Vote', backref='user', lazy=True)  # Relation One-to-Many avec les votes
    souscriptions = db.relationship('Souscription', backref='user', lazy=True)  # Relation One-to-Many avec les souscriptions
    follows = db.relationship('Follow', primaryjoin='User.id == Follow.followee_id', backref='followee', lazy=True)
    followers = db.relationship('Follow', primaryjoin='User.id == Follow.follower_id', backref='follower', lazy=True)
    
    
    # Le Constructeur
    def __init__(self, firstname: str, lastname: str, telephone: str, username: str, email: str, password: str, photo_profil:str = 'no_profil.png') -> None:
        self.firstname = firstname
        self.lastname = lastname
        self.telephone = telephone
        self.username = f"u/{username}"
        self.email = email
        self.set_password_hash(password) # On appelle la méthode de hachage qui va hacher le mdp dès qu'on crée une instance de User
        self.photo_profil = photo_profil
        self.date_creation = datetime.now(timezone.utc) # Stocker la date et l'heure en tant qu'objet datetime
    
    # Cette méthode permet de hacher un mot de passe utilisateur  
    def set_password_hash(self, password):
        self.password = generate_password_hash(password)
    
    # Cette méthode permet de comparer le mdp en clair passé en paramètre au mdp haché stocké en BD
    # Si les deux correspondent, on retourne True, sinon on retourne False.
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    
    # Méthode d'ajout d'un post dans la liste
    def addPost(self, post):
        self.listPosts.append(post)
        
    # Méthode d'ajout d'un commentaire dans la liste
    def addComment(self, comment):
        self.listCommentaires.append(comment)
        
    # Méthode d'ajout d'un vote dans la liste
    def addVote(self, vote):
        self.listVotes.append(vote)
        
    # Méthode d'ajout d'une souscription dans la liste
    def addSouscription(self, souscription):
        self.listSouscriptions.append(souscription)
        
    # Méthode d'ajout d'un follow (abonnement) dans la liste
    def addFollow(self, follow):
        self.listFollows.append(follow)
    
    @classmethod
    def findAll(clss):
        return clss.query.order_by(clss.date_creation)

    # Méthode pour afficher un User
    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.telephone}', '{self.email}', '{self.password}', '{self.date_creation.strftime("%d-%m-%Y %H:%M")}')"





# Classe qui va permettre de créer et gérer les photos des utilisateurs
class Photo(BaseMixin, db.Model):
    
    __tablename__ = 'photos'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))  # URL de la photo
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))  # Clé étrangère vers l'ID du post
    
    def __init__(self, photo_url, post="") -> None:
        self.url = photo_url
        if post:
            self.post = post
        # https://youtu.be/hykb5RC-DZs?si=CMdbug-5hkSd2oXO

# from src.models import User, Video, Post 
# user = User("Dicklan", "Norton","+221764534543", "D.Norton", "dicknorton@gmail.com", "passer1")
# video = Video ("https://youtu.be/hykb5RC-DZs?si=CMdbug-5hkSd2oXO")
# post = Post("Chris Brown New Song With Bryson Tyller", user)
# user.save()
# video.save()
# post.save()
# Classe qui va permettre de créer et gérer les videos des utilisateurs
class Video(BaseMixin, db.Model):
    __tablename__ = 'videos'
    
    id = db.Column(db.Integer, primary_key=True)
    video_url = db.Column(db.String(255), nullable=False)  # Identifiant unique de la vidéo YouTube
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))  # Clé étrangère vers l'ID du post
    
    def __init__(self, video_url, post=None) -> None:
        if is_youtube_video_valid_url(video_url):
            self.video_url = f"https://www.youtube.com/embed/{extract_video_id(video_url)}?autoplay=1"
        else:
            self.video_url = video_url
        if post:
            self.post = post

    def __repr__(self):
        return f"Post('{self.video_url}')"
    
    @classmethod
    def findById(clss, id):
        return super().findById(id)


# Cette Classe est une Enumération
# Classe qui va permettre de connaitre le type d'un post
class TypePost(Enum):
    PHOTO = 'photo'
    VIDEO = 'video'
    YOUTUBE = 'youtube'
    CONTENT = 'content'
    


# Classe qui va permettre de créer et gérer les posts des utilisateurs
class Post(BaseMixin, db.Model):
    
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    titre_post = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Clé étrangère vers l'ID du user
    author = db.relationship('User', back_populates='posts')  # Utiliser un autre nom pour la relation inverse
    content = db.Column(db.Text, nullable=True) # Ici, ce sera le post sous forme de contenu texte au cas ou un utilisateur voudrait poster du texte
    date_creation = db.Column(db.DateTime)  # Utilisation de DateTime pour stocker la date et l'heure
    commentaires = db.relationship('Commentaire', backref='post', lazy=True)  # Relation One-to-Many avec les commentaires
    votes = db.relationship('Vote', backref='post', lazy=True)  # Relation One-to-Many avec les votes
    photos = db.relationship('Photo', backref='post', lazy=True)  # Relation One-to-Many avec les photos
    videos = db.relationship('Video', backref='post', lazy=True)  # Relation One-to-Many avec les photos
    type = db.Column(db.Enum(TypePost), nullable=True)  # Utilisation de l'énumération pour le type de post

    
    def __init__(self, titre_post, content=None, auteur=None) -> None:
        self.titre_post = titre_post
        if content:
            self.content = content
            self.type = TypePost.CONTENT
        if auteur:
            self.author = auteur
        self.date_creation = datetime.now(timezone.utc) # Pour stocker la date et l'heure en temps réél
    
    # Méthode d'ajout d'un commentaire dans la liste
    def addComment(self, comment):
        self.commentaires.append(comment)
        
    # Méthode d'ajout d'un vote dans la liste
    def addVote(self, vote):
        self.votes.append(vote)
        
    # Méthode d'ajout d'une photo dans la liste
    def addPhoto(self, photo):
        # Obtient l'URL de l'image à partir de l'objet photo
        image_url = photo.url
        
        # Vérifie si l'URL se termine par une extension d'image courante
        if image_url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            self.photos.append(photo)
            self.type = TypePost.PHOTO
        else:
            print("Extension de fichier non prise en charge.")
        
    # Méthode d'ajout d'une video dans la liste 
    def addVideo(self, video):
        # Si le lien de la video est un lien embeded du genre 'https://www.youtube.com/embed/M5g91Om0Wlg?autoplay=1'
        if is_embeded_youtube_video_url(video.video_url):
            self.type = TypePost.YOUTUBE # On lui donne le type Youtube
            self.videos.append(video)
        elif video.video_url.endswith('.mp4'):
            # Si l'URL se termine par .mp4, c'est une vidéo MP4 standard
            self.type = TypePost.VIDEO
            self.videos.append(video)
            self.videos.append(video)

    def time_since_posted(self):
        now = datetime.utcnow()
        delta = now - self.date_creation
        
        if delta < timedelta(minutes=1):
            return 'just now'
        elif delta < timedelta(hours=1):
            minutes = delta.seconds // 60
            return f'{minutes} minute{"s" if minutes != 1 else ""} ago'
        elif delta < timedelta(days=1):
            hours = delta.seconds // 3600
            return f'{hours} hour{"s" if hours != 1 else ""} ago'
        elif delta < timedelta(days=30):
            days = delta.days
            return f'{days} day{"s" if days != 1 else ""} ago'
        elif delta < timedelta(days=365):
            months = delta.days // 30
            return f'{months} month{"s" if months != 1 else ""} ago'
        else:
            years = delta.days // 365
            return f'{years} year{"s" if years != 1 else ""} ago'
    
    # Méthode d'ajout d'un vote dans la liste
    def __repr__(self):
        return f"Post('{self.titre_post}', '{self.author}', '{self.photos}', '{self.videos}', '{self.date_creation}')"
    
    
    
# Classe qui va permettre de créer et gérer les commentaires utilisateurs
class Commentaire(BaseMixin, db.Model):
    
    __tablename__ = 'commentaires'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    date_creation = db.Column(db.DateTime)  # Utilisation de DateTime pour stocker la date et l'heure
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    votes = db.relationship('Vote', backref='commentaire', lazy=True)  # Relation One-to-Many avec les votes

    def __init__(self, content: str, user:User, post:Post) -> None:
        self.content = content
        self.user = user
        self.post = post
        self.date_creation = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M") # Pour stocker la date et l'heure en temps réél
        
    def addVote(self, vote):
        self.votes.append(vote)



# Classe qui va se charger de créer et gérer les abonnements des utilisateurs à des subreddits
class Souscription(BaseMixin, db.Model):
    
    __tablename__ = 'souscriptions' # Les abonnements à des subreddits
    
    id = db.Column(db.Integer, primary_key=True)
    subscriber_id = db.Column(db.Integer, db.ForeignKey('users.id')) # L'abonné (qui est un user)
    subreddit_id = db.Column(db.Integer, db.ForeignKey('subreddits.id'))
    date_souscription = db.Column(db.DateTime)  # Utilisation de DateTime pour stocker la date et l'heure
    
    def __init__(self, subscriber, subreddit) -> None:
        self.subscriber = subscriber # L'abonné
        self.subreddit = subreddit
        self.date_souscription = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M") # Pour stocker la date et l'heure en temps réél
    
    
# Classe qui va se charger de créer et gérer les abonnements entre utilisateurs
class Follow(BaseMixin, db.Model):
    
    __tablename__ = 'follows' # Les abonnements entre utilisateurs
    
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id')) # L'utilisateur_source (le suiveur)
    followee_id = db.Column(db.Integer, db.ForeignKey('users.id')) # L'utilisateur_cible (le suivi)
    date_abonnement = db.Column(db.DateTime)  # Utilisation de DateTime pour stocker la date et l'heure
    
    def __init__(self, follower, followee) -> None:
        self.follower = follower # L'utilisateur_source (le suiveur)
        self.followee = followee # L'utilisateur_cible (le suivi)
        self.date_abonnement = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M") # Pour stocker la date et l'heure en temps réél
    

# Classe qui va permettre de créer et gérer les subreddits (communautés reddit)
class Subreddit(BaseMixin, db.Model):
    
    __tablename__ = 'subreddits'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(25))  # Le nom du Subreddit
    description = db.Column(db.String(50))
    date_creation = db.Column(db.DateTime)  # Utilisation de DateTime pour stocker la date et l'heure
    souscriptions = db.relationship('Souscription', backref='subreddit', lazy=True)  # Relation One-to-Many avec les commentaires
    
    def __init__(self, nom, description) -> None:
        self.nom = f"r/{nom}"
        self.description = description
        self.date_creation = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M") # Pour stocker la date et l'heure en temps réél
        
    def addSouscription(self, souscription):
        self.souscriptions.append(souscription)


# Cette Classe est une Enumération
# Classe qui va permettre de connaitre le type de vote d'un user sur un post (Vote positif ou Vote négatif)
class TypeVote(Enum):
    NEGATIF = 0
    POSITIF = 1
    
    
# Classe qui va permettre de faire des votes, de donner des votes (like) à un post.
# Les vote peuvent etre des upvotes (vote positif) ou downvotes (vote négatif)
class Vote(BaseMixin, db.Model):
    
    __tablename__ = 'votes'
    
    id = db.Column(db.Integer, primary_key=True)
    type_vote = db.Column(db.Enum(TypeVote), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    commentaire_id = db.Column(db.Integer, db.ForeignKey('commentaires.id'), nullable=True)
    date_creation = db.Column(db.DateTime)  # Utilisation de DateTime pour stocker la date et l'heure
    
    def __init__(self, type_vote:TypeVote, user, post, commentaire) -> None:
        self.type_vote = type_vote
        self.user = user
        self.post = post
        self.commentaire = commentaire
        self.date_creation = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M") # Pour stocker la date et l'heure en temps réél
        

# post = Post.findById(1)
# print(post.__repr__)

# Initialiser la base de données
# init_db()

# v = Video("https://youtu.be/ZsQnAuh3tZU?si=kVrXRtSxgTVuFFRN")
# print(f"ID : {v.video_url}")
# print(extract_video_id("https://youtu.be/ZsQnAuh3tZU?si=kVrXRtSxgTVuFFRN"))
# print(is_youtube_video_url('https://www.youtube.com/embed/ZsQnAuh3tZU?autoplay=1'))
# posts = Post.findAll()
# for post in posts:
#     print(post.type)
#     for video in post.videos:
#         print(f"lien:{video.video_url}, id:{video.post_id}")
# all_users = User.findAll()
# for user in all_users:
#     print(user)

# def hash_existing_passwords():
#     # Récupérer les utilisateurs avec des mots de passe non hashés
#     users_to_hash = User.query.filter(User.password!='scrypt:32768:8:1$OSCe1iibqwzkUh0q$70342d56215243f761dc8f6be69603d6f954a0d9dec9c5dea08d02e62515a93c6f2946a415df904b6973e03054646e13e30348e94befd32d5dc290ca288d173e').all()
    
#     # Afficher les mots de passe des utilisateurs avant le hachage (facultatif)
#     for user in users_to_hash:
#         print("Mot de passe non hashé :", user.password)
    
#     # Hasher les mots de passe récupérés
#     for user in users_to_hash:
#         user.password = generate_password_hash(user.password)
#         # Vous pouvez également ajouter une vérification ici pour ne pas hasher les mots de passe vides ou nuls
    
#     # Enregistrez les modifications en base de données
#     db.session.commit()
    
#     # Afficher les mots de passe hashés après le hachage (facultatif)
#     for user in users_to_hash:
#         print("Mot de passe hashé :", user.password)
        
# hash_existing_passwords()

# user = User.filterByPassword("alliance23")
# if user:
#     if check_password_hash(user.password, password):
#         if(user.isActive==True):
#             #print("Votre compte a été désactivé par l'administarteur!")
#             print(user.__repr__)