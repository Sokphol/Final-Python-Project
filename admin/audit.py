from flask import render_template

from models.audit_log import AuditLog
from . import admin_bp


@admin_bp.get('/audit-logs')
def audit_logs():
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(500).all()
    return render_template('admin/audit_logs.html', logs=logs)