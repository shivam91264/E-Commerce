<template>
  <div class="d-flex flex-column min-vh-100 bg-light-subtle">
    
    <div class="flex-grow-1 py-5">
      <div class="container px-lg-5">
        
        <div class="row justify-content-center">
          <div class="col-lg-8 col-xl-6">
            
            <div class="text-center mb-5 animate-fade-up">
              <div class="mb-4">
                <div class="d-inline-flex align-items-center justify-content-center rounded-circle bg-success bg-opacity-10 text-success p-4 mb-2">
                  <i class="bi bi-check-lg display-4"></i>
                </div>
              </div>
              <h1 class="display-5 fw-bold tracking-tight mb-3">Order Placed Successfully</h1>
              <p class="lead text-muted mb-0 mx-auto" style="max-width: 500px;">
                Thank you for your purchase, <span class="fw-bold text-dark">{{ order.customerName }}</span>. 
                We've received your order and will notify you once it ships.
              </p>
            </div>

            <div class="card border-0 shadow-sm rounded-4 overflow-hidden mb-4 animate-fade-up delay-100">
              
              <div class="card-header bg-white border-bottom p-4">
                <div class="row align-items-center g-3">
                  <div class="col-6">
                    <span class="d-block text-muted extra-small text-uppercase tracking-wide mb-1">Order ID</span>
                    <span class="fw-bold font-monospace">{{ order.id }}</span>
                  </div>
                  <div class="col-6 text-end">
                    <span class="d-block text-muted extra-small text-uppercase tracking-wide mb-1">Date</span>
                    <span class="fw-bold">{{ order.date }}</span>
                  </div>
                </div>
              </div>

              <div class="card-body p-4">
                
                <div class="mb-5">
                  <h6 class="fw-bold mb-4 small text-uppercase tracking-wide text-muted">Order Status</h6>
                  <div class="position-relative m-4">
                    <div class="progress" style="height: 2px;">
                      <div class="progress-bar bg-dark" role="progressbar" style="width: 25%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
                    </div>
                    <div class="position-absolute top-0 start-0 translate-middle btn btn-sm btn-dark rounded-circle border-0 d-flex align-items-center justify-content-center" style="width: 2rem; height: 2rem;">
                      <i class="bi bi-check-lg"></i>
                    </div>
                    <div class="position-absolute top-0 start-50 translate-middle btn btn-sm btn-light border rounded-circle d-flex align-items-center justify-content-center text-muted" style="width: 2rem; height: 2rem;">
                      2
                    </div>
                    <div class="position-absolute top-0 start-100 translate-middle btn btn-sm btn-light border rounded-circle d-flex align-items-center justify-content-center text-muted" style="width: 2rem; height: 2rem;">
                      3
                    </div>
                  </div>
                  <div class="d-flex justify-content-between text-center small mt-2">
                    <span class="fw-bold text-dark">Processing</span>
                    <span class="text-muted">Shipped</span>
                    <span class="text-muted">Delivered</span>
                  </div>
                  <div class="alert alert-light border-0 bg-light-subtle mt-4 mb-0 d-flex align-items-center gap-3">
                    <i class="bi bi-calendar-event fs-5 text-dark"></i>
                    <div>
                      <span class="d-block fw-bold small">Estimated Delivery</span>
                      <span class="d-block text-muted extra-small">{{ order.estimatedDelivery }}</span>
                    </div>
                  </div>
                </div>

                <hr class="border-secondary opacity-10 my-4">

                <div class="mb-4">
                  <div v-for="item in order.items" :key="item.id" class="d-flex align-items-center gap-3 mb-3">
                    <div class="position-relative" style="width: 50px; height: 50px;">
                      <img :src="item.image" :alt="item.name" class="w-100 h-100 object-fit-cover rounded-2 border">
                      <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-secondary text-white border border-white" style="font-size: 0.6rem;">{{ item.quantity }}</span>
                    </div>
                    <div class="flex-grow-1">
                      <h6 class="mb-0 small fw-bold text-truncate" style="max-width: 200px;">{{ item.name }}</h6>
                      <span class="text-muted extra-small">{{ item.variant }}</span>
                    </div>
                    <span class="small fw-bold">${{ (item.price * item.quantity).toFixed(2) }}</span>
                  </div>
                </div>

                <hr class="border-secondary opacity-10 my-4">

                <div class="row g-4 mb-2">
                  <div class="col-md-6">
                    <h6 class="fw-bold small text-uppercase tracking-wide text-muted mb-2">Shipping Address</h6>
                    <address class="small text-dark mb-0 lh-sm fst-normal">
                      {{ order.customerName }}<br>
                      {{ order.address.street }}<br>
                      {{ order.address.city }}, {{ order.address.state }} {{ order.address.zip }}<br>
                      {{ order.address.country }}
                    </address>
                  </div>
                  <div class="col-md-6">
                    <h6 class="fw-bold small text-uppercase tracking-wide text-muted mb-2">Payment Method</h6>
                    <div class="d-flex align-items-center gap-2 small">
                      <i class="bi bi-credit-card-2-front fs-5"></i>
                      <span>Visa ending in <strong>4242</strong></span>
                    </div>
                    <div class="d-flex justify-content-between align-items-center mt-3 pt-3 border-top border-secondary border-opacity-10">
                      <span class="fw-bold small">Total Paid</span>
                      <span class="fw-bold fs-5">${{ order.total }}</span>
                    </div>
                  </div>
                </div>

              </div>
            </div>

            <div class="d-grid gap-3 d-sm-flex justify-content-center animate-fade-up delay-200">
              <button class="btn btn-dark rounded-pill px-5 py-3 text-uppercase fw-bold tracking-wide hover-lift" @click="handleTrackOrder">
                Track Order
              </button>
              <button class="btn btn-outline-dark rounded-pill px-5 py-3 text-uppercase fw-bold tracking-wide hover-lift" @click="handleNavigation('shop')">
                Continue Shopping
              </button>
            </div>

            <div class="text-center mt-5 pt-3 animate-fade-up delay-300">
              <p class="text-muted small mb-1">Need help with your order?</p>
              <a href="#" class="text-dark fw-bold text-decoration-none small hover-underline">Contact Support</a>
              <div class="mt-3">
                 <span class="badge bg-white border text-muted fw-normal rounded-pill px-3 py-2">
                   <i class="bi bi-arrow-return-left me-1"></i> Easy Returns
                 </span>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>

export default {
  name: "OrderSuccessView",
  data() {
    return {
      order: {
        id: "ORD-2025-8392",
        date: "Dec 30, 2025",
        customerName: "Alex Morgan",
        estimatedDelivery: "Jan 05, 2026 - Jan 07, 2026",
        total: "329.00",
        address: {
          street: "123 Market Street, Suite 400",
          city: "San Francisco",
          state: "CA",
          zip: "94103",
          country: "United States"
        },
        items: [
          { id: 101, name: "Linen Lounge Chair", variant: "Charcoal Grey", price: 299.00, quantity: 1, image: "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?auto=format&fit=crop&w=100&q=80" },
          { id: 104, name: "Ceramic Vase Set", variant: "White/Clay", price: 89.00, quantity: 1, image: "https://images.unsplash.com/photo-1612196808214-b7e239e5f6b7?auto=format&fit=crop&w=100&q=80" }
        ]
      }
    };
  },
  methods: {
    handleNavigation(page) {
      console.log(`Navigating to: ${page}`);
      // this.$router.push({ name: page });
    },
    handleTrackOrder() {
      alert(`Tracking order ${this.order.id}...`);
    }
  }
};
</script>

<style scoped>
/* PREMIUM DESIGN SYSTEM */

/* Layout & Background */
.bg-light-subtle { background-color: #f9fafb !important; }
.tracking-tight { letter-spacing: -0.03em; }
.tracking-wide { letter-spacing: 0.1em; }
.extra-small { font-size: 0.75rem; }

/* Animations */
.animate-fade-up {
  animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
  transform: translateY(20px);
}

.delay-100 { animation-delay: 0.1s; }
.delay-200 { animation-delay: 0.2s; }
.delay-300 { animation-delay: 0.3s; }

@keyframes fadeUp {
  to { opacity: 1; transform: translateY(0); }
}

/* Button Interactions */
.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.hover-underline:hover {
  text-decoration: underline !important;
}

/* Card Styling */
.card {
  box-shadow: 0 10px 30px rgba(0,0,0,0.04) !important;
}

/* Progress Bar Tweaks */
.progress {
  overflow: visible;
  background-color: #e9ecef;
}
</style>