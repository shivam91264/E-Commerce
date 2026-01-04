from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from datetime import datetime
from app.models.models import db, User, Product, Category, Order, OrderItem, Message, ProductImage, ProductAttribute, Review


admin_bp = Blueprint('admin', __name__)

# ----------------------------------------------------------------------
# HELPER: Admin Authorization Check
# ----------------------------------------------------------------------
def get_admin_user():
    """
    Helper to fetch current user and verify admin status.
    Returns user object if valid admin, else None.
    """
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if user and user.is_admin:
        return user
    return None

# ----------------------------------------------------------------------
# 1. ADMIN DASHBOARD / ANALYTICS
# ----------------------------------------------------------------------


##  TESTING DONE
# 1 Admin Summary (Matches Dashboard Cards)

@admin_bp.route('/admin/summary', methods=['GET'])
@jwt_required()
def get_summary():
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    total_users = User.query.filter_by(is_active=True).count()
    total_orders = Order.query.count()
    total_products = Product.query.count()

    # Calculate total revenue
    total_revenue = db.session.query(func.sum(Order.total_amount)).scalar() or 0

    # Return customer rate = users who ordered >1 time / total unique users with orders
    repeat_buyers = db.session.query(Order.user_id).group_by(Order.user_id).having(func.count(Order.id) > 1).count()
    unique_buyers = db.session.query(Order.user_id).distinct().count()
    return_rate = (repeat_buyers / unique_buyers * 100) if unique_buyers > 0 else 0

    return jsonify({
        "revenue": total_revenue,
        "total_orders": total_orders,
        "active_users": total_users,
        "return_rate": round(return_rate, 2)
    }), 200




##  TESTING DONE
# 2️⃣ Monthly Revenue Trend (Line Graph)
@admin_bp.route('/admin/revenue_trend', methods=['GET'])
@jwt_required()
def revenue_trend():
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    results = db.session.query(
        func.strftime('%Y-%m', Order.created_at).label('month'),
        func.sum(Order.total_amount).label('revenue')
    ).group_by('month').order_by('month').all()

    data = [{"month": r.month, "revenue": r.revenue} for r in results]
    return jsonify({"data": data}), 200


##  TESTING DONE
# 3️⃣ Order Status Breakdown (Doughnut Chart)
@admin_bp.route('/admin/order_status', methods=['GET'])
@jwt_required()
def order_status():
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    statuses = ['Delivered', 'Pending', 'Processing', 'Cancelled']
    data = {}

    for status in statuses:
        count = Order.query.filter_by(status=status).count()
        data[status] = count

    return jsonify({"data": data}), 200


##  TESTING DONE
# 4️⃣ Top Categories (Bar Chart)
@admin_bp.route('/admin/category_stats', methods=['GET'])
@jwt_required()
def get_category_stats():
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    results = db.session.query(
        Category.name,
        func.count(Product.id)
    ).outerjoin(Product).group_by(Category.id).all()

    data = [{"category": r[0], "count": r[1]} for r in results]
    return jsonify({"data": data}), 200


##  TESTING DONE
# 5️⃣ Performance Insights (Sidebar List)
@admin_bp.route('/admin/performance_insights', methods=['GET'])
@jwt_required()
def performance_insights():
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    # 🔥 Highest rated product (VALID – uses Review table)
    highest_rated = db.session.query(
        Product.name,
        func.avg(Review.rating).label('avg_rating')
    ).join(Review)\
     .group_by(Product.id)\
     .order_by(func.avg(Review.rating).desc())\
     .first()

    # 📦 Average order value
    avg_order_value = db.session.query(
        func.avg(Order.total_amount)
    ).scalar() or 0

    return jsonify({
        "avg_order_value": round(avg_order_value, 2),

        # ⛔ temporarily disabled until Product.views exists
        # "most_viewed": None,
        # "most_viewed_count": None,

        # ⭐ Ratings analytics
        "highest_rated": highest_rated[0] if highest_rated else None,
        "highest_rating": round(highest_rated[1], 1) if highest_rated else None,

        # 📍 Optional static insight
        "top_region": "Mumbai, MH"
    }), 200








# ----------------------------------------------------------------------
# 2. USERS MANAGEMENT
# ----------------------------------------------------------------------
# TESTING DONE 

# ---------------------- Helper Function ---------------------- #

def user_to_admin_view(user):
    """ Transform user model into AdminUsers.vue compatible format """
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or "Unnamed"
    orders_count = db.session.query(func.count(Order.id)).filter(Order.user_id == user.id).scalar()

    return {
        "id": user.id,
        "name": full_name,
        "email": user.email,
        "phone": user.phone,
        "role": "Admin" if user.is_admin else "User",
        "ordersCount": orders_count,
        "active": user.is_active,
        "joinedDate": user.created_at.strftime("%b %d, %Y") if user.created_at else None
    }


# ---------------------- GET ALL USERS ---------------------- #


# @admin_bp.route('/admin/users', methods=['GET'])
# @jwt_required()
# def get_all_users():
#     if not get_admin_user():
#         return jsonify({"msg": "Admin access required"}), 401

#     users = User.query.order_by(User.created_at.desc()).all()
#     return jsonify({
#         "data": [user_to_admin_view(u) for u in users],
#         "msg": "Users list loaded"
#     }), 200


## more functional route :--
## Testing Done

@admin_bp.route('/admin/users', methods=['GET'])
@jwt_required()
def get_all_users():
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    role = request.args.get("role")          # admin / user
    active = request.args.get("active")      # true / false
    search = request.args.get("search")      # name or email

    query = User.query

    # Filter by role
    if role == "admin":
        query = query.filter(User.is_admin == True)
    elif role == "user":
        query = query.filter(User.is_admin == False)

    # Filter by active status
    if active is not None:
        query = query.filter(User.is_active == (active.lower() == "true"))

    # Search by name or email
    if search:
        query = query.filter(
            (User.email.ilike(f"%{search}%")) |
            (User.first_name.ilike(f"%{search}%")) |
            (User.last_name.ilike(f"%{search}%"))
        )

    pagination = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=limit, error_out=False
    )

    return jsonify({
        "msg": "Users list loaded",
        "total": pagination.total,
        "page": page,
        "pages": pagination.pages,
        "data": [user_to_admin_view(u) for u in pagination.items]
    }), 200



# ---------------------- GET SINGLE USER ---------------------- #

## Testing Done

@admin_bp.route('/admin/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_single_user(user_id):
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({
        "data": user_to_admin_view(user),
        "msg": "User details loaded"
    }), 200


# ---------------------- TOGGLE ACTIVE/BLOCK USER ---------------------- #

##  Testing Done

@admin_bp.route('/admin/users/<int:user_id>/status', methods=['PUT'])
@jwt_required()
def update_user_status(user_id):
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json()
    if "is_active" not in data:
        return jsonify({"msg": "is_active field is required"}), 400

    user.is_active = bool(data["is_active"])
    db.session.commit()

    return jsonify({
        "msg": "User status updated",
        "data": user_to_admin_view(user)
    }), 200



# ---------------------- DELETE USER (EXCEPT ADMIN) ---------------------- #

## Testing Done

@admin_bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def archive_user(user_id):
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    if user.is_admin:
        return jsonify({"msg": "Cannot delete admin user"}), 403

    user.is_active = False
    user.is_deleted = True
    db.session.commit()

    return jsonify({"msg": "User archived successfully"}), 200





# ----------------------------------------------------------------------
# 4. PRODUCTS MANAGEMENT
# ----------------------------------------------------------------------



# ----------------------------------------------------------------------
# 4. PRODUCTS MANAGEMENT (Vue Friendly)
# ----------------------------------------------------------------------


# ---------- Helper: Convert DB Product to Vue format ---------- #

def product_to_admin_vue(product):
    category = Category.query.get(product.category_id)

    # fetch primary image or fallback to first or placeholder
    primary_img = ProductImage.query.filter_by(product_id=product.id, is_primary=True).first()
    fallback_img = ProductImage.query.filter_by(product_id=product.id).first()
    image_url = primary_img.image_url if primary_img else (fallback_img.image_url if fallback_img else "https://via.placeholder.com/120")

    return {
        "id": product.id,
        "name": product.name,
        "category": category.name if category else "Unknown",
        "price": product.price,
        "salePrice": product.sale_price,
        "stock": product.stock_quantity,
        "active": product.is_active,
        "image": image_url
    }


# ------------------ GET all products ------------------ #
## Testing Done

# @admin_bp.route('/admin/products', methods=['GET'])
# @jwt_required()
# def list_products():
#     if not get_admin_user():
#         return jsonify({"msg": "Admin access required"}), 401

#     products = Product.query.order_by(Product.created_at.desc()).all()
#     return jsonify({
#         "data": [product_to_vue(p) for p in products],
#         "msg": "Products list loaded"
#     }), 200



@admin_bp.route('/admin/products', methods=['GET'])
@jwt_required()
def list_products():
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    category = request.args.get("category")
    active = request.args.get("active")
    search = request.args.get("search")

    query = Product.query

    # Filter: category
    if category:
        cat = Category.query.filter_by(name=category).first()
        if cat:
            query = query.filter(Product.category_id == cat.id)

    # Filter: active status
    if active is not None:
        query = query.filter(Product.is_active == (active.lower() == "true"))

    # Search by name
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    pagination = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=limit, error_out=False
    )

    return jsonify({
        "msg": "Products list loaded",
        "total": pagination.total,
        "page": page,
        "pages": pagination.pages,
        "data": [product_to_admin_vue(p) for p in pagination.items]
    }), 200


# ------------------ CREATE product ------------------ #
## Testing Done

@admin_bp.route('/admin/products', methods=['POST'])
@jwt_required()
def create_product():
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    data = request.get_json()

    required_fields = ["name", "category_id", "price", "sku"]
    for f in required_fields:
        if not data.get(f):
            return jsonify({"msg": f"{f} is required"}), 400

    # validate category
    category = Category.query.get(data["category_id"])
    if not category:
        return jsonify({"msg": "Invalid category"}), 400

    # check SKU uniqueness
    if Product.query.filter_by(sku=data["sku"]).first():
        return jsonify({"msg": "SKU already exists"}), 400

    # generate unique slug
    base_slug = slugify(data["name"])
    slug = base_slug
    count = 1
    while Product.query.filter_by(slug=slug).first():
        slug = f"{base_slug}-{count}"
        count += 1

    new_prod = Product(
        name=data["name"],
        slug=slug,
        sku=data["sku"],
        description=data.get("description"),
        price=data["price"],
        sale_price=data.get("sale_price"),
        stock_quantity=data.get("stock", 0),
        category_id=category.id,
        is_featured=data.get("is_featured", False),
        is_active=data.get("active", True)
    )

    db.session.add(new_prod)
    db.session.commit()

    # image
    if data.get("image"):
        img = ProductImage(
            product_id=new_prod.id,
            image_url=data["image"],
            is_primary=True
        )
        db.session.add(img)
        db.session.commit()

    return jsonify({
        "msg": "Product created successfully",
        "data": product_to_admin_vue(new_prod)
    }), 201


# ------------------ UPDATE product ------------------ #
## Testing Done


@admin_bp.route('/admin/products/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    prod = Product.query.get(id)
    if not prod:
        return jsonify({"msg": "Product not found"}), 404

    data = request.get_json()

    # Update name & slug
    if data.get("name") and data["name"] != prod.name:
        prod.name = data["name"]
        prod.slug = data["name"].lower().replace(" ", "-")

    # Basic fields
    prod.price = data.get("price", prod.price)
    prod.sale_price = data.get("salePrice", prod.sale_price)
    prod.stock_quantity = data.get("stock", prod.stock_quantity)
    prod.is_active = data.get("active", prod.is_active)
    prod.is_featured = data.get("is_featured", prod.is_featured)
    prod.sku = data.get("sku", prod.sku)
    prod.description = data.get("description", prod.description)

    # Update category
    if data.get("category"):
        category = Category.query.filter_by(name=data["category"]).first()
        if not category:
            return jsonify({"msg": "Category not found"}), 400
        prod.category_id = category.id

    # Update image
    if data.get("image"):
        img = ProductImage.query.filter_by(product_id=id, is_primary=True).first()
        if img:
            img.image_url = data["image"]
        else:
            new_img = ProductImage(
                product_id=id,
                image_url=data["image"],
                is_primary=True
            )
            db.session.add(new_img)

    db.session.commit()

    return jsonify({
        "msg": "Product updated",
        "data": product_to_admin_vue(prod)
    }), 200


# ------------------ DELETE product ------------------ #

## Testing Done

## This api is hard deleteing the products :--
# @admin_bp.route('/admin/products/<int:id>', methods=['DELETE'])
# @jwt_required()
# def delete_product(id):
#     if not get_admin_user():
#         return jsonify({"msg": "Admin access required"}), 401

#     prod = Product.query.get(id)
#     if not prod:
#         return jsonify({"msg": "Product not found"}), 404

#     # cascade deletes images/attributes if configured, else delete manually
#     db.session.delete(prod)
#     db.session.commit()

#     return jsonify({"msg": "Product deleted"}), 200


## This api just un-actice the product, remove from visiblity :--

@admin_bp.route('/admin/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    prod = Product.query.get(id)
    if not prod:
        return jsonify({"msg": "Product not found"}), 404

    # Soft delete
    prod.is_active = False
    db.session.commit()

    return jsonify({
        "msg": "Product disabled successfully",
        "data": product_to_admin_vue(prod)
    }), 200




# ----------------------------------------------------------------------
# 5. ORDERS MANAGEMENT
# ----------------------------------------------------------------------



# ----------------------------------------------------------------------
# 5. ORDERS MANAGEMENT (Vue Friendly)  |  API TESTING DONE
# ----------------------------------------------------------------------

# ---------- Helper: Make initials ---------- #
def make_initials(name):
    return ''.join([word[0] for word in name.split()]).upper()[:2]


# ---------- Helper: Convert DB to Vue Order Format ---------- #
def order_to_vue(order):
    user = User.query.get(order.user_id)

    # Full name
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()

    # Items count
    items_count = db.session.query(func.count(OrderItem.id)).filter(OrderItem.order_id == order.id).scalar()

    return {
        "id": f"#ORD-{order.id:04d}",
        "customer": full_name,
        "initials": make_initials(full_name),
        "email": user.email,
        "date": order.created_at.strftime("%b %d, %Y") if order.created_at else "",
        "itemsCount": items_count,
        "total": f"${order.total_amount:.2f}",
        "status": order.status
    }



##  TESTING DONE
# ------------------ GET all orders ------------------ #
@admin_bp.route('/admin/orders', methods=['GET'])
@jwt_required()
def list_orders():
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    orders = Order.query.order_by(Order.created_at.desc()).all()
    return jsonify({
        "data": [order_to_vue(o) for o in orders],
        "msg": "Orders list loaded"
    }), 200



##  TESTING DONE
# ------------------ Get single order details ------------------ #
@admin_bp.route('/admin/orders/<int:id>', methods=['GET'])
@jwt_required()
def get_single_order(id):
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    order = Order.query.get(id)
    if not order:
        return jsonify({"msg": "Order not found"}), 404

    return jsonify({
        "data": order_to_vue(order),
        "msg": "Order details"
    }), 200


## TESTING DONE
# ------------------ Update order status ------------------ #
@admin_bp.route('/admin/orders/<int:id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(id):
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    order = Order.query.get(id)
    if not order:
        return jsonify({"msg": "Order not found"}), 404

    data = request.get_json()
    new_status = data.get("status")

    valid_statuses = ['New', 'Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']
    if new_status not in valid_statuses:
        return jsonify({"msg": f"Invalid status. Valid: {valid_statuses}"}), 400

    order.status = new_status
    db.session.commit()

    return jsonify({
        "msg": f"Order updated to {new_status}",
        "data": order_to_vue(order)
    }), 200


##  TESTING DONE
# ------------------ DELETE order ------------------ #
@admin_bp.route('/admin/orders/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_order(id):
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    order = Order.query.get(id)
    if not order:
        return jsonify({"msg": "Order not found"}), 404

    if order.status in ['Shipped', 'Delivered']:
        return jsonify({"msg": "Cannot delete shipped/delivered orders"}), 400

    db.session.delete(order)
    db.session.commit()
    return jsonify({"msg": "Order deleted successfully"}), 200






# ----------------------------------------------------------------------
# 6. MESSAGES / CUSTOMER QUERIES
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# 6. MESSAGES / CUSTOMER QUERIES (Vue Compatible)   |  API TESTING DONE
# ----------------------------------------------------------------------

# ------------ Helpers ------------ #

STATUS_MAP = ["New", "In Progress", "Resolved", "Archived"]

# Format timestamps like Vue mock data
def format_relative_time(dt):
    diff = datetime.utcnow() - dt

    if diff.seconds < 60:
        return "Just now"
    if diff.seconds < 3600:
        mins = diff.seconds // 60
        return f"{mins} mins ago"
    if diff.seconds < 86400:
        hrs = diff.seconds // 3600
        return f"{hrs} hours ago"

    days = diff.days
    if days == 1:
        return "Yesterday"
    return dt.strftime("%b %d")  # e.g. "Dec 28"

# Full formatted date
def full_date_format(dt):
    return dt.strftime("%b %d, %Y at %I:%M %p")


# Convert DB to Vue format
def message_to_vue(msg):
    return {
        "id": msg.id,
        "name": msg.name,
        "email": msg.email,
        "subject": msg.subject,
        "message": msg.message,
        "status": msg.status,
        "date": format_relative_time(msg.created_at),
        "fullDate": full_date_format(msg.created_at)
    }


# ------------ Routes ------------ #

##  TESTING DONE
@admin_bp.route('/admin/messages', methods=['GET'])
@jwt_required()
def list_messages():
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    msgs = Message.query.order_by(Message.created_at.desc()).all()
    return jsonify({
        "data": [message_to_vue(m) for m in msgs],
        "msg": "Messages list loaded"
    }), 200


##  TESTING DONE
@admin_bp.route('/admin/messages/<int:id>', methods=['GET'])
@jwt_required()
def get_single_message(id):
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    msg = Message.query.get(id)
    if not msg:
        return jsonify({"msg": "Message not found"}), 404

    return jsonify({"data": message_to_vue(msg)}), 200



##  TESTING DONE
@admin_bp.route('/admin/messages/<int:id>/status', methods=['PUT'])
@jwt_required()
def update_message_status(id):
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    msg = Message.query.get(id)
    if not msg:
        return jsonify({"msg": "Message not found"}), 404

    data = request.get_json()
    new_status = data.get("status")

    if new_status not in STATUS_MAP:
        return jsonify({"msg": f"Invalid status. Allowed: {STATUS_MAP}"}), 400

    msg.status = new_status
    db.session.commit()

    return jsonify({
        "msg": f"Message status updated to {new_status}",
        "data": message_to_vue(msg)
    }), 200


##  TESTING DONE
@admin_bp.route('/admin/messages/archive-resolved', methods=['PUT'])
@jwt_required()
def archive_resolved_messages():
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    updated = Message.query.filter_by(status="Resolved").update({"status": "Archived"})
    db.session.commit()

    return jsonify({"msg": f"{updated} messages archived"}), 200



##  TESTING DONE
@admin_bp.route('/admin/messages/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_message(id):
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    msg = Message.query.get(id)
    if not msg:
        return jsonify({"msg": "Message not found"}), 404

    db.session.delete(msg)
    db.session.commit()

    return jsonify({"msg": "Message deleted"}), 200





## ADMIN DASHBOARD API :--
# 1️⃣ Dashboard Summary API :--

# app/resources/dashboard/admin_dashboard.py


##  TESTING DONE
@admin_bp.route('/admin/dashboard', methods=['GET'])
@jwt_required()
def dashboard_overview():
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    total_users = User.query.count()
    active_products = Product.query.filter_by(is_active=True).count()
    total_orders = Order.query.count()

    # total revenue - only paid/delivered orders (optional)
    total_revenue = db.session.query(func.sum(Order.total_amount)).scalar() or 0

    response = {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "active_products": active_products,
        "registered_users": total_users
    }
    return jsonify({"data": response, "msg": "Dashboard stats"}), 200




##  TESTING DONE
# 2️⃣ Recent Orders API
@admin_bp.route('/admin/dashboard/recent-orders', methods=['GET'])
@jwt_required()
def recent_orders():
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()

    formatted_orders = []
    for o in orders:
        formatted_orders.append({
            "id": f"#{o.id}",                       # "#8392"
            "customer": f"{o.user.first_name} {o.user.last_name if o.user.last_name else ''}".strip(),
            "initials": (o.user.first_name[0] + (o.user.last_name[0] if o.user.last_name else '')).upper(),
            "amount": f"${o.total_amount:.2f}",
            "status": o.status,
            "created_at": o.created_at.isoformat()
        })

    return jsonify({"data": formatted_orders, "msg": "Recent 5 orders"}), 200





# CATEGORY CREATION API  | Testing Done

# app/resources/productlisting/category_operations.py


# Utility function
def slugify(text):
    return text.lower().strip().replace(" ", "-")

# ----------------------------------------------------------
# 1️⃣ Get all categories  | Testing done
# ----------------------------------------------------------
@admin_bp.route('/admin/categories', methods=['GET'])
@jwt_required()
def list_categories():
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    categories = Category.query.order_by(Category.name.asc()).all()
    return jsonify({
        "msg": "Categories list",
        "data": [c.serialize() for c in categories]
    }), 200


# ----------------------------------------------------------
# 2️⃣ Create category   | Testing Done
# ----------------------------------------------------------

@admin_bp.route('/admin/categories', methods=['POST'])
@jwt_required()
def create_category():
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    data = request.get_json()
    name = data.get("name")
    parent_id = data.get("parent_id")  # optional

    if not name:
        return jsonify({"msg": "Category name is required"}), 400

    slug = slugify(name)

    # avoid duplicates
    if Category.query.filter((Category.name == name) | (Category.slug == slug)).first():
        return jsonify({"msg": "Category already exists"}), 400

    new_cat = Category(
        name=name,
        slug=slug,
        description=data.get("description"),
        image_url=data.get("image_url"),
        parent_id=parent_id
    )

    db.session.add(new_cat)
    db.session.commit()

    return jsonify({"msg": "Category created", "data": new_cat.serialize()}), 201


# ----------------------------------------------------------
# 3️⃣ Update category  | Testing Done
# ----------------------------------------------------------
@admin_bp.route('/admin/categories/<int:id>', methods=['PUT'])
@jwt_required()
def update_category(id):
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    cat = Category.query.get(id)
    if not cat:
        return jsonify({"msg": "Category not found"}), 404

    data = request.get_json()

    new_name = data.get("name", cat.name)

    # If category name changes, update slug
    if new_name != cat.name:
        cat.name = new_name
        cat.slug = slugify(new_name)

    cat.description = data.get("description", cat.description)
    cat.image_url = data.get("image_url", cat.image_url)
    cat.parent_id = data.get("parent_id", cat.parent_id)

    db.session.commit()

    return jsonify({"msg": "Category updated", "data": cat.serialize()}), 200


# ----------------------------------------------------------
# 4️⃣ Delete category (only if no products)   |  Testing Done
# ----------------------------------------------------------
@admin_bp.route('/admin/categories/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    cat = Category.query.get(id)
    if not cat:
        return jsonify({"msg": "Category not found"}), 404

    # Prevent deletion if products exist
    if len(cat.products) > 0:
        return jsonify({"msg": "Cannot delete category with products"}), 400

    db.session.delete(cat)
    db.session.commit()

    return jsonify({"msg": "Category deleted"}), 200


# ----------------------------------------------------------
# 5️⃣ Get categories formatted for Vue dropdown
# (id + name only — faster UI load)      |  Testing Done
# ----------------------------------------------------------
@admin_bp.route('/admin/categories/dropdown', methods=['GET'])
@jwt_required()
def category_dropdown():
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    categories = Category.query.order_by(Category.name.asc()).all()
    return jsonify({
        "msg": "Dropdown list",
        "data": [{"id": c.id, "name": c.name} for c in categories]
    }), 200




#  ProductAttribute Table :--

@admin_bp.route('/admin/products/<int:product_id>/attributes', methods=['POST'])
@jwt_required()
def add_product_attribute(product_id):
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"msg": "Product not found"}), 404

    data = request.get_json()
    key = data.get("key")
    value = data.get("value")

    if not key or not value:
        return jsonify({"msg": "key and value are required"}), 400

    # Optional: prevent duplicate attribute keys
    existing = ProductAttribute.query.filter_by(
        product_id=product_id, key=key
    ).first()
    if existing:
        return jsonify({"msg": "Attribute already exists"}), 400

    attr = ProductAttribute(
        product_id=product_id,
        key=key,
        value=value
    )

    db.session.add(attr)
    db.session.commit()

    return jsonify({
        "msg": "Attribute added",
        "data": attr.serialize()
    }), 201




@admin_bp.route('/admin/products/<int:product_id>/attributes', methods=['GET'])
@jwt_required()
def list_product_attributes(product_id):
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"msg": "Product not found"}), 404

    attributes = ProductAttribute.query.filter_by(product_id=product_id).all()

    return jsonify({
        "data": [a.serialize() for a in attributes]
    }), 200





@admin_bp.route('/admin/product-attributes/<int:id>', methods=['PUT'])
@jwt_required()
def update_product_attribute(id):
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    attr = ProductAttribute.query.get(id)
    if not attr:
        return jsonify({"msg": "Attribute not found"}), 404

    data = request.get_json()
    value = data.get("value")

    if not value:
        return jsonify({"msg": "value is required"}), 400

    attr.value = value
    db.session.commit()

    return jsonify({
        "msg": "Attribute updated",
        "data": attr.serialize()
    }), 200







@admin_bp.route('/admin/product-attributes/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product_attribute(id):
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    attr = ProductAttribute.query.get(id)
    if not attr:
        return jsonify({"msg": "Attribute not found"}), 404

    db.session.delete(attr)
    db.session.commit()

    return jsonify({"msg": "Attribute deleted"}), 200
