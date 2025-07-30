from flask import Flask
from app.extensions import db, mail
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from app.models import Employee
import os

migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login_view'
login_manager.login_message_category = 'info'


def create_superuser():
    # Load from env or fallback to default
    email = os.getenv("SUPERUSER_EMAIL", "admin@company.com")
    raw_password = os.getenv("SUPERUSER_PASSWORD", "AdminPassword123")

    existing = Employee.query.filter_by(email=email).first()
    
    if not existing:
        admin = Employee(
            first_name="Super",
            surname="Admin",
            other_names="",
            email=email,
            phone="08000000000",
            password_hash=generate_password_hash(raw_password),
            must_reset_password=True,
            salary_per_day=0.0,
            status="full-time",
            office="Superadmin",
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
        print(f"✅ Superuser created: {email}")
    else:
        print(f"ℹ️ Superuser already exists: {email}")


def create_app():
    app = Flask(__name__)
    load_dotenv()

    # Configs
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Mail Config
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from app.routes import main
    app.register_blueprint(main)

    # Create DB and superuser on first run
    with app.app_context():
        db.create_all()
        create_superuser()

    return app


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))
