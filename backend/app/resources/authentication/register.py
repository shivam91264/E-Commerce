from app.models.models import db,User

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash


# Define Blueprint
register_bp = Blueprint('register', __name__)

@register_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()

    required_fields = ['full_name', 'email', 'password']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"msg": f"Field '{field}' is required"}), 400

    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    phone = data.get('phone')

    # SPLIT full_name into first_name & last_name
    name_parts = full_name.split(" ", 1)
    first_name = name_parts[0]
    last_name = name_parts[1] if len(name_parts) > 1 else None

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "Email already registered"}), 400

    hashed_password = generate_password_hash(password)

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=hashed_password,
        phone=phone,
        # is_admin=False
        is_admin=data.get("is_admin", False)
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "Registration successful", "user_id": new_user.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Registration failed", "error": str(e)}), 500
