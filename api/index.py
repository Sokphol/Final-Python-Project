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
