from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
from datetime import datetime
import uuid

from app.extensions import cache


from app.resources.productlisting.admin_operations import product_to_admin_vue
from app.utils.serializers import wishlist_to_vue
from app.utils.serializers import cart_item_to_vue
from app.utils.serializers import product_to_user_vue
from app.utils.serializers import product_card_to_vue
from app.utils.serializers import product_card_dto
from app.utils.serializers import shop_product_card_dto




# Import extensions and models (Assuming app structure)
# Update 'app' import if you define cache elsewhere
from app.models.models import db, User, Product, Category, CartItem, Review , Order, OrderItem, Message, ProductImage, ProductAttribute,Wishlist, Address

user_bp = Blueprint('user', __name__)

# ----------------------------------------------------------------------
# HELPER: Get Current User
# ----------------------------------------------------------------------
def get_current_user():
    """Helper to fetch user based on JWT identity (email)."""
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    return user

# ----------------------------------------------------------------------
# 👤 USER PROFILE  |  ProfileView.vue page api changed   | API TESTING DONE
# ----------------------------------------------------------------------

@user_bp.route('/user/profile', methods=['GET'], endpoint='user_profile_get')
@jwt_required()
def get_user_profile():
    user = get_current_user()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({
        "msg": "Profile fetched",
        "data": {
            "name": f"{user.first_name} {user.last_name}".strip(),
            "email": user.email,
            "phone": user.phone,
            "gender": user.gender,
            "dob": user.dob.isoformat() if user.dob else None
        }
    }), 200



@user_bp.route('/user/profile', methods=['PATCH'], endpoint='user_profile_update')
@jwt_required()
def update_user_profile():
    user = get_current_user()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json()

    # Handle name → first + last
    if 'name' in data:
        parts = data['name'].strip().split(' ', 1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ""

    if 'phone' in data:
        user.phone = data['phone']

    if 'gender' in data:
        user.gender = data['gender']

    if 'dob' in data:
        try:
            user.dob = datetime.strptime(data['dob'], "%Y-%m-%d")
        except ValueError:
            return jsonify({"msg": "Invalid date format"}), 400

    db.session.commit()

    return jsonify({
        "msg": "Profile updated successfully",
        "data": {
            "name": f"{user.first_name} {user.last_name}".strip(),
            "email": user.email,
            "phone": user.phone,
            "gender": user.gender,
            "dob": user.dob.isoformat() if user.dob else None
        }
    }), 200

# ----------------------------------------------------------------------
# 🏠 ADDRESSES   |  AddressesView.vue page api changed |  TESTING DONE 
# ----------------------------------------------------------------------

## TESTING DONE
@user_bp.route('/user/addresses', methods=['GET'])
@jwt_required()
def list_addresses():
    user = get_current_user()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({
        "msg": "Addresses fetched",
        "data": [
            {
                "id": a.id,
                "name": a.full_name,
                "phone": a.phone,
                "line1": a.address_line1,
                "line2": a.address_line2,
                "city": a.city,
                "state": a.state,
                "zip": a.zip_code,
                "country": a.country,
                "label": a.label,
                "isDefault": a.is_default
            }
            for a in user.addresses
        ]
    }), 200


## TESTING DONE
@user_bp.route('/user/addresses', methods=['POST'])
@jwt_required()
def add_address():
    user = get_current_user()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json()

    required = ['name', 'phone', 'line1', 'city', 'state', 'zip', 'country']
    if not all(k in data for k in required):
        return jsonify({"msg": "Missing required fields"}), 400

    new_addr = Address(
        user_id=user.id,
        full_name=data['name'],
        phone=data['phone'],
        address_line1=data['line1'],
        address_line2=data.get('line2'),
        city=data['city'],
        state=data['state'],
        zip_code=data['zip'],
        country=data['country'],
        label=data.get('label', 'Home'),
        is_default=data.get('isDefault', False)
    )

    if new_addr.is_default:
        Address.query.filter_by(user_id=user.id).update({"is_default": False})

    db.session.add(new_addr)
    db.session.commit()

    return jsonify({"msg": "Address added"}), 201



## TESTING DONE :--
@user_bp.route('/user/addresses/<int:id>', methods=['PUT'])
@jwt_required()
def update_address(id):
    user = get_current_user()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    addr = Address.query.get(id)
    if not addr or addr.user_id != user.id:
        return jsonify({"msg": "Address not found"}), 404

    data = request.get_json()

    addr.full_name = data.get('name', addr.full_name)
    addr.phone = data.get('phone', addr.phone)
    addr.address_line1 = data.get('line1', addr.address_line1)
    addr.address_line2 = data.get('line2', addr.address_line2)
    addr.city = data.get('city', addr.city)
    addr.state = data.get('state', addr.state)
    addr.zip_code = data.get('zip', addr.zip_code)
    addr.country = data.get('country', addr.country)
    addr.label = data.get('label', addr.label)

    db.session.commit()
    return jsonify({"msg": "Address updated"}), 200



## TESTING DONE :--
@user_bp.route('/user/addresses/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_address(id):
    user = get_current_user()
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    addr = Address.query.get(id)
    if not addr or addr.user_id != user.id:
        return jsonify({"msg": "Address not found"}), 404
        
    db.session.delete(addr)
    db.session.commit()
    return jsonify({"msg": "Address deleted"})



## TESTING DONE :--
@user_bp.route('/user/addresses/<int:id>/default', methods=['PUT'])
@jwt_required()
def set_default_address(id):
    user = get_current_user()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    addr = Address.query.get(id)
    if not addr or addr.user_id != user.id:
        return jsonify({"msg": "Address not found"}), 404

    # Unset all
    Address.query.filter_by(user_id=user.id).update({"is_default": False})

    addr.is_default = True
    db.session.commit()

    return jsonify({"msg": "Default address set"}), 200


# ----------------------------------------------------------------------
# 🛍 PRODUCTS (Read Only - Cached)  #  | ProductDetails.vue page api changed  |  API TESTING DONE 
# ----------------------------------------------------------------------

def product_to_details_view(product):
    primary_image = None
    gallery = []

    # 1. Image Logic
    for img in product.images:
        gallery.append(img.image_url)
        if img.is_primary:
            primary_image = img.image_url

    if not primary_image and gallery:
        primary_image = gallery[0]
    elif not gallery:
        primary_image = "https://via.placeholder.com/600" # Fallback
        gallery = [primary_image]

    # 2. Attribute Logic (Assuming ProductAttribute model has key/value)
    # We filter out 'care' and 'color' to put them in specific fields
    specs_dict = {}
    care_instruction = "Clean with a dry cloth." # Default
    colors_list = []

    for attr in product.attributes:
        k = attr.key.lower()
        v = attr.value
        
        if k == 'care':
            care_instruction = v
        elif k == 'color':
            # Try to map common names to hex, or just pass the name
            # You can expand this mapping or store hex in DB
            color_map = {"black": "#000", "white": "#fff", "red": "#f00", "blue": "#00f"}
            hex_code = color_map.get(v.lower(), "#ccc") 
            colors_list.append({"name": v, "hex": hex_code})
        else:
            specs_dict[attr.key] = v

    return {
        "id": product.id,
        "name": product.name,
        "tagline": product.description[:50] + "..." if product.description else "Premium Quality",
        "sku": product.sku,
        "price": product.price,
        "originalPrice": product.sale_price if product.sale_price else None,
        "inStock": product.stock_quantity > 0,
        "description": product.description,
        "badge": "Best Seller" if product.is_featured else None,
        "images": gallery,
        "specs": specs_dict,
        "care": care_instruction,
        "colors": colors_list,
        "rating": 4.5, # Static for now if reviews table empty
        "reviewCount": 0
    }




## TESTING DONE :--
@user_bp.route('/products/<int:id>', methods=['GET'])
@cache.cached(timeout=60)
def get_product(id):
    product = Product.query.get(id)

    if not product or not product.is_active:
        return jsonify({"msg": "Product not found"}), 404

    return jsonify({
        "msg": "Product details loaded",
        "data": product_to_details_view(product)
    }), 200


## TESTING DONE :--
@user_bp.route('/products/<int:id>/related', methods=['GET'])
@cache.cached(timeout=60)
def related_products(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"data": []})

    related = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != id,
        Product.is_active == True
    ).limit(6).all()

    return jsonify({
        "data": [
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "image": p.images[0].image_url if p.images else None
            } for p in related
        ]
    }), 200



## TESTING DONE :--
@user_bp.route('/products', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def list_products():
    products = Product.query.filter(
        Product.is_active == True
    ).all()

    return jsonify({
        "data": [product_to_details_view(p) for p in products],
        "msg": "Products fetched"
    })




# ----------------------------------------------------------------------
# ❤️ WISHLIST  |  WishlistView.vue page api changed
# ----------------------------------------------------------------------


## TESTING DONE :--
@user_bp.route('/user/wishlist', methods=['GET'])
@jwt_required()
def get_wishlist():
    user = get_current_user()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({
        "msg": "Wishlist fetched",
        "data": [wishlist_to_vue(w) for w in user.wishlist_items]
    }), 200


## TESTING DONE :--
@user_bp.route('/user/wishlist/<int:product_id>', methods=['POST'])
@jwt_required()
def add_to_wishlist(product_id):
    user = get_current_user()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    exists = Wishlist.query.filter_by(
        user_id=user.id,
        product_id=product_id
    ).first()

    if exists:
        return jsonify({"msg": "Product already in wishlist"}), 400

    new_item = Wishlist(user_id=user.id, product_id=product_id)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({
        "msg": "Added to wishlist",
        "data": wishlist_to_vue(new_item)
    }), 201


## TESTING DONE :--
@user_bp.route('/user/wishlist/<int:product_id>', methods=['DELETE'])
@jwt_required()
def removes_from_wishlist(product_id):
    user = get_current_user()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    item = Wishlist.query.filter_by(
        user_id=user.id,
        product_id=product_id
    ).first()

    if not item:
        return jsonify({"msg": "Item not in wishlist"}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({"msg": "Removed from wishlist"}), 200


## TESTING DONE
@user_bp.route('/user/wishlist', methods=['DELETE'])
@jwt_required()
def clear_from_wishlist():
    user = get_current_user()
    Wishlist.query.filter_by(user_id=user.id).delete()
    db.session.commit()

    return jsonify({"msg": "Wishlist cleared"}), 200



## TESTING DONE 

@user_bp.route('/user/wishlist/move-to-cart', methods=['POST'])
@jwt_required()
def move_wishlist_to_cart():
    user = get_current_user()
    data = request.get_json()

    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if not product_id:
        return jsonify({"msg": "product_id is required"}), 400

    wishlist_item = Wishlist.query.filter_by(
        user_id=user.id,
        product_id=product_id
    ).first()

    if not wishlist_item:
        return jsonify({"msg": "Item not found in wishlist"}), 404

    # Add / merge cart item
    cart_item = CartItem.query.filter_by(
        user_id=user.id,
        product_id=product_id
    ).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=user.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)

    # Remove from wishlist
    db.session.delete(wishlist_item)
    db.session.commit()

    return jsonify({"msg": "Moved to cart"}), 200




# ----------------------------------------------------------------------
# 🛒 CART  |  CartView.vue page api changed  |  API TESTING DONE
# ----------------------------------------------------------------------


##  TESTING DONE
@user_bp.route('/user/cart', methods=['GET'])
@jwt_required()
def get_cart():
    user = get_current_user()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    cart_items = []
    subtotal = 0
    total_qty = 0

    for item in user.cart_items:
        ui_item = cart_item_to_vue(item)
        subtotal += ui_item["price"] * ui_item["quantity"]
        total_qty += ui_item["quantity"]
        cart_items.append(ui_item)

    return jsonify({
        "data": cart_items,
        "cart_count": total_qty,
        "subtotal": round(subtotal, 2),
        "msg": "Cart fetched"
    }), 200



##  TESTING DONE
@user_bp.route('/user/cart/<int:product_id>', methods=['POST'])
@jwt_required()
def add_to_cart(product_id):
    user = get_current_user()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    product = Product.query.get(product_id)
    if not product or not product.is_active:
        return jsonify({"msg": "Product unavailable"}), 400

    cart_item = CartItem.query.filter_by(
        user_id=user.id,
        product_id=product_id
    ).first()

    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(
            user_id=user.id,
            product_id=product_id,
            quantity=1
        )
        db.session.add(cart_item)

    db.session.commit()

    return jsonify({
        "msg": "Added to cart",
        "data": cart_item_to_vue(cart_item)
    }), 200


##  TESTING DONE
@user_bp.route('/user/cart/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_cart_quantity(product_id):
    user = get_current_user()
    data = request.get_json()
    qty = int(data.get("quantity", 0))

    if qty < 1:
        return jsonify({"msg": "Invalid quantity"}), 400

    cart_item = CartItem.query.filter_by(
        user_id=user.id,
        product_id=product_id
    ).first()

    if not cart_item:
        return jsonify({"msg": "Item not in cart"}), 404

    cart_item.quantity = qty
    db.session.commit()

    return jsonify({
        "msg": "Quantity updated",
        "data": cart_item_to_vue(cart_item)
    }), 200


##  TESTING DONE
@user_bp.route('/user/cart/<int:product_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(product_id):
    user = get_current_user()
    cart_item = CartItem.query.filter_by(
        user_id=user.id,
        product_id=product_id
    ).first()

    if not cart_item:
        return jsonify({"msg": "Item not in cart"}), 404

    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({"msg": "Removed from cart"}), 200


# ----------------------------------------------------------------------
# 💳 CHECKOUT + ORDERS   |  CheckoutView.vue page api changed  |  API TESTING DONE
# ----------------------------------------------------------------------

##  TESTING DONE
@user_bp.route('/user/checkout/summary', methods=['GET'])
@jwt_required()
def checkout_summary():
    user = get_current_user()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    items = []
    subtotal = 0

    for item in user.cart_items:
        price = item.product.sale_price or item.product.price
        line_total = price * item.quantity
        subtotal += line_total

        items.append({
            "product_id": item.product_id,
            "name": item.product.name,
            "quantity": item.quantity,
            "price": price,
            "line_total": line_total,
            "image": item.product.images[0].image_url if item.product.images else None
        })

    return jsonify({
        "items": items,
        "subtotal": round(subtotal, 2),
        "shipping": 0,           # standard delivery default
        "tax": 0,
        "total": round(subtotal, 2),
        "msg": "Checkout summary loaded"
    }), 200



##  TESTING DONE
@user_bp.route('/user/orders', methods=['POST'])
@jwt_required()
def place_order():
    user = get_current_user()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    cart_items = user.cart_items
    if not cart_items:
        return jsonify({"msg": "Cart is empty"}), 400

    data = request.get_json()

    # Delivery fee
    delivery_method = data.get("delivery_method", "standard")
    shipping_fee = 15 if delivery_method == "express" else 0

    total = 0
    order_items = []

    for item in cart_items:
        price = item.product.sale_price or item.product.price
        total += price * item.quantity

        order_items.append(OrderItem(
            product_id=item.product_id,
            product_name=item.product.name,
            quantity=item.quantity,
            price_at_purchase=price
        ))

    total += shipping_fee

    order = Order(
        user_id=user.id,
        order_number=f"ORD-{uuid.uuid4().hex[:10].upper()}",
        total_amount=total,
        status="Pending",
        payment_status="Unpaid",
        payment_method=data.get("payment_method", "COD"),

        shipping_full_name=data.get("shipping_full_name"),
        shipping_address=data.get("shipping_address"),
        shipping_city=data.get("shipping_city"),
        shipping_zip=data.get("shipping_zip"),
        shipping_country=data.get("shipping_country"),
    )

    db.session.add(order)
    db.session.flush()

    for oi in order_items:
        oi.order_id = order.id
        db.session.add(oi)

    # Clear cart
    for item in cart_items:
        db.session.delete(item)

    db.session.commit()

    return jsonify({
        "msg": "Order placed successfully",
        "order_id": order.id,
        "order_number": order.order_number,
        "total_amount": total
    }), 201



##  TESTING DONE
@user_bp.route('/user/orders', methods=['GET'])
@jwt_required()
def list_user_orders():
    user = get_current_user()
    if not user:
        return jsonify({"msg": "User not found"}), 404
        
    # Use relationship, desc sort usually handled in query or logic
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
    return jsonify({"data": [o.serialize() for o in orders], "msg": "Orders fetched"})


##  TESTING DONE
@user_bp.route('/user/orders/<int:id>', methods=['GET'])
@jwt_required()
def get_order_details(id):
    user = get_current_user()
    if not user:
        return jsonify({"msg": "User not found"}), 404
        
    order = Order.query.get(id)
    if not order or order.user_id != user.id:
        return jsonify({"msg": "Order not found"}), 404
        
    return jsonify({"data": order.serialize(), "msg": "Order details"})


# ----------------------------------------------------------------------
# 📬 MESSAGES  |  API TESTING DONE
# ----------------------------------------------------------------------

##  TESTING DONE

@user_bp.route('/user/messages', methods=['POST'])
@jwt_required()
def send_message():
    user = get_current_user()
    if not user:
        return jsonify({"msg": "User not found"}), 404
        
    data = request.get_json()

    if not data.get('subject') or not data.get('message'):
        return jsonify({"msg": "Subject and message required"}), 400
        
    new_msg = Message(
        user_id=user.id,
        name=f"{user.first_name} {user.last_name}",
        email=user.email,
        subject=data.get('subject'),
        message=data['message'],   # ✅ FIXED
        status="New"
    )
    
    db.session.add(new_msg)
    db.session.commit()

    return jsonify({
        "msg": "Message sent",
        "data": new_msg.serialize()
    }), 201


##  TESTING DONE
@user_bp.route('/user/messages', methods=['GET'])
@jwt_required()
def get_my_messages():
    user = get_current_user()
    if not user:
        return jsonify({"msg": "User not found"}), 404
        
    msgs = Message.query.filter_by(user_id=user.id).order_by(Message.created_at.desc()).all()
    return jsonify({"data": [m.serialize() for m in msgs], "msg": "Messages fetched"})



# ----------------------------------------------------------------------
# 🌟 REVIEWS
# ----------------------------------------------------------------------


##  TESTING DONE

@user_bp.route('/products/<int:id>/review', methods=['POST'])
@jwt_required()
def add_review(id):
    user = get_current_user()
    if not user:
        return jsonify({"msg": "User not found"}), 404
        
    data = request.get_json()
    if not data.get('rating'):
        return jsonify({"msg": "Rating is required"}), 400
        
    # Optional: Check if user purchased product before reviewing (Business logic)
    
    review = Review(
        product_id=id,
        user_id=user.id,
        rating=int(data['rating']),
        comment=data.get('comment', '')
    )
    
    db.session.add(review)
    db.session.commit()
    return jsonify({"msg": "Review added", "data": review.serialize()}), 201


##  TESTING DONE

@user_bp.route('/products/<int:id>/reviews', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def get_product_reviews(id):
    # Public endpoint, no login needed
    reviews = Review.query.filter_by(product_id=id).order_by(Review.created_at.desc()).all()
    return jsonify({"data": [r.serialize() for r in reviews], "msg": "Reviews fetched"})



#  CategoryView.vue page apis :--


@user_bp.route('/products/category/<string:slug>', methods=['GET'])
def get_products_by_category(slug):
    # 1. Grab all Query Params
    sort = request.args.get('sort', 'relevance')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 12, type=int)
    price_min = request.args.get('price_min', type=float)
    price_max = request.args.get('price_max', type=float)
    in_stock = request.args.get('in_stock') # 'true'/'false' string
    on_sale = request.args.get('on_sale')   # 'true'/'false' string

    # 2. Base Query
    query = Product.query.filter(Product.is_active == True)

    # 3. Handle Category Filter
    if slug.lower() != "all":
        category = Category.query.filter_by(slug=slug).first()
        if not category:
            return jsonify({"msg": "Category not found", "data": []}), 404
        query = query.filter(Product.category_id == category.id)

    # 4. --- APPLY MISSING FILTERS ---
    if price_min is not None:
        query = query.filter(Product.price >= price_min)
    
    if price_max is not None:
        query = query.filter(Product.price <= price_max)

    if in_stock == 'true':
        query = query.filter(Product.stock_quantity > 0)

    if on_sale == 'true':
        # Assuming 'sale_price' is not Null when on sale
        query = query.filter(Product.sale_price.isnot(None))

    # 5. Sorting
    if sort == "price_low":
        query = query.order_by(Product.price.asc())
    elif sort == "price_high":
        query = query.order_by(Product.price.desc())
    elif sort == "newest":
        query = query.order_by(Product.created_at.desc())

    # 6. Pagination
    pagination = query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        "msg": "Products fetched",
        "total": pagination.total,
        "page": page,
        "pages": pagination.pages,
        "data": [product_to_user_vue(p) for p in pagination.items]
    }), 200



##  TESTING DONE  

@user_bp.route('/categories/<string:slug>', methods=['GET'])
def get_category(slug):
    category = Category.query.filter_by(slug=slug).first()
    if not category:
        return jsonify({"msg": "Category not found"}), 404

    return jsonify({
        "data": category.serialize(),
        "msg": "Category fetched"
    }), 200



@user_bp.route('/categories', methods=['GET'])
def list_navbar_categories():
    # Fetch all categories, sorted alphabetically
    categories = Category.query.order_by(Category.name.asc()).all()
    
    # Return list using your model's serialize() method
    return jsonify({
        "msg": "Categories fetched successfully",
        "data": [c.serialize() for c in categories] 
    }), 200



# ContactView.vue Page apis :--


##  TESTING DONE

@user_bp.route('/contact', methods=['POST'])
def submit_contact_message():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    subject = data.get("subject")
    message = data.get("message")

    # Validation
    if not name or not email or not message:
        return jsonify({"msg": "Name, email and message are required"}), 400

    # Optional user (if logged in)
    user_id = None
    try:
        user = get_current_user()
        if user:
            user_id = user.id
    except:
        pass  # guest user

    new_msg = Message(
        user_id=user_id,
        name=name,
        email=email,
        subject=subject,
        message=message
    )

    db.session.add(new_msg)
    db.session.commit()

    return jsonify({
        "msg": "Message received successfully"
    }), 201




# NewArrivalsView.vue page :--

##  TESTING DONE

@user_bp.route('/products/new-arrivals', methods=['GET'])
def new_arrivals():
    sort = request.args.get('sort', 'newest')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 8))

    query = Product.query.filter(Product.is_active == True)

    # Sorting
    if sort == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_high':
        query = query.order_by(Product.price.desc())
    else:
        # newest first
        query = query.order_by(Product.created_at.desc())

    pagination = query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        "msg": "New arrivals fetched",
        "total": pagination.total,
        "page": page,
        "pages": pagination.pages,
        "data": [product_card_to_vue(p) for p in pagination.items]
    }), 200




# OrderSuccessView.vue Page apis :--

##  TESTING DONE

@user_bp.route('/user/orders/<int:order_id>/success', methods=['GET'])
@jwt_required()
def get_order_success(order_id):
    user = get_current_user()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    order = Order.query.get(order_id)
    if not order or order.user_id != user.id:
        return jsonify({"msg": "Order not found"}), 404

    items = []

    for item in order.items:
        product = Product.query.get(item.product_id)

        image = None
        if product:
            image = next(
                (img.image_url for img in product.images if img.is_primary),
                None
            )

        items.append({
            "id": item.id,
            "name": item.product_name,
            "variant": "",                     # UI-only, safe default
            "price": item.price_at_purchase,
            "quantity": item.quantity,
            "image": image
        })

    return jsonify({
        "msg": "Order success details loaded",
        "data": {
            "orderNumber": order.order_number,
            "orderDate": order.created_at.strftime("%b %d, %Y"),
            "customerName": order.shipping_full_name,
            "estimatedDelivery": "5–7 Business Days",  # computed, not DB
            "total": float(order.total_amount),
            "shippingAddress": {
                "street": order.shipping_address,
                "city": order.shipping_city,
                "zip": order.shipping_zip,
                "country": order.shipping_country
            },
            "items": items
        }
    }), 200




# OrdersView.vue Page apis :--

## TESTING DONE :--

@user_bp.route('/user/orders', methods=['GET'])
@jwt_required()
def get_user_orders():
    user = get_current_user()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    status = request.args.get("status")
    query = Order.query.filter_by(user_id=user.id)

    if status and status != "All":
        query = query.filter(Order.status == status)

    # Sort by newest first
    orders = query.order_by(Order.created_at.desc()).all()

    result = []
    for order in orders:
        items_preview = []
        for item in order.items:
            # --- FIX: ROBUST IMAGE LOGIC ---
            # Default placeholder
            image_url = "https://via.placeholder.com/150?text=No+Image"
            
            # Try to get real product image
            if item.product and item.product.images:
                # Find primary image, or fallback to the first one available
                primary = next((img for img in item.product.images if img.is_primary), None)
                if primary:
                    image_url = primary.image_url
                elif len(item.product.images) > 0:
                    image_url = item.product.images[0].image_url

            items_preview.append({
                # Fallback to "Unknown Product" if name is missing in DB
                "name": item.product_name or "Unknown Product", 
                "qty": item.quantity,
                "image": image_url
            })

        result.append({
            "id": order.id,                 # INT: Primary Key (For Invoice Button)
            "order_number": order.order_number, # STRING: For Display (ORD-123)
            "date": order.created_at.strftime("%b %d, %Y"),
            "total": float(order.total_amount),
            "status": order.status,
            # Handle missing delivery message gracefully
            "deliveryMsg": f"Status: {order.status}", 
            "items": items_preview
        })

    return jsonify({
        "data": result,
        "total": len(result),
        "msg": "Orders fetched successfully"
    }), 200




##  TESTING DONE

@user_bp.route('/user/orders/<int:order_id>/invoice', methods=['GET'])
@jwt_required()
def download_invoice(order_id):
    user = get_current_user()
    if not user:
        return jsonify({"msg": "User not found"}), 404

    order = Order.query.get(order_id)
    if not order or order.user_id != user.id:
        return jsonify({"msg": "Order not found"}), 404

    # Later: generate PDF
    return jsonify({
        "msg": "Invoice generation triggered",
        "order_id": order.order_number
    }), 200




# SearchResultsView.vue page :--

##  TESTING DONE

@user_bp.route('/products/search', methods=['GET'])
def search_products():
    q = request.args.get('q', '').strip()
    category = request.args.get('category')
    sort = request.args.get('sort', 'relevance')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 12))

    if not q:
        return jsonify({"msg": "Search query required"}), 400

    query = Product.query.filter(Product.is_active == True)

    # 🔍 Keyword search (name + description)
    query = query.filter(
        Product.name.ilike(f"%{q}%") |
        Product.description.ilike(f"%{q}%")
    )

    # 🗂️ Category filter
    if category and category != "All":
        query = query.join(Category).filter(Category.name == category)

    # ↕️ Sorting
    if sort == "price_low":
        query = query.order_by(Product.price.asc())
    elif sort == "price_high":
        query = query.order_by(Product.price.desc())
    elif sort == "newest":
        query = query.order_by(Product.created_at.desc())
    else:
        # relevance fallback
        query = query.order_by(Product.created_at.desc())

    pagination = query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        "query": q,
        "total": pagination.total,
        "page": page,
        "pages": pagination.pages,
        "data": [product_card_dto(p) for p in pagination.items]
    }), 200





# ShopView.vue page :--

##  TESTING DONE

@user_bp.route('/products', methods=['GET'])
def list_shop_products():
    category_id = request.args.get('category_id')
    price_min = request.args.get('price_min', type=float)
    price_max = request.args.get('price_max', type=float)
    in_stock = request.args.get('in_stock')
    on_sale = request.args.get('on_sale')
    sort = request.args.get('sort', 'newest')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 12, type=int)

    query = Product.query.filter(Product.is_active == True)

    # 🗂️ Category
    if category_id:
        query = query.filter(Product.category_id == category_id)

    # 💰 Price range
    if price_min is not None:
        query = query.filter(Product.price >= price_min)
    if price_max is not None:
        query = query.filter(Product.price <= price_max)

    # 🟢 In stock
    if in_stock == "true":
        query = query.filter(Product.stock_quantity > 0)

    # 🔖 On sale
    if on_sale == "true":
        query = query.filter(Product.sale_price.isnot(None))

    # ↕️ Sorting
    if sort == "price_low":
        query = query.order_by(Product.price.asc())
    elif sort == "price_high":
        query = query.order_by(Product.price.desc())
    else:  # newest
        query = query.order_by(Product.created_at.desc())

    pagination = query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        "total": pagination.total,
        "page": page,
        "pages": pagination.pages,
        "data": [shop_product_card_dto(p) for p in pagination.items]
    }), 200




##  TESTING DONE

@user_bp.route('/categories', methods=['GET'])
def list_categories():
    categories = Category.query.order_by(Category.name.asc()).all()
    return jsonify({
        "data": [{"id": c.id, "name": c.name} for c in categories]
    }), 200





