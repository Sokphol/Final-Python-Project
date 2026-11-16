import sys
import os

# Add project root directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from init_watch_store import init_db

# Ensure database tables and initial products are initialized on Vercel
try:
    init_db()
except Exception as e:
    print("Database initialization note:", e)

class StripApiPrefixMiddleware:
    """
    Middleware that ensures Vercel serverless rewrites (e.g. /api/index, /api/index.py)
    are transparently mapped to Flask's root and sub-routes without 404s.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path_info = environ.get('PATH_INFO', '')
        if path_info.startswith('/api/index.py'):
            environ['PATH_INFO'] = path_info[len('/api/index.py'):] or '/'
        elif path_info.startswith('/api/index'):
            environ['PATH_INFO'] = path_info[len('/api/index'):] or '/'
        elif path_info.startswith('/api'):
            environ['PATH_INFO'] = path_info[len('/api'):] or '/'
        return self.wsgi_app(environ, start_response)

app.wsgi_app = StripApiPrefixMiddleware(app.wsgi_app)
application = app
