import os
import shutil
import tempfile
from dotenv import load_dotenv
from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError
import cloudinary

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "watch-shop-secret-key-2026")

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_URL = os.getenv("DATABASE_URL", "").strip().strip('"').strip("'")

    if DATABASE_URL:
        # Normalize postgres:// to postgresql:// for SQLAlchemy
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        try:
            make_url(DATABASE_URL)
            SQLALCHEMY_DATABASE_URI = DATABASE_URL
        except ArgumentError:
            SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "flask_db.sqlite").replace('\\', '/')
    else:
        # In serverless environments (e.g. Vercel), /var/task is read-only.
        # We copy or create the SQLite database in the system temp directory.
        if os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
            tmp_dir = tempfile.gettempdir()
            tmp_db = os.path.join(tmp_dir, "flask_db.sqlite")
            orig_db = os.path.join(BASE_DIR, "flask_db.sqlite")
            if os.path.exists(orig_db) and not os.path.exists(tmp_db):
                try:
                    shutil.copy2(orig_db, tmp_db)
                except Exception:
                    pass
            SQLALCHEMY_DATABASE_URI = "sqlite:///" + tmp_db.replace('\\', '/')
        else:
            SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "flask_db.sqlite").replace('\\', '/')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(tempfile.gettempdir() if os.getenv("VERCEL") else BASE_DIR, 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    PERMANENT_SESSION_LIFETIME = 1800

    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "").strip()
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "").strip()
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "").strip()

    if CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET:
        cloudinary.config(
            cloud_name=CLOUDINARY_CLOUD_NAME,
            api_key=CLOUDINARY_API_KEY,
            api_secret=CLOUDINARY_API_SECRET,
            secure=True,
        )
