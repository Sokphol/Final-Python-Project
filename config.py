import os
import shutil
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
            SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "flask_db.sqlite")
    else:
        # Vercel serverless environment handling:
        # Vercel filesystem is read-only except /tmp
        if os.getenv("VERCEL"):
            tmp_db = "/tmp/flask_db.sqlite"
            orig_db = os.path.join(BASE_DIR, "flask_db.sqlite")
            if not os.path.exists(tmp_db) and os.path.exists(orig_db):
                try:
                    shutil.copy2(orig_db, tmp_db)
                except Exception:
                    pass
            SQLALCHEMY_DATABASE_URI = f"sqlite:///{tmp_db}"
        else:
            SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "flask_db.sqlite")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
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
