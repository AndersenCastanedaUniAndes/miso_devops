from functools import wraps
from flask import request, jsonify, current_app

def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                'success': False,
                'message': 'Token de autorización no proporcionado'
            }), 401
            
        # Verificar que el header comience con 'Bearer '
        if not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'message': 'Formato de token inválido. Debe comenzar con "Bearer "'
            }), 401
            
        # Extraer el token
        token = auth_header.split(' ')[1]
        
        # Verificar que el token no esté vacío
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token no puede estar vacío'
            }), 401
            
        # Verificar que el token coincida
        if token != current_app.config['API_TOKEN']:
            return jsonify({
                'success': False,
                'message': 'Token de autorización inválido'
            }), 401
            
        return f(*args, **kwargs)
    return decorated 