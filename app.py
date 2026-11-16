import os
from flask import Flask, request, render_template, session
from extensions import db, migrate, login_manager, limiter
from config import Config
import front, admin, auth
from models.user import User
from models.rate_limit_log import RateLimitLog
from models.audit_log import AuditLog
from flask_login import current_user

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static'),
    static_url_path='/static'
)

app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
limiter.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to continue.'


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except Exception:
        return None


@app.context_processor
def inject_cart_info():
    cart = session.get('cart', {})
    cart_count = sum(item.get('quantity', 1) for item in cart.values()) if isinstance(cart, dict) else 0
    return {
        'cart_count': cart_count,
        'cart_items_count': len(cart) if isinstance(cart, dict) else 0
    }


_db_initialized = False

@app.before_request
def ensure_database():
    global _db_initialized
    if not _db_initialized:
        try:
            from init_watch_store import init_db
            init_db()
        except Exception as e:
            app.logger.warning(f"Database initialization notice: {e}")
        _db_initialized = True


@app.after_request
def write_audit_log(response):
    if not request.path.startswith('/static/'):
        try:
            log = AuditLog(
                endpoint=request.endpoint or request.path,
                method=request.method,
                path=request.path,
                ip_address=request.remote_addr,
                user_id=current_user.id if current_user.is_authenticated else None,
                status_code=response.status_code,
            )
            db.session.add(log)
            db.session.commit()
        except Exception:
            db.session.rollback()
    return response

app.register_blueprint(front.front_bp, url_prefix='/')
app.register_blueprint(admin.admin_bp, url_prefix='/admin')
app.register_blueprint(auth.auth_bp)

import models


@app.errorhandler(429)
def rate_limit_handler(error):
    identifier_type = 'user_id' if request.path.startswith('/admin') else 'ip'
    user_id = current_user.id if current_user.is_authenticated else None
    try:
        log = RateLimitLog(
            endpoint=request.endpoint or request.path,
            identifier=str(user_id or request.remote_addr or 'unknown'),
            identifier_type=identifier_type,
            ip_address=request.remote_addr,
            user_id=user_id,
        )
        db.session.add(log)
        db.session.commit()
    except Exception:
        db.session.rollback()
    return render_template('429.html', error=str(error)), 429

if __name__ == '__main__':
    app.run()
