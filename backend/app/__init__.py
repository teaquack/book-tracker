from flask import Flask
import os
from app.extensions import db, cors
from app.routes import book_routes, list_routes, tags

def create_app():
    app = Flask(__name__)

    # Configure the app
    db_path = os.path.join(app.instance_path, 'book_tracker.db')
    os.makedirs(app.instance_path, exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    cors.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(book_routes.bp)
    app.register_blueprint(list_routes.bp)
    app.register_blueprint(tags.bp)

    return app
