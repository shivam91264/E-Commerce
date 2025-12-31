<template>
  <div class="d-flex flex-column min-vh-100 bg-white">
    
    <PremiumNavbar 
      :is-authenticated="false" 
      :cart-item-count="cartCount" 
      user-role="guest"
    />

    <div class="flex-grow-1">
      <div class="container px-lg-5 py-5">
        
        <div class="mb-5 border-bottom pb-4">
          <h1 class="display-5 fw-bold tracking-tight mb-2">Your Cart</h1>
          <p class="text-muted mb-0">Review your selection before checkout.</p>
        </div>

        <div v-if="cartItems.length === 0" class="text-center py-5 animate-fade-up">
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

    <PremiumFooter />

  </div>
</template>

<script>
import PremiumNavbar from '@/components/Navbar.vue';
import PremiumFooter from '@/components/Footer.vue';
import CartItem from '@/components/CartItem.vue';

export default {
  name: "CartView",
  components: {
    PremiumNavbar,
    PremiumFooter,
    CartItem
  },
  data() {
    return {
      // Mock Cart Data
      cartItems: [
        { 
          id: 101, 
          name: "Linen Lounge Chair", 
          variant: "Charcoal Grey", 
          price: 299.00, 
          quantity: 1, 
          image: "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?auto=format&fit=crop&w=400&q=80" 
        },
        { 
          id: 103, 
          name: "Minimal Desk Lamp", 
          variant: "Matte Black", 
          price: 120.00, 
          quantity: 2, 
          image: "https://images.unsplash.com/photo-1507473888900-52e1ad145986?auto=format&fit=crop&w=400&q=80" 
        },
        { 
          id: 104, 
          name: "Ceramic Vase Set", 
          variant: "White/Clay", 
          price: 89.00, 
          quantity: 1, 
          image: "https://images.unsplash.com/photo-1612196808214-b7e239e5f6b7?auto=format&fit=crop&w=400&q=80" 
        }
      ]
    };
  },
  computed: {
    cartCount() {
      return this.cartItems.reduce((acc, item) => acc + item.quantity, 0);
    },
    subtotal() {
      return this.cartItems.reduce((acc, item) => acc + (item.price * item.quantity), 0);
    }
  },
  methods: {
    updateQuantity(id, newQty) {
      const item = this.cartItems.find(i => i.id === id);
      if (item && newQty > 0) {
        item.quantity = newQty;
      }
    },
    removeItem(id) {
      if(confirm('Are you sure you want to remove this item?')) {
        this.cartItems = this.cartItems.filter(i => i.id !== id);
      }
    },
    handleContinueShopping() {
      // In real app: this.$router.push({ name: 'shop' });
      console.log("Navigating to Shop");
    },
    proceedToCheckout() {
      // In real app: this.$router.push({ name: 'checkout' });
      console.log("Proceeding to Checkout");
    },
    navigateToProduct() {
      console.log("Navigating to PDP");
    }
  }
};
</script>

<style scoped>
/* Typography */
.tracking-tight { letter-spacing: -0.03em; }
.tracking-wide { letter-spacing: 0.1em; }
.extra-small { font-size: 0.75rem; }

/* Sticky positioning for summary */
.sticky-lg-top {
  position: -webkit-sticky;
  position: sticky;
  top: 100px; /* Offset for navbar */
}

/* Animations */
.animate-fade-up {
  animation: fadeUp 0.6s ease-out forwards;
  opacity: 0;
  transform: translateY(20px);
}
@keyframes fadeUp {
  to { opacity: 1; transform: translateY(0); }
}

.animate-slide-up {
  animation: slideUp 0.4s ease-out forwards;
}
@keyframes slideUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

/* Mobile Adjustments */
@media (max-width: 991px) {
  /* Ensure content doesn't get hidden behind sticky bottom bar */
  .flex-grow-1 { padding-bottom: 80px; }
}
</style>