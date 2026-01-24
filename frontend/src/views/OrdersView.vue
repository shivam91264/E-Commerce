<template>
  <div class="d-flex flex-column min-vh-100 bg-light-subtle">
    
    <main class="flex-grow-1 py-5">
      <div class="container px-lg-5">
        
        <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-end mb-5 gap-4 animate-fade-up">
          <div>
            <h1 class="display-5 fw-bold tracking-tight mb-2">Order History</h1>
            <p class="text-muted lead fs-6 mb-0">Track, return, or buy things again.</p>
          </div>
          
          <div class="d-flex align-items-center gap-3">
            <label class="text-muted extra-small fw-bold text-uppercase tracking-wide mb-0">Filter By:</label>
            <div class="position-relative">
              <select 
                class="form-select rounded-pill px-4 py-2 fw-bold text-dark border-secondary-subtle shadow-sm cursor-pointer" 
                style="min-width: 180px;"
                v-model="currentFilter"
              >
                <option value="All">Show All Orders</option>
                <option value="Pending">Pending</option>
                <option value="Processing">Processing</option>
                <option value="Shipped">Shipped</option>
                <option value="Delivered">Delivered</option>
                <option value="Cancelled">Cancelled</option>
              </select>
            </div>
          </div>
        </div>

        <div v-if="loading" class="text-center py-5">
           <div class="spinner-border text-dark" role="status"></div>
        </div>

        <div v-else-if="orders.length === 0" class="text-center py-6 animate-fade-up">
          <div class="bg-white d-inline-flex p-4 rounded-circle shadow-sm mb-4">
            <i class="bi bi-box-seam display-4 text-muted opacity-25"></i>
          </div>
          <h3 class="fw-bold mb-3">No orders found</h3>
          <p class="text-muted mb-4">
            No orders found with status "<strong>{{ currentFilter }}</strong>".
          </p>
          <button class="btn btn-dark rounded-pill px-5 py-3 text-uppercase fw-bold tracking-wide hover-lift" @click="currentFilter = 'All'">
            Show All Orders
          </button>
        </div>

        <div v-else class="row justify-content-center">
          <div class="col-lg-10 col-xl-9">
            
            <div 
              v-for="(order, index) in orders" 
              :key="order.id" 
              class="card border-0 shadow-sm rounded-4 mb-5 overflow-hidden animate-fade-up"
              :style="{ animationDelay: `${index * 100}ms` }"
            >
              
              <div class="card-header bg-light border-bottom border-light-subtle p-4">
                <div class="row align-items-center g-3">
                  <div class="col-6 col-md-3">
                    <span class="d-block text-muted extra-small text-uppercase tracking-wide fw-bold mb-1">Order Placed</span>
                    <span class="fw-bold text-dark small">{{ order.formattedDate }}</span>
                  </div>
                  <div class="col-6 col-md-2">
                    <span class="d-block text-muted extra-small text-uppercase tracking-wide fw-bold mb-1">Total</span>
                    <span class="fw-bold text-dark small">${{ order.displayTotal }}</span>
                  </div>
                  <div class="col-6 col-md-3">
                    <span class="d-block text-muted extra-small text-uppercase tracking-wide fw-bold mb-1">Order #</span>
                    <span class="fw-bold text-dark small font-monospace">{{ order.order_number }}</span>
                  </div>
                  <div class="col-12 col-md-4 text-md-end">
                    
                    <button 
                      @click="downloadInvoice(order)" 
                      class="btn btn-link text-decoration-none text-muted p-0 extra-small fw-bold text-uppercase d-inline-flex align-items-center gap-2 hover-dark"
                    >
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
                        <p class="text-muted small mb-0">{{ order.deliveryMsg || 'Status Updated' }}</p>
                      </div>

                      <div class="d-flex flex-column gap-3">
                        <div v-for="(item, i) in order.items" :key="i" class="d-flex gap-3 align-items-center">
                           <div class="ratio ratio-1x1 bg-light rounded-3 overflow-hidden border" style="width: 80px; min-width: 80px;">
                             <img :src="item.image || 'https://via.placeholder.com/150'" class="object-fit-cover w-100 h-100" alt="Product">
                           </div>
                           
                           <div>
                             <h6 class="fw-bold text-dark mb-1 d-block text-decoration-none">
                               {{ item.mappedName }}
                             </h6>
                             <span class="text-muted small">Qty: {{ item.mappedQty }}</span>
                           </div>
                        </div>
                      </div>
                  </div>

                  <div class="col-md-4 d-flex flex-column justify-content-center align-items-md-end gap-2 border-start-md ps-md-4">
                      <button @click="handleNavigation(order.order_number)" class="btn btn-dark w-100 rounded-pill py-2 fw-bold text-uppercase extra-small hover-lift">
                        View Order
                      </button>
                      <button v-if="order.status === 'Delivered'" class="btn btn-outline-dark w-100 rounded-pill py-2 fw-bold text-uppercase extra-small hover-fill">
                        Buy Again
                      </button>
                      <button v-else class="btn btn-light border w-100 rounded-pill py-2 fw-bold text-uppercase extra-small text-muted">
                        Track Package
                      </button>
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

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';

const loading = ref(true);
const currentFilter = ref('All'); 
const orders = ref([]);
const router = useRouter();

const fetchOrders = async () => {
  loading.value = true;
  try {
    const params = {};
    // Ensure we only pass status if it's NOT 'All'
    if (currentFilter.value && currentFilter.value !== 'All') {
      params.status = currentFilter.value;
    }

    console.log("Fetching orders with params:", params); // Debug log

    const res = await api.get('/user/orders', { params });
    
    const rawData = res.data.data || res.data; 

    if (Array.isArray(rawData)) {
      orders.value = rawData.map(order => {
        return {
          ...order,
          displayTotal: order.total || order.total_amount,
          formattedDate: order.date || new Date(order.created_at).toLocaleDateString(),
          items: order.items.map(item => ({
            ...item,
            mappedName: item.name || item.product_name || "Unknown Product",
            mappedQty: item.qty || item.quantity || 1,
            image: item.image || "https://via.placeholder.com/150"
          }))
        };
      });
    } else {
      orders.value = [];
    }

  } catch (err) {
    console.error("Failed to load orders", err);
  } finally {
    loading.value = false;
  }
};

// Generate Invoice HTML and Trigger Print to PDF
const downloadInvoice = (order) => {
  const invoiceWindow = window.open('', '_blank');
  
  const itemsHtml = order.items.map(item => `
    <tr>
      <td style="padding: 10px; border-bottom: 1px solid #ddd;">${item.mappedName}</td>
      <td style="padding: 10px; border-bottom: 1px solid #ddd;">${item.mappedQty}</td>
    </tr>
  `).join('');

  const htmlContent = `
    <html>
      <head>
        <title>Invoice - ${order.order_number}</title>
        <style>
          body { font-family: 'Helvetica', sans-serif; padding: 40px; color: #333; }
          .header { text-align: center; margin-bottom: 40px; border-bottom: 2px solid #000; padding-bottom: 20px; }
          .meta { margin-bottom: 30px; }
          table { width: 100%; border-collapse: collapse; margin-bottom: 30px; }
          th { text-align: left; background: #f4f4f4; padding: 10px; }
          .total { text-align: right; font-size: 1.5em; font-weight: bold; }
          .footer { margin-top: 50px; text-align: center; font-size: 0.8em; color: #777; }
        </style>
      </head>
      <body>
        <div class="header">
          <h1>INVOICE</h1>
          <p>Order #${order.order_number}</p>
        </div>
        
        <div class="meta">
          <p><strong>Date:</strong> ${order.formattedDate}</p>
          <p><strong>Status:</strong> ${order.status}</p>
        </div>

        <table>
          <thead>
            <tr>
              <th>Item Name</th>
              <th>Quantity</th>
            </tr>
          </thead>
          <tbody>
            ${itemsHtml}
          </tbody>
        </table>

        <div class="total">
          TOTAL PAID: $${order.displayTotal}
        </div>

        <div class="footer">
          <p>Thank you for shopping with MarketHub!</p>
        </div>
      </body>
    </html>
  `;

  invoiceWindow.document.write(htmlContent);
  invoiceWindow.document.close();
  
  // Wait for content to load then trigger print
  setTimeout(() => {
    invoiceWindow.focus();
    invoiceWindow.print();
  }, 500);
};

const handleNavigation = (orderNumber) => {
  router.push(`/order/${orderNumber}`);
};

const getStatusColor = (status) => {
  switch(status) {
    case 'Delivered': return 'text-success';
    case 'Shipped': return 'text-primary';
    case 'Processing': return 'text-info'; 
    case 'Pending': return 'text-warning';
    case 'Cancelled': return 'text-danger';
    default: return 'text-dark';
  }
};

// Re-fetch whenever the dropdown selection changes
watch(currentFilter, () => {
  fetchOrders();
});

onMounted(() => {
  fetchOrders();
});
</script>

<style scoped>
/* Keeping your existing styles */
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
.cursor-pointer { cursor: pointer; }
</style>