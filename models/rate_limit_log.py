from datetime import datetime, timezone

from extensions import db


class RateLimitLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(255), nullable=False)
    identifier = db.Column(db.String(255), nullable=False)
    identifier_type = db.Column(db.String(30), nullable=False)
    ip_address = db.Column(db.String(64), nullable=True)
    user_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
