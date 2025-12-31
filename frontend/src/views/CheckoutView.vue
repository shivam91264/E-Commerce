<template>
  <div class="d-flex flex-column min-vh-100 bg-light-subtle">
    
    <PremiumNavbar :is-authenticated="true" :cart-item-count="3" user-role="guest" />

    <div class="flex-grow-1 py-4 py-lg-5">
      <div class="container px-lg-5">
        
        <div class="mb-5 text-center text-lg-start">
          <h1 class="display-5 fw-bold tracking-tight mb-2">Checkout</h1>
          <div class="d-flex align-items-center justify-content-center justify-content-lg-start gap-3 text-muted small text-uppercase tracking-wide">
            <span class="text-dark fw-bold">1. Shipping</span>
            <i class="bi bi-chevron-right extra-small"></i>
            <span>2. Payment</span>
            <i class="bi bi-chevron-right extra-small"></i>
            <span>3. Review</span>
          </div>
        </div>

        <div class="row g-5">
          
          <div class="col-lg-7">
            
            <div class="card border-0 shadow-sm rounded-3 mb-4 overflow-hidden">
              <div class="card-header bg-white p-4 border-bottom">
                <h5 class="mb-0 fw-bold d-flex align-items-center gap-2">
                  <i class="bi bi-geo-alt text-muted"></i> Shipping Address
                </h5>
              </div>
              <div class="card-body p-4">
                <AddressForm />
              </div>
            </div>

            <div class="card border-0 shadow-sm rounded-3 mb-4 overflow-hidden">
              <div class="card-header bg-white p-4 border-bottom">
                <h5 class="mb-0 fw-bold d-flex align-items-center gap-2">
                  <i class="bi bi-truck text-muted"></i> Delivery Method
                </h5>
              </div>
              <div class="card-body p-4">
                <div class="form-check p-3 border rounded-2 mb-2 bg-light-hover cursor-pointer selected-radio">
                  <input class="form-check-input" type="radio" name="delivery" id="std" checked>
                  <label class="form-check-label d-flex justify-content-between w-100 cursor-pointer" for="std">
                    <span>
                      <span class="d-block fw-bold text-dark">Standard Delivery</span>
                      <span class="d-block extra-small text-muted">Estimated: 5-7 Business Days</span>
                    </span>
                    <span class="fw-bold">Free</span>
                  </label>
                </div>
                <div class="form-check p-3 border rounded-2 bg-light-hover cursor-pointer">
                  <input class="form-check-input" type="radio" name="delivery" id="exp">
                  <label class="form-check-label d-flex justify-content-between w-100 cursor-pointer" for="exp">
                    <span>
                      <span class="d-block fw-bold text-dark">Express Shipping</span>
                      <span class="d-block extra-small text-muted">Estimated: 2-3 Business Days</span>
                    </span>
                    <span class="fw-bold">$15.00</span>
                  </label>
                </div>
              </div>
            </div>

            <div class="card border-0 shadow-sm rounded-3 mb-5 overflow-hidden">
              <div class="card-header bg-white p-4 border-bottom">
                <h5 class="mb-0 fw-bold d-flex align-items-center gap-2">
                  <i class="bi bi-credit-card text-muted"></i> Payment
                </h5>
              </div>
              <div class="card-body p-4">
                <PaymentOptions />
              </div>
            </div>

          </div>

          <div class="col-lg-5">
            <OrderSummary />
            
            <div class="mt-4 text-center text-muted">
              <div class="d-flex justify-content-center gap-4 mb-3 opacity-50">
                <i class="bi bi-shield-lock fs-4"></i>
                <i class="bi bi-box-seam fs-4"></i>
                <i class="bi bi-arrow-counterclockwise fs-4"></i>
              </div>
              <p class="extra-small">
                Your data is protected. By placing an order, you agree to our Terms of Service and Privacy Policy.
              </p>
            </div>
          </div>

        </div>
      </div>
    </div>

    <div class="d-lg-none fixed-bottom bg-white border-top shadow-lg p-3 animate-slide-up z-3">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <span class="text-muted small">Total to pay</span>
        <span class="fw-bold fs-5">$329.00</span>
      </div>
      <button class="btn btn-dark w-100 py-3 rounded-pill text-uppercase fw-bold tracking-wide" @click="placeOrder">
        Place Order
      </button>
    </div>

    <PremiumFooter />
  </div>
</template>

<script>
import PremiumNavbar from '@/components/Navbar.vue';
import PremiumFooter from '@/components/Footer.vue';
import AddressForm from '@/components/checkout/AddressForm.vue';
import PaymentOptions from '@/components/checkout/PaymentOptions.vue';
import OrderSummary from '@/components/checkout/OrderSummary.vue';

export default {
  name: "CheckoutView",
  components: {
    PremiumNavbar,
    PremiumFooter,
    AddressForm,
    PaymentOptions,
    OrderSummary
  },
  methods: {
    placeOrder() {
      // In real app, trigger form validation then submit
      alert("Processing your order secure...");
    }
  }
};
</script>

<style scoped>
/* Page Styles */
.bg-light-subtle { background-color: #f9fafb !important; }
.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }

/* Radio Selection Styles */
.bg-light-hover:hover { background-color: #f8f9fa; }
.form-check-input:checked + label { color: #000; }
.selected-radio {
  background-color: #f8f9fa;
  border-color: #000 !important;
}

/* Animations */
.animate-slide-up { animation: slideUp 0.4s ease-out forwards; }
@keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0); } }
</style>