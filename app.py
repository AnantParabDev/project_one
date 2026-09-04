from flask import Flask, redirect, jsonify, request
from config.database import db, init_db
from controller.auth_controller import auth_bp
from controller.dashboard_controller import dashboard_bp
from controller.ticket_controller import ticket_bp
from controller.category_controller import category_bp
from flask_jwt_extended import JWTManager
from controller.comment_controller import comment_bp
from prometheus_flask_exporter import PrometheusMetrics
import os
from dotenv import load_dotenv
import time
import sys

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Retry database initialization
    max_retries = 10
    retry_delay = 3
    for attempt in range(max_retries):
        try:
            init_db(app)
            break
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Database connection failed (attempt {attempt + 1}/{max_retries}): {e}", file=sys.stderr)
                print(f"Retrying in {retry_delay} seconds...", file=sys.stderr)
                time.sleep(retry_delay)
            else:
                print(f"Failed to connect to database after {max_retries} attempts", file=sys.stderr)
                raise

    metrics = PrometheusMetrics(app)

    metrics.info(
         'flask_app_info', 
         "Flask Application Information",
         version = "1.0.0"
    )

    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.register_blueprint(auth_bp)
    app.register_blueprint(ticket_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(dashboard_bp)
    jwt = JWTManager(app)

    

    @jwt.unauthorized_loader
    def missing_token_callback(err_string):
        if request.is_json or request.path.startswith('/api'):
            return (jsonify({'message': 'Authorization token is missing', 'error': 'unauthorized'}), 401)
        return redirect('/')

    @jwt.invalid_token_loader
    def invalid_token_callback(err_string):
        if request.is_json or request.path.startswith('/api'):
            return (jsonify({'message': 'Authorization token is invalid', 'error': 'invalid_token'}), 401)
        return redirect('/')

    @app.errorhandler(Exception)
    def handle_global_error(e):
        app.logger.error(f'Unhandled Exception: {e}')
        if request.path.startswith('/api/'):
            return (jsonify({'message': 'An internal server error occurred.'}), 500)
        return ('An unexpected error occurred. Please try again later.', 500)
    
    with app.app_context():
        db.create_all()
    
    @app.route("/", methods=["GET"])
    def home():
        return "<h1>Home</h1>"
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)
