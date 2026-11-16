from flask import Blueprint, abort
from flask_login import current_user, login_required

from extensions import limiter

admin_bp = Blueprint('admin_bp', __name__)


def _admin_user_key():
	return str(current_user.id) if current_user.is_authenticated else 'anonymous'


@admin_bp.before_request
@login_required
@limiter.limit('60 per minute', key_func=_admin_user_key)
def require_admin():
	if current_user.role != 'admin':
		abort(403)

from . import dashboard
from . import product
from . import category
from . import user
from . import audit
from . import order
