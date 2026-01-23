<template>
  <div class="d-flex flex-column min-vh-100 bg-light-subtle">
    
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

        <div v-if="loading" class="text-center py-5">
           <div class="spinner-border text-dark" role="status"></div>
        </div>

        <div v-else-if="filteredOrders.length === 0" class="text-center py-6 animate-fade-up">
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
                    <button @click="downloadInvoice(order.realId)" class="btn btn-link text-decoration-none text-muted p-0 extra-small fw-bold text-uppercase d-inline-flex align-items-center gap-2 hover-dark">
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
                             <img :src="item.image || 'https://via.placeholder.com/150'" class="object-fit-cover w-100 h-100" alt="Product">
                           </div>
                           <div>
                             <h6 class="fw-bold text-dark mb-1 d-block text-decoration-none">{{ item.name }}</h6>
                             <span class="text-muted small">Qty: {{ item.qty }}</span>
                           </div>
                        </div>
                      </div>
                  </div>

                  <div class="col-md-4 d-flex flex-column justify-content-center align-items-md-end gap-2 border-start-md ps-md-4">
                      <button @click="handleNavigation('ordersuccess?orderId=' + order.realId)" class="btn btn-dark w-100 rounded-pill py-2 fw-bold text-uppercase extra-small hover-lift">
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

            </div>
        </div>

      </div>
    </main>

  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "OrdersView",
  data() {
    return {
      loading: true,
      currentFilter: 'All',
      orders: [], // Will fetch from API
    };
  },
  computed: {
    // Client-side filtering fallback (though API handles it now)
    filteredOrders() {
      // Since API filters, we just return orders. 
      // If you want client-side filtering instead, uncomment:
      // if (this.currentFilter === 'All') return this.orders;
      // return this.orders.filter(o => o.status === this.currentFilter);
      return this.orders;
    }
  },
  watch: {
    // Re-fetch when filter changes
    currentFilter() {
      this.fetchOrders();
    }
  },
  mounted() {
    this.fetchOrders();
  },
  methods: {
    async fetchOrders() {
      this.loading = true;
      try {
        const params = {};
        if (this.currentFilter !== 'All') {
          params.status = this.currentFilter;
        }

        const res = await api.get('/user/orders', { params });
        
        // Map API response to match template structure if needed, 
        // though your API response matches well.
        // We added 'realId' because your API returns 'id' as order_number string ("ORD-123"), 
        // but 'downloadInvoice' endpoint expects an INT ID usually? 
        // NOTE: Your API snippet uses <int:order_id> but stores strings like "ORD-..."
        // FIX: The backend should ideally accept the string order_number or return the numeric ID separately.
        // Assuming API returns numeric ID in a field or accepts logic.
        // For now, mapping directly.
        this.orders = res.data.data.map(o => ({
            ...o,
            realId: o.id // Assuming 'id' from API is the identifier
        }));

      } catch (err) {
        console.error("Failed to load orders", err);
        if (err.response && err.response.status === 401) {
           this.$router.push('/login');
        }
      } finally {
        this.loading = false;
      }
    },

    handleNavigation(path) {
      // Support query params logic
      if (path.includes('?')) {
         const [name, queryStr] = path.split('?');
         const params = new URLSearchParams(queryStr);
         this.$router.push({ path: name, query: Object.fromEntries(params) });
      } else {
         this.$router.push(`/${path}`);
      }
    },

    async downloadInvoice(orderId) {
      try {
        // Find the numeric ID if your API requires integer, 
        // OR pass the string ID if your API supports it.
        // Based on your API snippet: @user_bp.route('/user/orders/<int:order_id>/invoice')
        // You MUST pass the INTEGER ID.
        // Since your list API returned "id": order.order_number (String),
        // YOU NEED TO UPDATE YOUR API to return the numeric 'pk' (primary key) separately (e.g. "pk": order.id).
        
        // Assuming we pass whatever ID we have for now:
        const res = await api.get(`/user/orders/${orderId}/invoice`);
        alert(res.data.msg + " " + res.data.order_id);
      } catch (err) {
        alert("Failed to download invoice");
      }
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
/* Reused Styles */
.bg-light-subtle { background-color: #f9fafb !important; }
.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }
.transition-all { transition: all 0.2s ease; }
.btn-white { background-color: #fff; color: #6c757d; border-color: #dee2e6; }
.btn-white:hover { background-color: #f8f9fa; color: #000; border-color: #000; }
.hover-dark:hover { color: #000 !important; text-decoration: underline !important; }
.hover-lift { transition: transform 0.2s ease, box-shadow 0.2s ease; }
.hover-lift:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.hover-fill { transition: all 0.2s ease; }
.hover-fill:hover { background-color: #000; color: #fff; }
.animate-fade-up { animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; opacity: 0; transform: translateY(20px); }
@keyframes fadeUp { to { opacity: 1; transform: translateY(0); } }
@media (min-width: 768px) { .border-start-md { border-left: 1px solid #dee2e6; } }
.hide-scrollbar::-webkit-scrollbar { display: none; }
.hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>