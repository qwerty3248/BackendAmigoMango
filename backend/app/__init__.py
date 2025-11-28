from flask import Flask
from .routes import api
from .extensiones import db, bcrypt
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)

    CORS(app, resources={r"/*": {"origins": "*"}})
    CORS(api, resources={r"/*": {"origins": "*"}})

    app.register_blueprint(api)
    
    bcrypt.init_app(app)
    
    return app