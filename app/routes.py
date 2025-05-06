from flask import Blueprint, request, jsonify
from app.models import Blacklist
from app import db
from app.auth import require_token
from datetime import datetime

blacklist_bp = Blueprint('blacklist', __name__)
health_bp = Blueprint('health', __name__)

def get_client_ip():
    # Obtener la IP real del cliente, considerando proxies
    if 'X-Forwarded-For' in request.headers:
        return request.headers['X-Forwarded-For'].split(',')[0]
    return request.remote_addr

@blacklist_bp.route('', methods=['POST'])
@require_token
def create_blacklist():
    try:
        data = request.get_json()
        
        if not all(key in data for key in ['email', 'app_uuid', 'blocked_reason']):
            return jsonify({
                'success': False,
                'message': 'Faltan campos requeridos'
            }), 400

        new_blacklist = Blacklist(
            email=data['email'],
            app_uuid=data['app_uuid'],
            blocked_reason=data['blocked_reason'],
            request_ip=get_client_ip(),
            request_time=datetime.utcnow()
        )

        db.session.add(new_blacklist)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Email agregado a la lista negra exitosamente',
            'data': new_blacklist.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error al guardar el email: {str(e)}'
        }), 500

@blacklist_bp.route('/<string:email>', methods=['GET'])
@require_token
def check_blacklist(email):
    try:
        blacklist_entry = Blacklist.query.filter_by(email=email).first()
        
        if blacklist_entry:
            return jsonify({
                'success': True,
                'is_blacklisted': True,
                'data': {
                    'email': blacklist_entry.email,
                    'blocked_reason': blacklist_entry.blocked_reason,
                    'app_uuid': blacklist_entry.app_uuid,
                    'created_at': blacklist_entry.created_at.isoformat(),
                    'request_ip': blacklist_entry.request_ip,
                    'request_time': blacklist_entry.request_time.isoformat()
                }
            }), 200
        else:
            return jsonify({
                'success': True,
                'is_blacklisted': False,
                'message': 'El email no está en la lista negra'
            }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error al verificar el email: {str(e)}'
        }), 500 
@health_bp.route('/', methods=["GET"])
def index():
    return {"message": "API running"}, 200