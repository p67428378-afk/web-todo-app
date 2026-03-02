# Module: app.py
# Purpose: Main Flask application for the Hotel Order Management Service.
# Author: Architect Agent
# Created: 2024-03-02

from flask import Flask, jsonify
from .config import Config
from .models import init_db
from .routes import order_bp

def create_app():
    """
    Creates and configures the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)

    app.register_blueprint(order_bp)

    @app.route('/')
    def health_check():
        """
        Health check endpoint.
        """
        return jsonify({'status': 'Hotel Order Management Service is running'}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
