from flask import Flask
from app.models.models import db 
from app.config.config import Config
# from app.extensions import db
from app.extensions import cache

from flask_cors import CORS


from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)

# JWT Secret Key (required)
app.config["JWT_SECRET_KEY"] = "super_secret_key_123456789"  # change this in production


db.init_app(app)
cache.init_app(app) 


CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})


@app.route('/')
def home():
    return {"msg":"hello-flask"}

# Initialize JWT
jwt = JWTManager(app)

# Register blueprints
from app.resources.authentication.register import register_bp
app.register_blueprint(register_bp, url_prefix="/api")

from app.resources.authentication.login import login_bp
app.register_blueprint(login_bp, url_prefix="/api")

from app.resources.productlisting.admin_operations import admin_bp
app.register_blueprint(admin_bp, url_prefix="/api")

from app.resources.productlisting.user_operations import user_bp
app.register_blueprint(user_bp, url_prefix="/api")




with app.app_context():
    db.create_all()