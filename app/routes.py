from flask import Blueprint, request, jsonify
from .models import Blacklist
from . import db
from .auth import token_required

bp = Blueprint('routes', __name__)
health_bp = Blueprint('health', __name__)

@bp.route('/blacklists', methods=['POST'])
@token_required
def add_to_blacklist():
    data = request.get_json()
    email = data.get('email')
    app_uuid = data.get('app_uuid')
    blocked_reason = data.get('blocked_reason', '')

    if not email:
        return jsonify({'error': 'email required'}), 400

    if not app_uuid:
        return jsonify({'error': 'app_uuid required'}), 400

    if len(app_uuid) != 36 or not all(c in '0123456789abcdef-' for c in app_uuid):
        return jsonify({'error': 'Invalid app_uuid format'}), 400

    if len(blocked_reason) > 255:
        return jsonify({'error': 'blocked_reason exceeds maximum length'}), 400

    existing = Blacklist.query.filter_by(email=email).first()
    if existing:
        return jsonify({'message': 'Email already in blacklist'}), 200

    new_entry = Blacklist(
        email=email,
        app_uuid=app_uuid,
        blocked_reason=blocked_reason[:255],
        ip_address=request.remote_addr
    )
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({'message': 'Email added to blacklist successfully'}), 201

@bp.route('/blacklists/<string:email>', methods=['GET'])
@token_required
def check_blacklist(email):
    entry = Blacklist.query.filter_by(email=email).first()
    if entry:
        return jsonify({
            'blacklisted': True,
            'blocked_reason': entry.blocked_reason
        }), 200
    return jsonify({'blacklisted': False}), 200

@health_bp.route('/', methods=["GET"])
def index():
    return {"message": "API running"}, 200