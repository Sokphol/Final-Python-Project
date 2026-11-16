from datetime import datetime, timezone

from extensions import db


class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(255), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    path = db.Column(db.String(500), nullable=False)
    ip_address = db.Column(db.String(64), nullable=True)
    user_id = db.Column(db.Integer, nullable=True)
    status_code = db.Column(db.Integer, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )