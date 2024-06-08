from flask import Flask
from .main_route import main_bp
from .items_route import items_bp
from .router import router_bp
from .switch import switch_bp
from .pc import pc_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(main_bp)
    app.register_blueprint(items_bp)
    app.register_blueprint(router_bp, url_prefix='/router')
    app.register_blueprint(switch_bp, url_prefix='/switch')
    app.register_blueprint(pc_bp, url_prefix='/pc')

    return app