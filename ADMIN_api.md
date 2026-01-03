## Login :--
POST http://127.0.0.1:5000/api/auth/login

{
  "email": "shivam@example.com",
  "password": "Test@123"
}


## Register :--
POST http://127.0.0.1:5000/api/auth/register

{
  "full_name": "Shivam Gupta",
  "email": "shivam@example.com",
  "password": "Test123",
  "phone": "9876543210"
}


###  ADMIN DASHBOARD / ANALYTICS :--


#  get_summary
http://127.0.0.1:5000/api/admin/summary


#  revenue_trend
http://127.0.0.1:5000/api/admin/revenue_trend


#  order_status
http://127.0.0.1:5000/api/admin/order_status


# get_category_stats
GET  http://127.0.0.1:5000/api/admin/category_stats


#  performance_insights 
GET  http://127.0.0.1:5000/api/admin/performance_insights




### Admin Apis :--

### Category table

# 1. Create:--

POST http://127.0.0.1:5000/api/admin/categories

{
  "name": "Shoes",
  "description": "All footwear items",
  "image_url": "https://static.example.com/img/shoes.png"
}



# 2. Update :--

PUT http://localhost:5000/api/admin/categories/1

{
  "name": "Men Shoes",
  "description": "Footwear for men",
  "image_url": "https://example.com/men-shoes.jpg"
}



# 3. GET :--

GET http://localhost:5000/api/admin/categories


# 4. DELETE :--

DELETE http://localhost:5000/api/admin/categories/1


# 5. DROPDOWN :--

GET http://localhost:5000/api/admin/categories/dropdown




### Product table 

# 1. Create Product :--
POST http://localhost:5000/api/admin/products

{
  "name": "Nike Air Max",
  "sku": "NIKE-AM-001",
  "category_id": 1,
  "description": "Premium running shoes",
  "price": 4999,
  "sale_price": 4499,
  "stock": 25,
  "is_featured": true,
  "active": true,
  "image": "https://static.example.com/img/nike-air-max.png"
}


# 2. UPDATE Product :--
PUT http://127.0.0.1:5000/api/admin/products/1

{
  "name": "Nike Air Max Pro",
  "price": 5499,
  "salePrice": 4999,
  "stock": 20,
  "sku": "NIKE-AM-PRO-001",
  "category": "Shoes",
  "is_featured": true,
  "active": true,
  "description": "Premium running shoes with air cushioning",
  "image": "https://static.example.com/img/airmaxpro.png"
}



# 3. List Products :--
GET http://127.0.0.1:5000/api/admin/products


## Pagination Test :--
GET http://127.0.0.1:5000/api/admin/products?page=1&limit=5


## Filter by Category :--
GET http://127.0.0.1:5000/api/admin/products?category=Shoes


## Filter Active Products :--
GET http://127.0.0.1:5000/api/admin/products?active=true


## Search Product :--
GET http://127.0.0.1:5000/api/admin/products?search=nike



# 4. DELETE Product :--
DELETE http://127.0.0.1:5000/api/admin/products/3



### USERS Table :--

# 1.  GET USERS :--
GET http://127.0.0.1:5000/api/admin/users


## Pagination :--
GET /api/admin/users?page=1&limit=5


## Filter by Role :--
GET /api/admin/users?role=admin
GET /api/admin/users?role=user


## Filter Active / Blocked Users :--
GET /api/admin/users?active=true
GET /api/admin/users?active=false


## Search User :--
GET /api/admin/users?search=shivam



# 2. GET SINGLE USER :--
GET http://127.0.0.1:5000/api/admin/users/1



# 3. UPDATE USER STATUS :--
PUT  http://127.0.0.1:5000/api/admin/users/5/status

{
  "is_active": false
}


# 4. User Account Disabled :--
DELETE  http://127.0.0.1:5000/api/admin/users/7






###   Dashboard Summary API :--


# dashboard_overview
GET  http://127.0.0.1:5000/api/admin/dashboard


# recent_orders
GET  http://127.0.0.1:5000/api/admin/dashboard/recent-orders






###  MESSAGES / CUSTOMER QUERIES API :--

#  list_messages
GET  http://127.0.0.1:5000/api/admin/messages


#  get_single_message
GET  http://127.0.0.1:5000/api/admin/messages/1



#  update_message_status
PUT  http://127.0.0.1:5000/api/admin/messages/3/status



#  archive_resolved_messages
PUT  http://127.0.0.1:5000/api/admin/messages/archive-resolved



# delete_message
DELETE  http://127.0.0.1:5000/api/admin/messages/12






###  ORDERS MANAGEMENT API :--



# list_orders
GET  http://127.0.0.1:5000/api/admin/orders



# get_single_order
GET  http://127.0.0.1:5000/api/admin/orders/1


# update_order_status
PUT  http://127.0.0.1:5000/api/admin/orders/3/status



# delete_order
DELETE  http://127.0.0.1:5000/api/admin/orders/3