from . import db
from datetime import datetime

class Blacklist(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    email           = db.Column(db.String(255), nullable=False, unique=True)
    app_uuid        = db.Column(db.String(36), nullable=False)
    blocked_reason  = db.Column(db.String(255))
    ip_address      = db.Column(db.String(45))
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)
