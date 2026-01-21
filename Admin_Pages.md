AdminDashboard.vue :--

/api/admin/dashboard
/api/admin/dashboard/recent-orders



AdminProducts.vue :--

GET /api/admin/products
POST /api/admin/products
PUT /api/admin/products/:id
DELETE /api/admin/products/:id
GET /api/admin/categories/dropdown



AdminOrder.vue :--

GET /admin/orders
GET /admin/orders/<int:id>
PUT /admin/orders/<int:id>/status



AdminUsers.vue :--

GET /admin/users
GET /admin/users/<user_id>/orders
GET /admin/users/<user_id>/addresses
PUT /admin/users/<user_id>/status



AdminMessages.vue :--

GET /admin/messages
PUT /admin/messages/<int:id>/status
PUT /admin/messages/archive-resolved
