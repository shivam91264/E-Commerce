from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

from app.models.models import db,User


# Define Blueprint
login_bp = Blueprint('login', __name__)

@login_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    # 1. Validate fields exist
    if not data.get('email') or not data.get('password'):
        return jsonify({"msg": "Email and Password are required"}), 400

    email = data.get('email')
    password = data.get('password')

    # 2. Fetch user by email
    user = User.query.filter_by(email=email).first()

    # 3. Check if user exists
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # 4. Compare password
    if check_password_hash(user.password_hash, password):
        # 5. Generate Access Token (Using email as identity)
        access_token = create_access_token(identity=user.email)

        return jsonify({
            "msg": "Login successful",
            "access_token": access_token,
            "user": user.serialize(),
            "is_admin": user.is_admin
        }), 200

    else:
        return jsonify({"msg": "Incorrect email or password"}), 401