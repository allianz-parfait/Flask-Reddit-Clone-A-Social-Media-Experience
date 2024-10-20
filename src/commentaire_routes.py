from flask import Flask, Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user

from .models import Post
from .forms import CommentaireForm

commentaire_bp = Blueprint('commentaire', __name__)

@commentaire_bp.route('/post/<int:post_id>/make-comment', methods=['GET', 'POST'])
@login_required
def commenter_post(post_id):
    form = CommentaireForm()
    post = Post.findById(post_id)
    
    if request.method == 'POST':
        if form.validate_on_submit():
            # Logique pour traiter et enregistrer le commentaire
            # Par exemple, créer un nouvel objet Comment et l'ajouter à la base de données
            comment_text = form.text_area.data
            # Supposons que vous avez un modèle Comment et que vous le sauvegardez ici
            # new_comment = Comment(text=comment_text, user_id=current_user.id, post_id=post_id)
            # db.session.add(new_comment)
            # db.session.commit()
            
            return jsonify(success=True, message="Commentaire soumis avec succès")
        return jsonify(success=False, message="Échec de la validation du formulaire")

    return render_template("client/commentaire.view.html", post=post, user=current_user, form=form)
