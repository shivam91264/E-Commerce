ShopView.vue and ProductCard.vue :--

GET /api/products
GET /api/categories
POST /api/cart



ProductDetails.vue :--

GET /api/products/<id>
GET /api/products/<id>/related
POST /api/cart



ProfileView.vue :--

GET /api/user/profile
PUT /api/user/profile
PUT /api/user/change-password
PUT /api/user/2fa
POST /api/auth/logout



CartView.vue :--

GET /api/cart
PUT /api/cart/<item_id>
DELETE /api/cart/<item_id>
POST /api/checkout/init