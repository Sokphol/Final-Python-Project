from urllib.parse import urlparse

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db, limiter
from models.user import User
from . import auth_bp


def _safe_next_url(value):
    if not value:
        return None
    parsed = urlparse(value)
    if parsed.netloc or parsed.scheme:
        return None
    return value


@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit('5 per minute')
def login():
    if current_user.is_authenticated:
        return redirect(
            url_for('admin_bp.dashboard')
            if current_user.role == 'admin'
            else url_for('front_bp.home')
        )

    if request.method == 'POST':
        identity = request.form.get('identity', '').strip()
        password = request.form.get('password', '')
        user = db.session.scalar(
            db.select(User).where(or_(User.email == identity, User.user_name == identity))
        )
        valid_password = user and (
            check_password_hash(user.password, password)
            if user.password.startswith(('scrypt:', 'pbkdf2:', 'argon2:'))
            else user.password == password
        )
        if valid_password and user.is_active:
            if not user.password.startswith(('scrypt:', 'pbkdf2:', 'argon2:')):
                user.password = generate_password_hash(password)
                db.session.commit()
            login_user(user, remember=bool(request.form.get('remember')))
            next_url = _safe_next_url(request.args.get('next'))
            if next_url:
                return redirect(next_url)
            return redirect(
                url_for('admin_bp.dashboard')
                if user.role == 'admin'
                else url_for('front_bp.home')
            )
        flash('Invalid username/email or password.', 'error')

    return render_template('auth/login.html')


@auth_bp.get('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
