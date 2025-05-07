from app import create_app, db
from flask import Flask
application = create_app()

if __name__ == '__main__':
     with application.app_context():
        db.create_all()  # Crea la base de datos si no existe
        application.run(host='0.0.0.0', port=5000, debug=True) 