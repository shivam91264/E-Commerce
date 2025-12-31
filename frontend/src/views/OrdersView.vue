<template>
  <div class="d-flex flex-column min-vh-100 bg-light-subtle">
    
    <PremiumNavbar 
      :is-authenticated="true" 
      :cart-item-count="0" 
      user-role="user"
      @navigate="handleNavigation"
    />

    <main class="flex-grow-1 py-5">
      <div class="container px-lg-5">
        
        <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-end mb-5 gap-4 animate-fade-up">
          <div>
            <h1 class="display-5 fw-bold tracking-tight mb-2">Order History</h1>
            <p class="text-muted lead fs-6 mb-0">Track, return, or buy things again.</p>
          </div>
          
          <div class="d-flex gap-2 overflow-auto pb-1 hide-scrollbar">
            <button 
              v-for="filter in ['All', 'Processing', 'Shipped', 'Delivered', 'Cancelled']" 
              :key="filter"
              class="btn rounded-pill px-4 fw-bold text-uppercase extra-small transition-all border"
              :class="currentFilter === filter ? 'btn-dark' : 'btn-white'"
              @click="currentFilter = filter"
            >
              {{ filter }}
            </button>
          </div>
        </div>

        <div v-if="filteredOrders.length === 0" class="text-center py-6 animate-fade-up">
          <div class="bg-white d-inline-flex p-4 rounded-circle shadow-sm mb-4">
            <i class="bi bi-box-seam display-4 text-muted opacity-25"></i>
          </div>
          <h3 class="fw-bold mb-3">No orders found</h3>
          <p class="text-muted mb-4">You have no past orders matching this filter.</p>
          <button class="btn btn-dark rounded-pill px-5 py-3 text-uppercase fw-bold tracking-wide hover-lift" @click="currentFilter = 'All'">
            Show All Orders
          </button>
        </div>

        <div v-else class="row justify-content-center">
          <div class="col-lg-10 col-xl-9">
            
            <div 
              v-for="(order, index) in filteredOrders" 
              :key="order.id" 
              class="card border-0 shadow-sm rounded-4 mb-5 overflow-hidden animate-fade-up"
              :style="{ animationDelay: `${index * 100}ms` }"
            >
              
              <div class="card-header bg-light border-bottom border-light-subtle p-4">
                <div class="row align-items-center g-3">
                  <div class="col-6 col-md-3">
                    <span class="d-block text-muted extra-small text-uppercase tracking-wide fw-bold mb-1">Order Placed</span>
                    <span class="fw-bold text-dark small">{{ order.date }}</span>
                  </div>
                  <div class="col-6 col-md-2">
                    <span class="d-block text-muted extra-small text-uppercase tracking-wide fw-bold mb-1">Total</span>
                    <span class="fw-bold text-dark small">${{ order.total }}</span>
                  </div>
                  <div class="col-6 col-md-3">
                    <span class="d-block text-muted extra-small text-uppercase tracking-wide fw-bold mb-1">Order #</span>
                    <span class="fw-bold text-dark small font-monospace">{{ order.id }}</span>
                  </div>
                  <div class="col-12 col-md-4 text-md-end">
                    <button @click="downloadInvoice(order.id)" class="btn btn-link text-decoration-none text-muted p-0 extra-small fw-bold text-uppercase d-inline-flex align-items-center gap-2 hover-dark">
                      <i class="bi bi-file-earmark-arrow-down fs-5"></i> Invoice
                    </button>
                  </div>
                </div>
              </div>

              <div class="card-body p-4">
                <div class="row g-4">
                  
                  <div class="col-md-8">
                     <div class="mb-4">
                       <h5 class="fw-bold mb-1" :class="getStatusColor(order.status)">
                         {{ order.status }}
                       </h5>
                       <p class="text-muted small mb-0">{{ order.deliveryMsg }}</p>
                     </div>

                     <div class="d-flex flex-column gap-3">
                       <div v-for="(item, i) in order.items" :key="i" class="d-flex gap-3 align-items-center">
                          <div class="ratio ratio-1x1 bg-light rounded-3 overflow-hidden border" style="width: 80px; min-width: 80px;">
                             <img :src="item.image" class="object-fit-cover w-100 h-100" alt="Product">
                          </div>
                          <div>
                             <h6 class="fw-bold text-dark mb-1 d-block text-decoration-none">{{ item.name }}</h6>
                             <span class="text-muted small">Qty: {{ item.qty }}</span>
                          </div>
                       </div>
                     </div>
                  </div>

                  <div class="col-md-4 d-flex flex-column justify-content-center align-items-md-end gap-2 border-start-md ps-md-4">
                     <button class="btn btn-dark w-100 rounded-pill py-2 fw-bold text-uppercase extra-small hover-lift">
                       View Order
                     </button>
                     <button v-if="order.status === 'Delivered'" class="btn btn-outline-dark w-100 rounded-pill py-2 fw-bold text-uppercase extra-small hover-fill">
                       Buy Again
                     </button>
                     <button v-else class="btn btn-light border w-100 rounded-pill py-2 fw-bold text-uppercase extra-small text-muted">
                       Track Package
                     </button>
                     <a href="#" class="text-muted extra-small text-decoration-underline text-center mt-2">Problem with order?</a>
                  </div>

                </div>
              </div>

            </div>

            <div class="text-center mt-5">
              <span class="text-muted small d-block mb-3">Showing {{ filteredOrders.length }} of {{ orders.length }} orders</span>
              <button class="btn btn-outline-dark rounded-0 px-5 py-2 text-uppercase fw-bold extra-small tracking-wide" v-if="filteredOrders.length > 0">
                Load More
              </button>
            </div>

          </div>
        </div>

      </div>
    </main>

    <PremiumFooter @navigate="handleNavigation" />

  </div>
</template>

<script>
import PremiumNavbar from '@/components/Navbar.vue';
import PremiumFooter from '@/components/Footer.vue';

export default {
  name: "OrdersView",
  components: {
    PremiumNavbar,
    PremiumFooter
  },
  data() {
    return {
      currentFilter: 'All',
      orders: [
        {
          id: "8392-XJ",
          date: "Dec 15, 2025",
          total: "329.00",
          status: "Delivered",
          deliveryMsg: "Package handed to resident",
          items: [
            { name: "Linen Lounge Chair", qty: 1, image: "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?auto=format&fit=crop&w=150&q=80" }
          ]
        },
        {
          id: "7721-MC",
          date: "Dec 28, 2025",
          total: "240.00",
          status: "Shipped",
          deliveryMsg: "Arriving by Jan 2, 2026",
          items: [
            { name: "Ceramic Vase Set", qty: 2, image: "https://images.unsplash.com/photo-1612196808214-b7e239e5f6b7?auto=format&fit=crop&w=150&q=80" },
            { name: "Minimal Desk Lamp", qty: 1, image: "https://images.unsplash.com/photo-1507473888900-52e1ad145986?auto=format&fit=crop&w=150&q=80" }
          ]
        },
        {
          id: "1102-PP",
          date: "Nov 01, 2025",
          total: "45.00",
          status: "Cancelled",
          deliveryMsg: "Refund processed on Nov 03",
          items: [
            { name: "Velvet Cushion", qty: 1, image: "https://images.unsplash.com/photo-1584100936595-c0654b55a2e6?auto=format&fit=crop&w=150&q=80" }
          ]
        }
      ]
    };
  },
  computed: {
    filteredOrders() {
      if (this.currentFilter === 'All') return this.orders;
      return this.orders.filter(o => o.status === this.currentFilter);
    }
  },
  methods: {
    handleNavigation(page) {
      console.log(`Navigating to: ${page}`);
    },
    downloadInvoice(orderId) {
      // Functional Mock Logic
      alert(`Downloading Invoice for Order #${orderId}...`);
      console.log(`Download triggered for ${orderId}`);
    },
    getStatusColor(status) {
      switch(status) {
        case 'Delivered': return 'text-success';
        case 'Shipped': return 'text-primary';
        case 'Processing': return 'text-warning';
        case 'Cancelled': return 'text-danger';
        default: return 'text-dark';
      }
    }
  }
};
</script>

<style scoped>
/* PREMIUM DESIGN SYSTEM */

/* Background */
.bg-light-subtle { background-color: #f9fafb !important; }

/* Typography */
.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }

/* Transitions & Buttons */
.transition-all { transition: all 0.2s ease; }

.btn-white {
  background-color: #fff;
  color: #6c757d;
  border-color: #dee2e6;
}
.btn-white:hover {
  background-color: #f8f9fa;
  color: #000;
  border-color: #000;
}

.hover-dark:hover {
  color: #000 !important;
  text-decoration: underline !important;
}

.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.hover-fill {
  transition: all 0.2s ease;
}
.hover-fill:hover {
  background-color: #000;
  color: #fff;
}

/* Animations */
.animate-fade-up {
  animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
  transform: translateY(20px);
}
@keyframes fadeUp {
  to { opacity: 1; transform: translateY(0); }
}

/* Responsive Utilities */
@media (min-width: 768px) {
  .border-start-md {
    border-left: 1px solid #dee2e6;
  }
}

.hide-scrollbar::-webkit-scrollbar { display: none; }
.hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>