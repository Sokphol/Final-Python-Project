import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app
from extensions import db
from models.category import Category
from models.user import User
from init_watch_store import init_db


def test_duplicate_slug_is_rejected_on_category_update():
    with app.app_context():
        db.drop_all()
        db.create_all()

        first = Category(title='First', slug='first-slug', is_active=True)
        second = Category(title='Second', slug='second-slug', is_active=True)
        db.session.add_all([first, second])
        db.session.commit()

        second.slug = 'first-slug'

        try:
            db.session.commit()
        except Exception as exc:
            db.session.rollback()
            assert 'UNIQUE constraint failed' in str(exc)
        else:
            raise AssertionError('Expected duplicate slug update to fail')


def test_duplicate_email_is_rejected_on_user_update():
    with app.app_context():
        db.drop_all()
        db.create_all()

        first = User(user_name='first', email='first@example.com', password='pw', role='user', is_active=True)
        second = User(user_name='second', email='second@example.com', password='pw', role='user', is_active=True)
        db.session.add_all([first, second])
        db.session.commit()

        second.email = 'first@example.com'

        try:
            db.session.commit()
        except Exception as exc:
            db.session.rollback()
            assert 'UNIQUE constraint failed' in str(exc)
        else:
            raise AssertionError('Expected duplicate email update to fail')

        # Restore watch store data
        init_db()
