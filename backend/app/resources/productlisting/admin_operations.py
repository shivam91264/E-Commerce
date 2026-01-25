from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from datetime import datetime
from app.models.models import db, User, Product, Category, Order, OrderItem, Message, ProductImage, ProductAttribute, Review
import csv
from io import StringIO
from flask import make_response
from app.models.models import Address  # Ensure Address model is imported



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
@admin_bp.route('/admin/order_status', methods=['GET'])
@jwt_required()
def order_status():
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    # FIX: Added 'Shipped' to the list so it gets counted
    statuses = ['Delivered', 'Shipped', 'Pending', 'Processing', 'Cancelled']
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

    # Logic for "Last Login": 
    # Since User model lacks 'last_login', we use 'updated_at' as a proxy.
    # If updated_at is None, we default to "Never".
    last_active = user.updated_at.strftime("%b %d, %H:%M") if user.updated_at else "Never"

    return {
        "id": user.id,
        "name": full_name,
        "email": user.email,
        "phone": user.phone,
        "role": "Admin" if user.is_admin else "User",
        "ordersCount": orders_count,
        "active": user.is_active,
        "joinedDate": user.created_at.strftime("%b %d, %Y") if user.created_at else None,
        "last_login": last_active  # <--- Added for Vue Drawer
    }


# ---------------------- GET ALL USERS ---------------------- #


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




## Not tested and not mentioned in  Adminapi.md

@admin_bp.route('/admin/users/export', methods=['GET'])
@jwt_required()
def export_users():
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    # Fetch all users sorted by newest
    users = User.query.order_by(User.created_at.desc()).all()

    # Create CSV in memory
    si = StringIO()
    cw = csv.writer(si)
    
    # CSV Header
    cw.writerow(['User ID', 'Name', 'Email', 'Phone', 'Role', 'Status', 'Joined Date'])

    # CSV Data
    for user in users:
        full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        cw.writerow([
            user.id,
            full_name,
            user.email,
            user.phone or "N/A",
            "Admin" if user.is_admin else "User",
            "Active" if user.is_active else "Blocked",
            user.created_at.strftime("%Y-%m-%d") if user.created_at else ""
        ])

    # Create Response
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=users_export.csv"
    output.headers["Content-type"] = "text/csv"
    return output



## Not tested and not mentioned in  Adminapi.md

# ---------------------- GET USER ADDRESSES ---------------------- #
@admin_bp.route('/admin/users/<int:user_id>/addresses', methods=['GET'])
@jwt_required()
def get_user_addresses(user_id):
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Fetch addresses linked to this user
    addresses = Address.query.filter_by(user_id=user.id).all()
    
    data = []
    for addr in addresses:
        # FIX: Combine address_line1 and address_line2 correctly
        full_address_str = addr.address_line1
        if addr.address_line2:
            full_address_str += f", {addr.address_line2}"
        
        full_address_str += f", {addr.city}, {addr.state} {addr.zip_code}"

        data.append({
            "id": addr.id,
            "type": addr.label or "Home",  # FIX: Use 'label' from your Model
            "address": full_address_str,   # FIX: Constructed string
            "country": addr.country
        })

    return jsonify({
        "msg": "User addresses loaded",
        "data": data
    }), 200



## Not tested and not mentioned in  Adminapi.md

@admin_bp.route('/admin/users/<int:user_id>/orders', methods=['GET'])
@jwt_required()
def get_user_orders(user_id):
    if not get_admin_user():
        return jsonify({"msg": "Admin access required"}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Fetch orders for this specific user
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()

    data = []
    for o in orders:
        data.append({
            "id": f"#ORD-{o.id:04d}",
            "date": o.created_at.strftime("%b %d, %Y"),
            "total": f"${o.total_amount:.2f}",
            "status": o.status,
            "items_count": len(o.items) if o.items else 0
        })

    return jsonify({
        "msg": f"Order history for {user.first_name}",
        "data": data
    }), 200



# ----------------------------------------------------------------------
# 4. PRODUCTS MANAGEMENT
# ----------------------------------------------------------------------



# ----------------------------------------------------------------------
# 4. PRODUCTS MANAGEMENT (Updated for Vue Connection)
# ----------------------------------------------------------------------

# ---------- Helper: Convert DB Product to Vue format ---------- #
def product_to_admin_vue(product):
    category = Category.query.get(product.category_id)

    # Get all images, sorted by display_order
    images_query = ProductImage.query.filter_by(product_id=product.id).order_by(ProductImage.display_order).all()
    
    # Create list of URLs for frontend
    image_urls = [img.image_url for img in images_query]
    
    # Fallback for table display (primary image)
    primary_img_url = image_urls[0] if image_urls else "https://via.placeholder.com/120"

    return {
        "id": product.id,
        "name": product.name,
        "category": category.name if category else "Uncategorized",
        "category_id": product.category_id,
        "description": product.description,
        "sku": product.sku,
        "price": product.price,
        "sale_price": product.sale_price,
        "stock_quantity": product.stock_quantity,
        "is_active": product.is_active,
        "image": primary_img_url, # Single string for Table View
        "images": image_urls      # Array for Modal View (Edit Mode)
    }

# ------------------ GET all products ------------------ #
@admin_bp.route('/admin/products', methods=['GET'])
@jwt_required()
def list_products():
    # if not get_admin_user(): return jsonify({"msg": "Admin access required"}), 401

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    category = request.args.get("category")
    active = request.args.get("active")
    search = request.args.get("search")

    query = Product.query

    if category:
        cat = Category.query.filter_by(name=category).first()
        if cat:
            query = query.filter(Product.category_id == cat.id)

    if active is not None:
        query = query.filter(Product.is_active == (active.lower() == "true"))

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
# ------------------ CREATE product ------------------ #
@admin_bp.route('/admin/products', methods=['POST'])
@jwt_required()
def create_product():
    # if not get_admin_user(): return jsonify({"msg": "Admin access required"}), 401

    data = request.get_json()

    # Validate Required Fields
    required = ["name", "category_id", "price", "stock_quantity"]
    for f in required:
        if f not in data:
            return jsonify({"msg": f"{f} is required"}), 400

    # Validate Category
    category = Category.query.get(data["category_id"])
    if not category:
        return jsonify({"msg": "Invalid category ID"}), 400

    # Validate SKU Uniqueness
    if data.get("sku") and Product.query.filter_by(sku=data["sku"]).first():
        return jsonify({"msg": "SKU already exists"}), 400

    # Generate Slug
    base_slug = slugify(data["name"])
    slug = base_slug
    count = 1
    while Product.query.filter_by(slug=slug).first():
        slug = f"{base_slug}-{count}"
        count += 1

    # Create Product
    new_prod = Product(
        name=data["name"],
        slug=slug,
        sku=data.get("sku"),
        description=data.get("description"),
        price=float(data["price"]),
        sale_price=float(data["sale_price"]) if data.get("sale_price") else None,
        stock_quantity=int(data["stock_quantity"]),
        category_id=category.id,
        is_active=data.get("is_active", True)
    )

    db.session.add(new_prod)
    db.session.commit()

    # --- FIX: Handle Multiple Images ---
    # The frontend sends: "images": ["url1", "url2"]
    images_list = data.get("images", []) 
    
    # Fallback: check if frontend sent old single "image" key
    if not images_list and data.get("image"):
        images_list = [data["image"]]

    for index, img_url in enumerate(images_list):
        if img_url.strip(): # Avoid empty strings
            new_img = ProductImage(
                product_id=new_prod.id, 
                image_url=img_url, 
                is_primary=(index == 0), # First image is primary
                display_order=index
            )
            db.session.add(new_img)
    
    db.session.commit()

    return jsonify({
        "msg": "Product created successfully",
        "data": product_to_admin_vue(new_prod)
    }), 201




# ------------------ UPDATE product ------------------ #
@admin_bp.route('/admin/products/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    # if not get_admin_user(): return jsonify({"msg": "Admin access required"}), 401

    prod = Product.query.get(id)
    if not prod:
        return jsonify({"msg": "Product not found"}), 404

    data = request.get_json()

    # --- FIX 1: Check SKU Uniqueness (Excluding current product) ---
    if "sku" in data and data["sku"]:
        existing_sku = Product.query.filter_by(sku=data["sku"]).first()
        if existing_sku and existing_sku.id != id:
            return jsonify({"msg": "SKU already exists"}), 400

    # Update Basic Fields
    if "name" in data: prod.name = data["name"]
    
    if "category_id" in data:
        cat = Category.query.get(data["category_id"])
        if cat: prod.category_id = cat.id

    if "price" in data: prod.price = float(data["price"])
    if "sale_price" in data: 
        prod.sale_price = float(data["sale_price"]) if data["sale_price"] else None
    
    if "stock_quantity" in data: prod.stock_quantity = int(data["stock_quantity"])
    if "is_active" in data: prod.is_active = bool(data["is_active"])
    if "sku" in data: prod.sku = data["sku"]
    if "description" in data: prod.description = data["description"]

    # --- FIX 2: Safer Image Update Logic ---
    if "images" in data:
        # Delete existing images using explicit session synchronization setting
        ProductImage.query.filter_by(product_id=id).delete(synchronize_session=False)
        
        # Add new images
        images_list = data["images"]
        for index, img_url in enumerate(images_list):
            if img_url and img_url.strip():
                new_img = ProductImage(
                    product_id=prod.id, 
                    image_url=img_url, 
                    is_primary=(index == 0), 
                    display_order=index
                )
                db.session.add(new_img)

    try:
        db.session.commit()
        return jsonify({
            "msg": "Product updated",
            "data": product_to_admin_vue(prod)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Update failed", "error": str(e)}), 500



# ------------------ DELETE product ------------------ #
@admin_bp.route('/admin/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    # if not get_admin_user(): return jsonify({"msg": "Admin access required"}), 401

    prod = Product.query.get(id)
    if not prod:
        return jsonify({"msg": "Product not found"}), 404

    try:
        db.session.delete(prod)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"msg": "Cannot delete product (likely has orders)"}), 400

    return jsonify({"msg": "Product deleted successfully"}), 200



# ----------------------------------------------------------------------
# 5. ORDERS MANAGEMENT
# ----------------------------------------------------------------------



# ----------------------------------------------------------------------
# 5. ORDERS MANAGEMENT (Vue Friendly)
# ----------------------------------------------------------------------

# ---------- Helper: Make initials ---------- #
def make_initials(name):
    if not name: return "NA"
    return ''.join([word[0] for word in name.split()]).upper()[:2]

# ---------- Helper: Order to Vue Dict ---------- #
def order_to_vue(order):
    user = User.query.get(order.user_id)
    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip() if user else "Unknown Customer"

    # 1. Get Actual Items List (Required for the Drawer)
    items_list = []
    for item in order.items:
        # Fetch product image safely
        image_url = "https://via.placeholder.com/100"
        if item.product and item.product.images:
            # Try to find primary, otherwise first
            primary = next((img for img in item.product.images if img.is_primary), item.product.images[0])
            image_url = primary.image_url

        items_list.append({
            "name": item.product_name,
            "quantity": item.quantity,
            "price": item.price_at_purchase,
            "image": image_url
        })

    # 2. Calculate Financials
    subtotal = order.total_amount - order.shipping_cost - order.tax_amount

    return {
        "id": f"#ORD-{order.id:04d}",
        "db_id": order.id, # <--- REQUIRED for Status Update API
        "customer": full_name,
        "initials": make_initials(full_name),
        "email": user.email if user else "",
        "date": order.created_at.strftime("%b %d, %Y") if order.created_at else "",
        
        # List data
        "items": items_list, 
        "itemsCount": len(items_list),

        # Financials
        "total": f"${order.total_amount:.2f}",
        "subtotal": f"${subtotal:.2f}",
        "shipping": f"${order.shipping_cost:.2f}",
        "tax": f"${order.tax_amount:.2f}",
        
        "status": order.status
    }

# ------------------ GET all orders ------------------ #
@admin_bp.route('/admin/orders', methods=['GET'])
@jwt_required()
def list_orders():
    # if not get_admin_user(): return jsonify({"msg": "Admin access required"}), 401
    
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return jsonify({
        "data": [order_to_vue(o) for o in orders],
        "msg": "Orders list loaded"
    }), 200

# ------------------ Update order status ------------------ #
@admin_bp.route('/admin/orders/<int:id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(id):
    # if not get_admin_user(): return jsonify({"msg": "Admin access required"}), 401

    order = Order.query.get(id)
    if not order:
        return jsonify({"msg": "Order not found"}), 404

    data = request.get_json()
    new_status = data.get("status")

    # Optional: Add validation logic here
    order.status = new_status
    db.session.commit()

    return jsonify({
        "msg": f"Order updated to {new_status}",
        "data": order_to_vue(order)
    }), 200


### This api will not be used
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


# Corrected Helper Function
def format_relative_time(dt):
    now = datetime.utcnow()
    diff = now - dt

    # 1. Check if it's been more than 24 hours FIRST
    if diff.days > 0:
        if diff.days == 1:
            return "Yesterday"
        return dt.strftime("%b %d")  # e.g. "Jan 02"

    # 2. If it's less than 24 hours, check seconds
    seconds = diff.seconds

    if seconds < 60:
        return "Just now"
    if seconds < 3600:
        mins = seconds // 60
        return f"{mins} mins ago"
    
    # 3. Hours logic
    hrs = seconds // 3600
    return f"{hrs} hours ago"


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
