from app import db
from datetime import datetime

class Blacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    app_uuid = db.Column(db.String(36), nullable=False)
    blocked_reason = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    request_ip = db.Column(db.String(45), nullable=False)  # IPv6 puede tener hasta 45 caracteres
    request_time = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'app_uuid': self.app_uuid,
            'blocked_reason': self.blocked_reason,
            'created_at': self.created_at.isoformat(),
            'request_ip': self.request_ip,
            'request_time': self.request_time.isoformat()
        } 