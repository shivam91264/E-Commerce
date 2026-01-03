def wishlist_to_vue(w):
    product = w.product

    return {
        "id": product.id,
        "name": product.name,
        "category": product.category.name if product.category else None,
        "price": product.sale_price if product.sale_price else product.price,
        "image": product.images[0].image_url if product.images else None,
        "badge": "Low Stock" if product.stock_quantity < 5 else "",
        "inStock": product.stock_quantity > 0
    }




def cart_item_to_vue(item):
    product = item.product
    price = product.sale_price if product.sale_price else product.price

    return {
        "id": product.id,
        "name": product.name,
        "variant": "Default",  # later: size/color
        "price": price,
        "quantity": item.quantity,
        "image": product.images[0].image_url if product.images else None
    }





## User :--

def product_to_user_vue(p):
    primary_image = next(
        (img.image_url for img in p.images if img.is_primary),
        None
    )

    return {
        "id": p.id,
        "name": p.name,
        "price": p.sale_price if p.sale_price else p.price,
        "image": primary_image,
        "badge": "Sale" if p.sale_price else "",
        "category": p.category.name if p.category else None
    }




def product_card_to_vue(p):
    primary_image = next(
        (img.image_url for img in p.images if img.is_primary),
        None
    )

    return {
        "id": p.id,
        "name": p.name,
        "price": p.sale_price if p.sale_price else p.price,
        "image": primary_image,
        "badge": "New",
        "category": p.category.name if p.category else None
    }






def product_card_dto(p):
    primary_image = next(
        (img.image_url for img in p.images if img.is_primary),
        None
    )

    badge = ""
    if p.sale_price:
        badge = "Sale"
    elif p.is_featured:
        badge = "Best Seller"
    elif (datetime.utcnow() - p.created_at).days <= 14:
        badge = "New"

    return {
        "id": p.id,
        "name": p.name,
        "category": p.category.name if p.category else None,
        "price": p.sale_price if p.sale_price else p.price,
        "image": primary_image,
        "badge": badge
    }




def shop_product_card_dto(p):
    primary_image = next(
        (img.image_url for img in p.images if img.is_primary),
        None
    )

    badge = ""
    if p.sale_price:
        badge = "Sale"
    elif p.is_featured:
        badge = "Best Seller"
    elif (datetime.utcnow() - p.created_at).days <= 14:
        badge = "New"

    return {
        "id": p.id,
        "name": p.name,
        "category": p.category_id,
        "price": p.sale_price if p.sale_price else p.price,
        "image": primary_image,
        "badge": badge,
        "in_stock": p.stock_quantity > 0
    }
