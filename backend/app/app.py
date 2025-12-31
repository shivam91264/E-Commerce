from flask import Flask
from app.models.models import db 
from app.config.config import Config


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def home():
    return {"msg":"hello-flask"}



with app.app_context():
    db.create_all()