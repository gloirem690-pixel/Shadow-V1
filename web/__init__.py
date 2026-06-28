from flask import Flask
from web.routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key'  # À changer en prod
    register_routes(app)
    return app

def run_web_server(port=5000):
    app = create_app()
    app.run(host='0.0.0.0', port=port, debug=False)
