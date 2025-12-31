<template>
  <div class="d-flex flex-column min-vh-100 bg-light-subtle">
    
    <nav class="navbar navbar-expand-lg navbar-dark bg-black sticky-top py-3">
      <div class="container px-lg-5">
        <a class="navbar-brand fw-bold tracking-tight fs-4" href="#">
          MARKETHUB <span class="text-secondary fw-normal fs-6 ps-2">| &nbsp;Admin</span>
        </a>
        
        <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#adminNav">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="adminNav">
          <ul class="navbar-nav ms-auto gap-lg-4 mb-2 mb-lg-0 align-items-lg-center">
            <li class="nav-item"><a class="nav-link text-white-50 fw-medium" href="#" @click="$emit('navigate', 'admin-dashboard')">Dashboard</a></li>
            <li class="nav-item"><a class="nav-link text-white-50 fw-medium" href="#" @click="$emit('navigate', 'admin-products')">Products</a></li>
            <li class="nav-item"><a class="nav-link text-white-50 fw-medium" href="#" @click="$emit('navigate', 'admin-orders')">Orders</a></li>
            <li class="nav-item"><a class="nav-link text-white-50 fw-medium" href="#" @click="$emit('navigate', 'admin-users')">Users</a></li>
            <li class="nav-item"><a class="nav-link text-white-50 fw-medium" href="#" @click="$emit('navigate', 'admin-messages')">Messages</a></li>
            <li class="nav-item"><a class="nav-link active fw-medium" href="#">Analytics</a></li>
            <li class="nav-item ms-lg-3">
              <button class="btn btn-outline-light rounded-pill px-4 btn-sm fw-bold text-uppercase tracking-wide">Log Out</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <main class="flex-grow-1 py-5">
      <div class="container px-lg-5">
        
        <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-end mb-5 gap-4 animate-fade-up">
          <div>
            <h1 class="display-5 fw-bold tracking-tight mb-2">Business Reports</h1>
            <p class="text-muted lead fs-6 mb-0">Track store performance, revenue, and user behavior.</p>
          </div>
          
          <div class="d-flex gap-2">
            <select class="form-select border shadow-sm rounded-pill fw-bold text-uppercase extra-small tracking-wide bg-white px-4 py-2" style="width: auto;">
              <option>Last 7 Days</option>
              <option selected>Last 30 Days</option>
              <option>This Year</option>
            </select>
            
            <button class="btn btn-dark rounded-pill px-4 py-2 fw-bold text-uppercase extra-small tracking-wide hover-lift shadow-sm" @click="exportReport">
              <i class="bi bi-download me-2"></i> Export
            </button>
          </div>
        </div>

        <div class="row row-cols-1 row-cols-sm-2 row-cols-xl-4 g-4 mb-5 animate-fade-up delay-100">
          
          <div class="col">
            <div class="card border-0 shadow-sm rounded-4 h-100 p-4 hover-lift transition-all">
              <div class="d-flex justify-content-between mb-3">
                <div class="bg-light rounded-circle d-flex align-items-center justify-content-center" style="width: 48px; height: 48px;">
                  <i class="bi bi-currency-rupee fs-5 text-dark"></i>
                </div>
                <span class="badge bg-success-subtle text-success rounded-pill px-2 py-1 extra-small fw-bold border border-success-subtle d-flex align-items-center">
                  <i class="bi bi-arrow-up-short fs-6"></i> 12.5%
                </span>
              </div>
              <h3 class="fw-bold tracking-tight mb-1">₹4,20,000</h3>
              <span class="text-muted small text-uppercase tracking-wide fw-bold">Total Revenue</span>
            </div>
          </div>

          <div class="col">
            <div class="card border-0 shadow-sm rounded-4 h-100 p-4 hover-lift transition-all">
              <div class="d-flex justify-content-between mb-3">
                <div class="bg-light rounded-circle d-flex align-items-center justify-content-center" style="width: 48px; height: 48px;">
                  <i class="bi bi-bag-check fs-5 text-dark"></i>
                </div>
                <span class="badge bg-success-subtle text-success rounded-pill px-2 py-1 extra-small fw-bold border border-success-subtle d-flex align-items-center">
                  <i class="bi bi-arrow-up-short fs-6"></i> 5.2%
                </span>
              </div>
              <h3 class="fw-bold tracking-tight mb-1">1,240</h3>
              <span class="text-muted small text-uppercase tracking-wide fw-bold">Total Orders</span>
            </div>
          </div>

          <div class="col">
            <div class="card border-0 shadow-sm rounded-4 h-100 p-4 hover-lift transition-all">
              <div class="d-flex justify-content-between mb-3">
                <div class="bg-light rounded-circle d-flex align-items-center justify-content-center" style="width: 48px; height: 48px;">
                  <i class="bi bi-people fs-5 text-dark"></i>
                </div>
                <span class="badge bg-warning-subtle text-warning-emphasis rounded-pill px-2 py-1 extra-small fw-bold border border-warning-subtle d-flex align-items-center">
                  <i class="bi bi-arrow-right-short fs-6"></i> 0.8%
                </span>
              </div>
              <h3 class="fw-bold tracking-tight mb-1">760</h3>
              <span class="text-muted small text-uppercase tracking-wide fw-bold">Active Users</span>
            </div>
          </div>

          <div class="col">
            <div class="card border-0 shadow-sm rounded-4 h-100 p-4 hover-lift transition-all">
              <div class="d-flex justify-content-between mb-3">
                <div class="bg-light rounded-circle d-flex align-items-center justify-content-center" style="width: 48px; height: 48px;">
                  <i class="bi bi-arrow-repeat fs-5 text-dark"></i>
                </div>
                <span class="badge bg-light text-muted rounded-pill px-2 py-1 extra-small fw-bold border d-flex align-items-center">
                  Stable
                </span>
              </div>
              <h3 class="fw-bold tracking-tight mb-1">32%</h3>
              <span class="text-muted small text-uppercase tracking-wide fw-bold">Return Customer Rate</span>
            </div>
          </div>

        </div>

        <div class="row g-4 mb-5 animate-fade-up delay-200">
          
          <div class="col-lg-8">
            <div class="card border-0 shadow-sm rounded-4 p-4 h-100">
              <div class="d-flex justify-content-between align-items-center mb-4">
                <h5 class="fw-bold mb-0">Revenue Trend</h5>
                <button class="btn btn-sm btn-white border rounded-circle shadow-sm">
                  <i class="bi bi-three-dots"></i>
                </button>
              </div>
              <div class="chart-container" style="position: relative; height: 300px;">
                <canvas id="revenueChart"></canvas>
              </div>
            </div>
          </div>

          <div class="col-lg-4">
            <div class="card border-0 shadow-sm rounded-4 p-4 h-100">
              <div class="d-flex justify-content-between align-items-center mb-4">
                <h5 class="fw-bold mb-0">Order Status</h5>
                <button class="btn btn-sm btn-white border rounded-circle shadow-sm">
                  <i class="bi bi-three-dots"></i>
                </button>
              </div>
              <div class="chart-container d-flex align-items-center justify-content-center" style="position: relative; height: 250px;">
                <canvas id="statusChart"></canvas>
              </div>
              <div class="mt-4 text-center">
                 <span class="text-muted extra-small">Total Orders: 1,240</span>
              </div>
            </div>
          </div>

        </div>

        <div class="row g-4 animate-fade-up delay-300">
          
          <div class="col-lg-6">
            <div class="card border-0 shadow-sm rounded-4 p-4 h-100">
              <h5 class="fw-bold mb-4">Top Categories</h5>
              <div class="chart-container" style="position: relative; height: 250px;">
                <canvas id="categoryChart"></canvas>
              </div>
            </div>
          </div>

          <div class="col-lg-6">
            <div class="card border-0 shadow-sm rounded-4 p-4 h-100">
              <h5 class="fw-bold mb-4">Performance Insights</h5>
              
              <div class="list-group list-group-flush">
                
                <div class="list-group-item px-0 border-light-subtle d-flex align-items-center justify-content-between py-3">
                  <div class="d-flex align-items-center gap-3">
                    <div class="bg-light rounded-circle d-flex align-items-center justify-content-center text-muted" style="width: 40px; height: 40px;">
                      <i class="bi bi-cart"></i>
                    </div>
                    <div>
                      <span class="d-block fw-bold small text-dark">Average Order Value</span>
                      <span class="d-block extra-small text-muted">Per transaction</span>
                    </div>
                  </div>
                  <span class="fw-bold">₹3,250</span>
                </div>

                <div class="list-group-item px-0 border-light-subtle d-flex align-items-center justify-content-between py-3">
                  <div class="d-flex align-items-center gap-3">
                    <div class="bg-light rounded-circle d-flex align-items-center justify-content-center text-muted" style="width: 40px; height: 40px;">
                      <i class="bi bi-eye"></i>
                    </div>
                    <div>
                      <span class="d-block fw-bold small text-dark">Most Viewed Product</span>
                      <span class="d-block extra-small text-muted">Linen Lounge Chair</span>
                    </div>
                  </div>
                  <span class="fw-bold">12.5k Views</span>
                </div>

                <div class="list-group-item px-0 border-light-subtle d-flex align-items-center justify-content-between py-3">
                  <div class="d-flex align-items-center gap-3">
                    <div class="bg-light rounded-circle d-flex align-items-center justify-content-center text-muted" style="width: 40px; height: 40px;">
                      <i class="bi bi-star"></i>
                    </div>
                    <div>
                      <span class="d-block fw-bold small text-dark">Highest Rated Item</span>
                      <span class="d-block extra-small text-muted">Ceramic Vase Set</span>
                    </div>
                  </div>
                  <span class="fw-bold">4.9/5.0</span>
                </div>
                 
                <div class="list-group-item px-0 border-0 d-flex align-items-center justify-content-between py-3">
                  <div class="d-flex align-items-center gap-3">
                    <div class="bg-light rounded-circle d-flex align-items-center justify-content-center text-muted" style="width: 40px; height: 40px;">
                      <i class="bi bi-geo-alt"></i>
                    </div>
                    <div>
                      <span class="d-block fw-bold small text-dark">Top Region</span>
                      <span class="d-block extra-small text-muted">Based on delivery addresses</span>
                    </div>
                  </div>
                  <span class="fw-bold">Mumbai, MH</span>
                </div>

              </div>
            </div>
          </div>

        </div>

      </div>
    </main>

    <footer class="bg-white border-top py-4 text-center mt-auto">
      <p class="text-muted extra-small mb-0 text-uppercase tracking-wide">
        &copy; 2025 MarketHub Admin Panel.
      </p>
    </footer>

  </div>
</template>

<script>
// IMPORTANT: You must install chart.js to use this component
// Run: npm install chart.js
import Chart from 'chart.js/auto';

export default {
  name: "AdminAnalytics",
  data() {
    return {
      revenueChart: null,
      statusChart: null,
      categoryChart: null
    };
  },
  mounted() {
    this.initCharts();
  },
  methods: {
    exportReport() {
      alert("Preparing PDF report for download...");
    },
    initCharts() {
      // 1. Revenue Chart (Line)
      const ctxRevenue = document.getElementById('revenueChart');
      if (ctxRevenue) {
        this.revenueChart = new Chart(ctxRevenue, {
          type: 'line',
          data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
              label: 'Revenue (₹)',
              data: [120000, 150000, 180000, 220000, 200000, 250000, 310000, 290000, 350000, 380000, 410000, 420000],
              borderColor: '#000000', // Premium Black
              backgroundColor: 'rgba(0, 0, 0, 0.05)',
              tension: 0.4, // Smooth curve
              borderWidth: 2,
              pointRadius: 0,
              pointHoverRadius: 6,
              fill: true
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false },
              tooltip: { 
                backgroundColor: '#000', 
                titleColor: '#fff', 
                padding: 10, 
                cornerRadius: 4 
              }
            },
            scales: {
              x: { grid: { display: false } },
              y: { 
                grid: { borderDash: [5, 5] }, 
                ticks: { callback: (val) => '₹' + val / 1000 + 'k' } 
              }
            }
          }
        });
      }

      // 2. Order Status Chart (Doughnut)
      const ctxStatus = document.getElementById('statusChart');
      if (ctxStatus) {
        this.statusChart = new Chart(ctxStatus, {
          type: 'doughnut',
          data: {
            labels: ['Delivered', 'Pending', 'Processing', 'Cancelled'],
            datasets: [{
              data: [65, 15, 12, 8],
              backgroundColor: [
                '#198754', // Green (Delivered)
                '#6c757d', // Grey (Pending)
                '#ffc107', // Yellow (Processing)
                '#dc3545'  // Red (Cancelled)
              ],
              borderWidth: 0,
              hoverOffset: 4
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '75%', // Modern thin ring
            plugins: {
              legend: { 
                position: 'bottom', 
                labels: { usePointStyle: true, boxWidth: 8, padding: 20, font: { size: 11 } } 
              }
            }
          }
        });
      }

      // 3. Categories Chart (Bar)
      const ctxCategory = document.getElementById('categoryChart');
      if (ctxCategory) {
        this.categoryChart = new Chart(ctxCategory, {
          type: 'bar',
          data: {
            labels: ['Furniture', 'Lighting', 'Decor', 'Electronics', 'Acc.'],
            datasets: [{
              label: 'Sales',
              data: [450, 320, 280, 150, 90],
              backgroundColor: '#000000',
              borderRadius: 4,
              barThickness: 20
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false }
            },
            scales: {
              x: { grid: { display: false } },
              y: { display: false } // Minimal look
            }
          }
        });
      }
    }
  }
};
</script>

<style scoped>
/* ADMIN THEME STYLES */

/* Backgrounds */
.bg-light-subtle { background-color: #f9fafb !important; }

/* Typography */
.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }

/* Animations */
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

/* Interactions */
.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.transition-all { transition: all 0.2s ease; }

/* Buttons */
.btn-white {
  background-color: #fff; color: #000; border-color: #dee2e6;
}
.btn-white:hover { border-color: #000; }

/* List Group */
.list-group-item {
  background-color: transparent;
}
</style>