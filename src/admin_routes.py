from flask import Flask, Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user

from .models import User

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard/all-users')
# @login_required
def dashboard():
    users = User.findAll()
    return render_template("admin/dashboard.html", user=current_user, users=users)


@admin_bp.route('/dashboard/user/<int:user_id>/remove', methods=['DELETE', 'POST'])
# @login_required
def remove_user(user_id):
    if request.method == 'DELETE' or (request.method == 'POST' and request.form.get('_method') == 'DELETE'):
        user = User.findById(user_id)
        user.remove()
        if request.method == 'DELETE':
            return jsonify({'message': 'User deleted'}), 200
    return redirect(url_for('admin.dashboard'))



@admin_bp.route('/dashboard/user/<int:user_id>/edit')
# @login_required
def edit_user(user_id):
    user = User.findById(user_id)
    return render_template("admin/manage.user.html", user=user)


@admin_bp.route('/dashboard/user/<int:user_id>/block-user', methods=['POST'])
# @login_required
def block_user(user_id):
    user = User.findById(user_id)
    if user:
        if user.isActive:
            user.isActive = False
            user.save()
            return jsonify({'message': 'L\'utilisateur a été bloqué avec succès.'}), 200
        return jsonify({'message': 'L\'utilisateur est déja bloqué.'}), 200
    return jsonify({'message': 'User not found.'}), 404


@admin_bp.route('/dashboard/user/<int:user_id>/unblock-user', methods=['POST'])
# @login_required
def unblock_user(user_id):
    user = User.findById(user_id)
    if user:
        if not user.isActive:
            user.isActive = True
            user.save()
            return jsonify({'message': 'L\'utilisateur a été débloqué avec succès'}), 200
        return jsonify({'message': 'L\'utilisateur est déja actif.'}), 200
    return jsonify({'message': 'User not found.'}), 404
