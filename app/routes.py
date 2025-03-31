from flask import Blueprint, request, jsonify
from .models import Blacklist
from .init import db
from .auth import token_required

bp = Blueprint('routes', __name__)

@bp.route('/blacklists', methods=['POST'])
@token_required
def add_to_blacklist():
    data = request.get_json()
    email = data.get('email')
    app_uuid = data.get('app_uuid')
    blocked_reason = data.get('blocked_reason', '')

    if not email or not app_uuid:
        return jsonify({'error': 'email and app_uuid are required'}), 400

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
