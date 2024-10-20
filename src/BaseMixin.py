#  C'est une classe de base pour nos modèles SQLAlchemy qui contient des méthodes utilitaires 
# communes entre nos modèles.

from werkzeug.security import check_password_hash

from .models import db

class BaseMixin:
    
    @classmethod
    def findAll(clss):
        return clss.query.all()
    
    @classmethod
    def findById(clss, id):
        return clss.query.get(id)
    
    # @classmethod
    # def findByPassword(cls, password):
    #     user = cls.query.filter_by(password=password).first()
    #     # Déterminer le schéma de hachage utilisé pour le hachage dans la base de données
    #     # Ceci dépend de la manière dont les mots de passe ont été hachés lors de leur stockage

    #     # Hacher le mot de passe en clair fourni par l'utilisateur en utilisant le même schéma de hachage
    #     hashed_password_input = hash_password(password)

    #     # Comparer les deux hachages pour voir s'ils correspondent
    #     if check_password_hash(password, hashed_password_input):
    #         return user
    #     else:
    #         return None
        
    # récupérer la valeur saisie par l'utilisateur dans le champ de mot de passe du formulaire, afin de la comparer avec les données de la base de données.
    @classmethod
    def filterByPassword(clss, password):
        return clss.query.filter_by(password=password.data).first()
    
    # récupérer la valeur saisie par l'utilisateur dans le champ d'email du formulaire, afin de la comparer avec les emails de la base de données.
    @classmethod
    def filterByEmail(clss, email):
        return clss.query.filter_by(email=email.data).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def remove(self):
        db.session.delete(self)
        db.session.commit()