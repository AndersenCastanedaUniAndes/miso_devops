from app import create_app, db
from flask import Flask
application = create_app()

if __name__ == '__main__':
    with application.app_context():
        db.create_all()
        application.run(debug=True)
