<template>
  <div class="d-flex flex-column min-vh-100 bg-white">
    
    <div class="flex-grow-1">
      <div class="container px-lg-5 py-5">
        
        <div class="mb-5 border-bottom pb-4">
          <h1 class="display-5 fw-bold tracking-tight mb-2">Your Cart</h1>
          <p class="text-muted mb-0">Review your selection before checkout.</p>
        </div>

        <div v-if="loading" class="text-center py-5">
           <div class="spinner-border text-dark" role="status"></div>
        </div>

        <div v-else-if="cartItems.length === 0" class="text-center py-5 animate-fade-up">
          <div class="mb-4">
            <i class="bi bi-bag display-1 text-light"></i>
          </div>
          <h3 class="fw-bold mb-3">Your cart is currently empty.</h3>
          <p class="text-muted mb-4" style="max-width: 400px; margin: 0 auto;">
            Looks like you haven't made your choice yet. Explore our latest collection to find something you love.
          </p>
          <button class="btn btn-dark rounded-pill px-5 py-3 text-uppercase fw-bold tracking-wide" @click="handleContinueShopping">
            Start Shopping
          </button>
        </div>

        <div class="row g-5" v-else>
          
          <div class="col-lg-8">
            <div class="mb-2 d-flex justify-content-between align-items-center">
              <span class="text-uppercase tracking-wide extra-small text-muted fw-bold">Product</span>
              <span class="text-uppercase tracking-wide extra-small text-muted fw-bold d-none d-md-block">Total</span>
            </div>
            
            <div class="border-top border-dark">
              <CartItem 
                v-for="item in cartItems" 
                :key="item.id" 
                :item="item" 
                @update-quantity="updateQuantity"
                @remove="removeItem"
                @click-item="navigateToProduct"
              />
            </div>

            <div class="d-lg-none mt-5 pt-4 border-top">
              <div class="row g-3 text-center">
                <div class="col-4">
                  <i class="bi bi-shield-check fs-4 mb-2 d-block text-muted"></i>
                  <span class="extra-small text-uppercase fw-bold">Secure</span>
                </div>
                <div class="col-4">
                  <i class="bi bi-arrow-return-left fs-4 mb-2 d-block text-muted"></i>
                  <span class="extra-small text-uppercase fw-bold">Returns</span>
                </div>
                <div class="col-4">
                  <i class="bi bi-truck fs-4 mb-2 d-block text-muted"></i>
                  <span class="extra-small text-uppercase fw-bold">Fast Ship</span>
                </div>
              </div>
            </div>

            <div class="mt-5 d-none d-lg-block">
              <button class="btn btn-link text-dark text-decoration-none fw-bold px-0" @click="handleContinueShopping">
                <i class="bi bi-arrow-left me-2"></i> Continue Shopping
              </button>
            </div>
          </div>

          <div class="col-lg-4">
            <div class="card border-0 bg-light rounded-3 p-4 sticky-lg-top" style="top: 100px; z-index: 1;">
              <h5 class="fw-bold mb-4 text-uppercase tracking-wide small">Order Summary</h5>
              
              <div class="d-flex justify-content-between mb-3">
                <span class="text-muted small">Subtotal ({{ cartCount }} items)</span>
                <span class="fw-medium">${{ subtotal.toFixed(2) }}</span>
              </div>
              <div class="d-flex justify-content-between mb-3">
                <span class="text-muted small">Shipping Estimate</span>
                <span class="fw-medium text-success">Calculated at next step</span>
              </div>
              <div class="d-flex justify-content-between mb-4">
                <span class="text-muted small">Tax Estimate</span>
                <span class="fw-medium">$0.00</span>
              </div>

              <hr class="border-secondary opacity-10 my-4">

              <div class="d-flex justify-content-between mb-4">
                <span class="fw-bold fs-5">Total</span>
                <span class="fw-bold fs-5">${{ subtotal.toFixed(2) }}</span>
              </div>

              <div class="d-grid gap-3">
                <button class="btn btn-dark py-3 rounded-0 text-uppercase fw-bold tracking-wide" @click="proceedToCheckout">
                  Proceed to Checkout
                </button>
                <div class="text-center mt-2">
                   <small class="text-muted extra-small"><i class="bi bi-lock-fill me-1"></i> SSL Secured Checkout</small>
                </div>
              </div>
              
              <div class="mt-4 pt-4 border-top border-secondary border-opacity-10 d-none d-lg-block">
                 <div class="d-flex justify-content-between opacity-50">
                   <i class="bi bi-credit-card-2-front fs-5"></i>
                   <i class="bi bi-paypal fs-5"></i>
                   <i class="bi bi-apple fs-5"></i>
                   <i class="bi bi-google fs-5"></i>
                 </div>
              </div>

            </div>
          </div>

        </div>
      </div>
    </div>

    <div class="d-lg-none fixed-bottom bg-white border-top shadow-lg p-3 animate-slide-up" v-if="cartItems.length > 0">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <span class="small text-muted">Total</span>
        <span class="fw-bold fs-5">${{ subtotal.toFixed(2) }}</span>
      </div>
      <button class="btn btn-dark w-100 py-3 rounded-pill text-uppercase fw-bold tracking-wide" @click="proceedToCheckout">
        Checkout
      </button>
    </div>

  </div>
</template>

<script>
import CartItem from '@/components/CartItem.vue';
import api from "@/services/api";

export default {
  name: "CartView",
  components: {
    CartItem
  },
  data() {
    return {
      cartItems: [],
      loading: true
    };
  },
  computed: {
    cartCount() {
      // Calculate total item count (sum of quantities)
      return this.cartItems.reduce((acc, item) => acc + item.quantity, 0);
    },
    subtotal() {
      // API might return this, but calculating on frontend is safer for instant UI updates
      return this.cartItems.reduce((acc, item) => acc + (item.price * item.quantity), 0);
    }
  },
  mounted() {
    this.fetchCart();
  },
  methods: {
    async fetchCart() {
      this.loading = true;
      try {
        const response = await api.get('/user/cart');
        // Make sure API response structure matches { data: [...] }
        this.cartItems = response.data.data; 
      } catch (error) {
        console.error("Failed to load cart:", error);
        if (error.response && error.response.status === 401) {
           this.$router.push('/login');
        }
      } finally {
        this.loading = false;
      }
    },

    async updateQuantity(product_id, newQty) {
      if (newQty < 1) return;
      try {
        // Optimistic UI update
        const item = this.cartItems.find(i => i.product_id === product_id); // Changed from i.id to i.product_id based on API
        if (item) item.quantity = newQty;

        await api.put(`/user/cart/${product_id}`, { quantity: newQty });
        // Optionally fetchCart() again to ensure sync
      } catch (error) {
        alert("Failed to update quantity");
        this.fetchCart(); // Revert on error
      }
    },

    async removeItem(product_id) {
      if (!confirm('Are you sure you want to remove this item?')) return;
      
      try {
        await api.delete(`/user/cart/${product_id}`);
        // Remove from local array immediately
        this.cartItems = this.cartItems.filter(i => i.product_id !== product_id);
      } catch (error) {
        alert("Failed to remove item");
      }
    },

    handleContinueShopping() {
      this.$router.push('/shop');
    },

    proceedToCheckout() {
      this.$router.push('/checkout');
    },

    navigateToProduct(item) {
      this.$router.push(`/product/${item.product_id}`);
    }
  }
};
</script>

<style scoped>
/* Reused Styles */
.tracking-tight { letter-spacing: -0.03em; }
.tracking-wide { letter-spacing: 0.1em; }
.extra-small { font-size: 0.75rem; }
.sticky-lg-top { position: -webkit-sticky; position: sticky; top: 100px; }
.animate-fade-up { animation: fadeUp 0.6s ease-out forwards; opacity: 0; transform: translateY(20px); }
@keyframes fadeUp { to { opacity: 1; transform: translateY(0); } }
.animate-slide-up { animation: slideUp 0.4s ease-out forwards; }
@keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0); } }
@media (max-width: 991px) { .flex-grow-1 { padding-bottom: 80px; } }
</style>