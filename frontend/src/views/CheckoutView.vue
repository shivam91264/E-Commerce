<template>
  <div class="d-flex flex-column min-vh-100 bg-light-subtle">
    
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
              <div class="card-header bg-white p-4 border-bottom d-flex justify-content-between align-items-center">
                <h5 class="mb-0 fw-bold d-flex align-items-center gap-2">
                  <i class="bi bi-geo-alt text-muted"></i> Shipping Address
                </h5>
                
                <div class="dropdown" v-if="savedAddresses.length > 0">
                  <button class="btn btn-outline-dark btn-sm rounded-pill dropdown-toggle px-3" type="button" data-bs-toggle="dropdown">
                    Use Saved Address
                  </button>
                  <ul class="dropdown-menu dropdown-menu-end border-0 shadow p-2" style="max-height: 300px; overflow-y: auto;">
                    <li v-for="addr in savedAddresses" :key="addr.id">
                      <button class="dropdown-item small rounded-2 py-2 mb-1" @click="selectAddress(addr)">
                        <strong>{{ addr.label }}</strong> - {{ addr.line1 }}, {{ addr.city }}
                      </button>
                    </li>
                  </ul>
                </div>
              </div>

              <div class="card-body p-4">
                <AddressForm v-model="shippingData" />
              </div>
            </div>

            <div class="card border-0 shadow-sm rounded-3 mb-4 overflow-hidden">
              <div class="card-header bg-white p-4 border-bottom">
                <h5 class="mb-0 fw-bold d-flex align-items-center gap-2">
                  <i class="bi bi-truck text-muted"></i> Delivery Method
                </h5>
              </div>
              <div class="card-body p-4">
                <div class="form-check p-3 border rounded-2 mb-2 bg-light-hover cursor-pointer" :class="{ 'selected-radio': deliveryMethod === 'standard' }">
                  <input class="form-check-input" type="radio" name="delivery" id="std" value="standard" v-model="deliveryMethod">
                  <label class="form-check-label d-flex justify-content-between w-100 cursor-pointer" for="std">
                    <span>
                      <span class="d-block fw-bold text-dark">Standard Delivery</span>
                      <span class="d-block extra-small text-muted">Estimated: 5-7 Business Days</span>
                    </span>
                    <span class="fw-bold">Free</span>
                  </label>
                </div>
                <div class="form-check p-3 border rounded-2 bg-light-hover cursor-pointer" :class="{ 'selected-radio': deliveryMethod === 'express' }">
                  <input class="form-check-input" type="radio" name="delivery" id="exp" value="express" v-model="deliveryMethod">
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
                <PaymentOptions v-model="paymentMethod" />
              </div>
            </div>

          </div>

          <div class="col-lg-5">
            <OrderSummary 
              :subtotal="summary.subtotal" 
              :shipping="shippingCost" 
              :total="grandTotal" 
              :items="summary.items"
              :loading="loading"
              @place-order="placeOrder" 
            />
            
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
        <span class="fw-bold fs-5">${{ grandTotal.toFixed(2) }}</span>
      </div>
      <button 
        class="btn btn-dark w-100 py-3 rounded-pill text-uppercase fw-bold tracking-wide" 
        @click="placeOrder"
        :disabled="placingOrder"
      >
        <span v-if="placingOrder" class="spinner-border spinner-border-sm me-2"></span>
        {{ placingOrder ? 'Processing...' : 'Place Order' }}
      </button>
    </div>

  </div>
</template>

<script>
import AddressForm from '@/components/checkout/AddressForm.vue';
import PaymentOptions from '@/components/checkout/PaymentOptions.vue';
import OrderSummary from '@/components/checkout/OrderSummary.vue';
import api from "@/services/api";

export default {
  name: "CheckoutView",
  components: {
    AddressForm,
    PaymentOptions,
    OrderSummary
  },
  data() {
    return {
      loading: true,
      placingOrder: false,
      
      // Form Inputs
      deliveryMethod: 'standard',
      paymentMethod: 'COD',
      shippingData: {
        full_name: '',
        phone: '',
        address_line1: '',
        address_line2: '',
        city: '',
        state: '',
        zip_code: '',
        country: 'United States'
      },
      
      // Data from API
      savedAddresses: [],
      summary: {
        subtotal: 0,
        items: []
      }
    };
  },
  computed: {
    shippingCost() {
      return this.deliveryMethod === 'express' ? 15.00 : 0;
    },
    grandTotal() {
      // Ensure values are safe to add
      return (this.summary.subtotal || 0) + this.shippingCost;
    }
  },
  mounted() {
    this.fetchCheckoutSummary();
    this.fetchSavedAddresses();
  },
  methods: {
    // 1. Fetch Cart Data
    async fetchCheckoutSummary() {
      this.loading = true;
      try {
        const res = await api.get('/user/checkout/summary');
        
        // FIX: Reverse the items array so newest appear first (Top)
        if (res.data && res.data.items) {
           res.data.items = res.data.items.reverse();
        }

        this.summary = res.data;
      } catch (err) {
        console.error("Summary error", err);
        // If cart is empty (API returns 400 or data suggests empty), redirect
        if (err.response && err.response.status === 400) {
           this.$router.push('/cart');
        }
      } finally {
        this.loading = false;
      }
    },

    // 2. Fetch Addresses
    async fetchSavedAddresses() {
      try {
        const res = await api.get('/user/addresses');
        this.savedAddresses = res.data.data;
        
        // Auto-select default if exists
        const defaultAddr = this.savedAddresses.find(a => a.isDefault);
        if (defaultAddr) this.selectAddress(defaultAddr);
      } catch (err) {
        console.error("Address error", err);
      }
    },

    // 3. Auto-fill logic
    selectAddress(addr) {
      this.shippingData = {
        full_name: addr.name,
        phone: addr.phone,
        address_line1: addr.line1,
        address_line2: addr.line2,
        city: addr.city,
        state: addr.state,
        zip_code: addr.zip,
        country: addr.country
      };
    },

    // 4. Place Order (Robust Error Handling)
    async placeOrder() {
      if (!this.shippingData.full_name || !this.shippingData.address_line1 || !this.shippingData.city) {
        alert("Please complete the shipping address form.");
        return;
      }

      this.placingOrder = true;

      try {
        const payload = {
          delivery_method: this.deliveryMethod,
          payment_method: this.paymentMethod,
          
          shipping_full_name: this.shippingData.full_name,
          shipping_address: `${this.shippingData.address_line1} ${this.shippingData.address_line2 || ''}`,
          shipping_city: this.shippingData.city,
          shipping_zip: this.shippingData.zip_code,
          shipping_country: this.shippingData.country
        };

        const res = await api.post('/user/orders', payload);
        
        // Ensure we have a valid Order ID before redirecting
        if (res.data && res.data.order_id) {
          this.$router.push({ 
            name: 'ordersuccess', 
            query: { orderId: res.data.order_id } 
          });
        } else {
          console.error("Order ID missing in response", res.data);
          alert("Order Placed, but redirect failed. Check your Orders page.");
          this.$router.push('/order'); // Fallback redirect
        }

      } catch (err) {
        console.error("Order failed:", err);
        // Display specific API error message if available
        const msg = err.response?.data?.msg || err.message || "Failed to place order.";
        alert(`Order Failed: ${msg}`);
      } finally {
        this.placingOrder = false;
      }
    }
  }
};
</script>

<style scoped>
/* Styles */
.bg-light-subtle { background-color: #f9fafb !important; }
.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }
.bg-light-hover:hover { background-color: #f8f9fa; }
.selected-radio { background-color: #f8f9fa; border-color: #000 !important; }
.animate-slide-up { animation: slideUp 0.4s ease-out forwards; }
@keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0); } }
</style>