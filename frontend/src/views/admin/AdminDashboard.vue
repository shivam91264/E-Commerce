<template>
  <div class="d-flex flex-column min-vh-100 bg-light-subtle">
    
    <main class="flex-grow-1 py-5">
      <div class="container px-lg-5">
        
        <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-5 gap-3 animate-fade-up">
          <div>
            <h1 class="display-5 fw-bold tracking-tight mb-2">Overview</h1>
            <p class="text-muted lead fs-6 mb-0">Monitor your business performance and store operations.</p>
          </div>
          
          <div class="d-flex gap-2">
             <span class="badge bg-white text-dark border shadow-sm px-3 py-2 rounded-pill fw-normal">
               <i class="bi bi-calendar3 me-2"></i> Last 30 Days
             </span>
          </div>
        </div>

        <div class="row row-cols-1 row-cols-sm-2 row-cols-xl-4 g-4 mb-5 animate-fade-up delay-100">
          <div class="col" v-for="(stat, index) in stats" :key="index">
            <div class="card border-0 shadow-sm rounded-4 h-100 p-4 hover-lift transition-all">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <div class="bg-light rounded-circle d-flex align-items-center justify-content-center" style="width: 48px; height: 48px;">
                  <i :class="stat.icon" class="fs-5 text-dark"></i>
                </div>
                <span class="badge rounded-pill px-2 py-1 extra-small fw-bold" :class="stat.trendUp ? 'bg-success-subtle text-success' : 'bg-danger-subtle text-danger'">
                  <i :class="stat.trendUp ? 'bi bi-arrow-up' : 'bi bi-arrow-down'"></i> {{ stat.trend }}
                </span>
              </div>
              <h3 class="fw-bold tracking-tight mb-1">{{ stat.value }}</h3>
              <span class="text-muted small text-uppercase tracking-wide fw-bold">{{ stat.label }}</span>
            </div>
          </div>
        </div>

        <div class="row g-5">
          
          <div class="col-lg-8 animate-fade-up delay-200">
            <div class="card border-0 shadow-sm rounded-4 overflow-hidden h-100">
              <div class="card-header bg-white p-4 border-bottom d-flex justify-content-between align-items-center">
                <h5 class="fw-bold mb-0">Recent Orders</h5>
                <a href="#" class="text-decoration-none small fw-bold text-dark text-uppercase tracking-wide hover-underline">View All</a>
              </div>
              <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                  <thead class="bg-light">
                    <tr>
                      <th class="ps-4 py-3 text-uppercase extra-small text-muted fw-bold border-0">Order ID</th>
                      <th class="py-3 text-uppercase extra-small text-muted fw-bold border-0">Customer</th>
                      <th class="py-3 text-uppercase extra-small text-muted fw-bold border-0">Status</th>
                      <th class="py-3 text-uppercase extra-small text-muted fw-bold border-0 text-end">Amount</th>
                      <th class="pe-4 py-3 text-uppercase extra-small text-muted fw-bold border-0 text-end">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="order in recentOrders" :key="order.id" class="cursor-pointer">
                      <td class="ps-4 py-3 fw-bold small font-monospace">{{ order.id }}</td>
                      <td class="py-3 small">
                        <div class="d-flex align-items-center gap-2">
                          <div class="bg-light rounded-circle d-flex align-items-center justify-content-center fw-bold extra-small text-muted" style="width: 32px; height: 32px;">
                            {{ order.initials }}
                          </div>
                          {{ order.customer }}
                        </div>
                      </td>
                      <td class="py-3">
                        <span class="badge rounded-pill border px-2 py-1 extra-small fw-bold text-uppercase" :class="getStatusClass(order.status)">
                          {{ order.status }}
                        </span>
                      </td>
                      <td class="py-3 text-end fw-medium small">{{ order.amount }}</td>
                      <td class="pe-4 py-3 text-end">
                        <button class="btn btn-sm btn-white border rounded-circle shadow-sm" style="width: 32px; height: 32px;">
                          <i class="bi bi-chevron-right extra-small"></i>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <div class="col-lg-4 animate-fade-up delay-300">
            
            <div class="card border-0 shadow-sm rounded-4 p-4 mb-4">
              <h5 class="fw-bold mb-4">Quick Actions</h5>
              <div class="row g-3">
                <div class="col-6">
                  <button class="btn btn-dark w-100 py-3 rounded-3 h-100 d-flex flex-column align-items-center justify-content-center gap-2 hover-scale">
                    <i class="bi bi-plus-lg fs-4"></i>
                    <span class="extra-small text-uppercase fw-bold">Add Product</span>
                  </button>
                </div>
                <div class="col-6">
                  <button class="btn btn-light border w-100 py-3 rounded-3 h-100 d-flex flex-column align-items-center justify-content-center gap-2 hover-bg-gray">
                    <i class="bi bi-box-seam fs-5 text-muted"></i>
                    <span class="extra-small text-uppercase fw-bold text-muted">Orders</span>
                  </button>
                </div>
                <div class="col-6">
                  <button class="btn btn-light border w-100 py-3 rounded-3 h-100 d-flex flex-column align-items-center justify-content-center gap-2 hover-bg-gray">
                    <i class="bi bi-people fs-5 text-muted"></i>
                    <span class="extra-small text-uppercase fw-bold text-muted">Users</span>
                  </button>
                </div>
                <div class="col-6">
                  <button class="btn btn-light border w-100 py-3 rounded-3 h-100 d-flex flex-column align-items-center justify-content-center gap-2 hover-bg-gray">
                    <i class="bi bi-chat-dots fs-5 text-muted"></i>
                    <span class="extra-small text-uppercase fw-bold text-muted">Support</span>
                  </button>
                </div>
              </div>
            </div>

            <div class="card border-0 shadow-sm rounded-4 p-4 text-center bg-white position-relative overflow-hidden">
              <div class="position-relative z-2 py-3">
                <div class="mb-3 d-inline-flex align-items-center justify-content-center bg-light rounded-circle text-muted" style="width: 60px; height: 60px;">
                  <i class="bi bi-bar-chart-line fs-3"></i>
                </div>
                <h5 class="fw-bold mb-2">Analytics Insights</h5>
                <p class="text-muted small mb-3 px-3">
                  Detailed sales charts and traffic analysis integration coming soon.
                </p>
                <button class="btn btn-outline-dark rounded-pill px-4 btn-sm fw-bold text-uppercase extra-small tracking-wide disabled">
                  Coming Soon
                </button>
              </div>
            </div>

          </div>

        </div>
      </div>
    </main>

  </div>
</template>

<script>

export default {
  name: "AdminDashboard",
  data() {
    return {
      stats: [
        { label: "Total Revenue", value: "$124,500", trend: "12%", trendUp: true, icon: "bi bi-currency-dollar" },
        { label: "Total Orders", value: "1,280", trend: "8%", trendUp: true, icon: "bi bi-bag-check" },
        { label: "Active Products", value: "340", trend: "Stable", trendUp: true, icon: "bi bi-tag" },
        { label: "Registered Users", value: "860", trend: "2%", trendUp: false, icon: "bi bi-people" }
      ],
      recentOrders: [
        { id: "#8392", customer: "Alex Morgan", initials: "AM", amount: "$329.00", status: "New", date: "Just now" },
        { id: "#8391", customer: "Sarah Jenkins", initials: "SJ", amount: "$120.50", status: "Shipped", date: "2 hrs ago" },
        { id: "#8390", customer: "Michael Chen", initials: "MC", amount: "$89.00", status: "Processing", date: "5 hrs ago" },
        { id: "#8389", customer: "David Kim", initials: "DK", amount: "$450.00", status: "Delivered", date: "Yesterday" },
        { id: "#8388", customer: "Emily Blunt", initials: "EB", amount: "$65.00", status: "Cancelled", date: "Yesterday" },
      ]
    };
  },
  methods: {
    logout() {
      if(confirm("Exit Admin Panel?")) {
        console.log("Logging out admin...");
        // Redirect to Login
      }
    },
    getStatusClass(status) {
      switch(status) {
        case 'New': return 'bg-primary-subtle text-primary border-primary-subtle';
        case 'Shipped': return 'bg-info-subtle text-info-emphasis border-info-subtle';
        case 'Processing': return 'bg-warning-subtle text-warning-emphasis border-warning-subtle';
        case 'Delivered': return 'bg-success-subtle text-success border-success-subtle';
        case 'Cancelled': return 'bg-secondary-subtle text-secondary border-secondary-subtle';
        default: return 'bg-light text-dark';
      }
    }
  }
};
</script>

<style scoped>
/* ADMIN THEME OVERRIDES */

/* Backgrounds */
.bg-light-subtle { background-color: #f9fafb !important; }

/* Typography */
.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }

/* Navbar Overrides */
.navbar-brand { font-family: system-ui, -apple-system, sans-serif; }
.nav-link { font-size: 0.9rem; transition: color 0.2s; }
.nav-link:hover, .nav-link.active { color: #fff !important; }

/* Animations & Transitions */
.transition-all { transition: all 0.2s ease; }

.animate-fade-up {
  animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
  transform: translateY(20px);
}
.delay-100 { animation-delay: 0.1s; }
.delay-200 { animation-delay: 0.2s; }
.delay-300 { animation-delay: 0.3s; }

@keyframes fadeUp {
  to { opacity: 1; transform: translateY(0); }
}

/* Card Interactions */
.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.hover-lift:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.05) !important;
}

.hover-scale:hover { transform: scale(1.02); }
.hover-bg-gray:hover { background-color: #f1f3f5 !important; }
.hover-underline:hover { text-decoration: underline !important; }

/* Table Styling */
.table-hover tbody tr:hover { background-color: #f8f9fa; }
.cursor-pointer { cursor: pointer; }

/* Button Styling */
.btn-white { background: #fff; color: #000; border-color: #dee2e6; }
.btn-white:hover { border-color: #000; }
</style>