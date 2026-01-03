# USER PROFILE PAGE :--

# GET :--
GET http://127.0.0.1:5000/api/user/profile


# Update profile :--

PATCH http://127.0.0.1:5000/api/user/profile

{
  "name": "Sachin Kumar Gupta",
  "phone": "9998887776",
  "gender": "Male",
  "dob": "1998-06-15"
}




# USER ADDRESS PAGE :--

# GET :--

GET http://127.0.0.1:5000/api/user/addresses



# ADD :--

POST http://127.0.0.1:5000/api/user/addresses

{
  "name": "Sachin Gupta",
  "phone": "9876543210",
  "line1": "Flat 203, Shree Apartments",
  "line2": "Near City Mall",
  "city": "Pune",
  "state": "Maharashtra",
  "zip": "411001",
  "country": "India",
  "label": "Home",
  "isDefault": true
}




# UPDATE :--
PUT http://127.0.0.1:5000/api/user/addresses/1

{
  "name": "Shivam Gupta",
  "phone": "9998887776",
  "line1": "Flat 501, Sunshine Residency",
  "line2": "Near IT Park",
  "city": "Pune",
  "state": "Maharashtra",
  "zip": "411045",
  "country": "India",
  "label": "Office"
}



# DELETE :--

http://127.0.0.1:5000/api/user/addresses/1



# SET ADDRESS DEFAULT :--

PUT  http://127.0.0.1:5000/api/user/addresses/1/default





#  ProductDetails.vue page :--

#  GET :--

GET http://127.0.0.1:5000/api/products/1


# GET related_products :--

GET http://127.0.0.1:5000/api/products/1/related


# GET list_products :--

GET  http://127.0.0.1:5000/api/products



#  WishlistView.vue page :--


# add_to_wishlist :--
# No json data needed, data comes from url, from product id

POST http://127.0.0.1:5000/api/user/wishlist/1 


# list_wishlist :--

GET http://127.0.0.1:5000/api/user/wishlist


# removes_from_wishlist :--

DELETE http://127.0.0.1:5000/api/user/wishlist/1



#  clear_from_wishlist :--

DELETE  http://127.0.0.1:5000/api/user/wishlist




# CartView.vue page :--

# add_to_cart :--
# No json data needed, data comes from url, from product id

POST  http://127.0.0.1:5000/api/user/cart/1



# get_cart :--

GET  http://127.0.0.1:5000/api/user/cart



#  update_cart_quantity :--

PUT http://127.0.0.1:5000/api/user/cart/101

{
  "quantity": 3
}



# remove_from_cart :--

DELETE  http://127.0.0.1:5000/api/user/cart/101




# CheckoutView.vue page :--

# place_order :--

POST  http://127.0.0.1:5000/api/user/orders

{
  "delivery_method": "standard",
  "payment_method": "COD",
  "shipping_full_name": "Sachin Gupta",
  "shipping_address": "Flat 301, MG Road",
  "shipping_city": "Pune",
  "shipping_zip": "411001",
  "shipping_country": "India"
}


# list_user_orders :--

GET http://127.0.0.1:5000/api/user/orders



# get_order_details :--

GET  http://127.0.0.1:5000/api/user/orders/3


# checkout_summary :--

GET  http://127.0.0.1:5000/api/user/checkout/summary



#  MESSAGES :--

# send_message :--

POST http://127.0.0.1:5000/api/user/messages

{
  "subject": "Order delay",
  "message": "My order has not arrived yet. Please check."
}


# get_my_messages :--

GET  http://127.0.0.1:5000/api/user/messages



# REVIEWS :--

# add_review  :--

POST  http://127.0.0.1:5000/api/products/1/review

{
  "rating": 5,
  "comment": "Excellent product, quality is amazing!"
}



#  get_product_reviews :--

GET  http://127.0.0.1:5000/api/products/1/reviews



# CategoryView.vue page :--

# get_products_by_category :--

GET  http://127.0.0.1:5000/api/products/category/shoes



# get_category :--

GET  http://127.0.0.1:5000/api/categories/shoes



#  ContactView.vue Page :--

# submit_contact_message :--

POST  http://127.0.0.1:5000/api/contact


{
  "name": "Rahul Sharma",
  "email": "rahul@example.com",
  "subject": "Order related query",
  "message": "I have an issue with my recent order."
}



#  NewArrivalsView.vue page :--

# new_arrivals :--

GET  http://127.0.0.1:5000/api/products/new-arrivals


# PAGINATION TEST  :--

GET  http://127.0.0.1:5000/api/products/new-arrivals?page=2


# CHANGE PAGE SIZE :--

GET  http://127.0.0.1:5000/api/products/new-arrivals?limit=4


# SORT BY PRICE (LOW → HIGH) :--

GET  http://127.0.0.1:5000/api/products/new-arrivals?sort=price_low


# SORT BY PRICE (HIGH → LOW)

GET  http://127.0.0.1:5000/api/products/new-arrivals?sort=price_high




#  OrderSuccessView.vue Page  :--

# get_order_success 

GET http://127.0.0.1:5000/api/user/orders/12/success




#  OrdersView.vue Page  :--

GET  http://127.0.0.1:5000/api/user/orders



# download_invoice

GET  http://127.0.0.1:5000/api/user/orders/1/invoice



#  SearchResultsView.vue page :--

GET  http://127.0.0.1:5000/api/products/search?q=shoes&category=Men&sort=price_low&page=1&limit=12



# ShopView.vue page :--


#  list_shop_products :--

GET  http://127.0.0.1:5000/api/products



# list_categories :--

GET  http://127.0.0.1:5000/api/categories




# WishlistView.vue page :--

# get_wishlist :--

GET  http://127.0.0.1:5000/api/user/wishlist


