from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, supports_credentials=True, origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
    ])
    login_manager.init_app(app)

    # Import models so Alembic sees them
    from src.models import (  # noqa: F401
        city, union, panchayat, childcare_centre,
        cluster, employee, registration, evaluate, evaluation_month,
    )

    # Register blueprints
    from src.routes.api_routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
