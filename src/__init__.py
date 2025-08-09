import os
from flask import Flask, session, redirect, url_for, request
from .models import db
from .routes.auth import bp as auth_bp
from .routes.dashboard import bp as dashboard_bp
from .routes.project import bp as project_bp
from .routes.team import bp as team_bp
from .routes.task import bp as task_bp


def create_app(test_config=None):
    print("Inside create_app function")
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flask_app.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize the database
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(team_bp)
    app.register_blueprint(task_bp)
    app.add_url_rule('/', endpoint='index')
    

    # Global login enforcement
    @app.before_request
    def require_login():
        # Define publicly accessible routes
        allowed_routes = ['auth.login', 'auth.register', 'auth.validate_email', 'static']
        if 'user_id' not in session and request.endpoint not in allowed_routes:
            return redirect(url_for('auth.login'))

    return app
