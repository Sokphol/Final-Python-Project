from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy import text

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address, storage_uri='memory://')


def execute_raw_sql(sql, params=None, fetch=True):
    result = db.session.execute(text(sql), params or {})

    if fetch:
        return result.fetchall()
    else:
        db.session.commit()
        return result.rowcount