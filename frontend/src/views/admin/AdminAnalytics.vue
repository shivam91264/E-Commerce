<template>
  <div class="d-flex flex-column min-vh-100 bg-light-subtle">
    
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

        <div v-if="summary" class="row row-cols-1 row-cols-sm-2 row-cols-xl-4 g-4 mb-5 animate-fade-up delay-100">
          
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
              <h3 class="fw-bold tracking-tight mb-1">{{ formatCurrency(summary.revenue) }}</h3>
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
              <h3 class="fw-bold tracking-tight mb-1">{{ summary.total_orders }}</h3>
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
              <h3 class="fw-bold tracking-tight mb-1">{{ summary.active_users }}</h3>
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
              <h3 class="fw-bold tracking-tight mb-1">{{ summary.return_rate }}%</h3>
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
                 <span class="text-muted extra-small">Total Orders: {{ summary ? summary.total_orders : 0 }}</span>
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
              
              <div class="list-group list-group-flush" v-if="insights">
                
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
                  <span class="fw-bold">{{ formatCurrency(insights.avg_order_value) }}</span>
                </div>

                <div class="list-group-item px-0 border-light-subtle d-flex align-items-center justify-content-between py-3">
                  <div class="d-flex align-items-center gap-3">
                    <div class="bg-light rounded-circle d-flex align-items-center justify-content-center text-muted" style="width: 40px; height: 40px;">
                      <i class="bi bi-eye"></i>
                    </div>
                    <div>
                      <span class="d-block fw-bold small text-dark">Most Viewed Product</span>
                      <span class="d-block extra-small text-muted">Trending now</span>
                    </div>
                  </div>
                  <span class="fw-bold">{{ insights.most_viewed || 'N/A' }}</span>
                </div>

                <div class="list-group-item px-0 border-light-subtle d-flex align-items-center justify-content-between py-3">
                  <div class="d-flex align-items-center gap-3">
                    <div class="bg-light rounded-circle d-flex align-items-center justify-content-center text-muted" style="width: 40px; height: 40px;">
                      <i class="bi bi-star"></i>
                    </div>
                    <div>
                      <span class="d-block fw-bold small text-dark">Highest Rated Item</span>
                      <span class="d-block extra-small text-muted">{{ insights.highest_rated || 'No ratings yet' }}</span>
                    </div>
                  </div>
                  <span class="fw-bold">{{ insights.highest_rating ? insights.highest_rating + '/5.0' : '-' }}</span>
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
                  <span class="fw-bold">{{ insights.top_region }}</span>
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
import Chart from 'chart.js/auto';
import api from "@/services/api";

export default {
  name: "AdminAnalytics",
  data() {
    return {
      summary: null,
      insights: null,
      
      // Chart instances
      revenueChart: null,
      statusChart: null,
      categoryChart: null
    };
  },
  async mounted() {
    await this.fetchSummary();
    await this.fetchInsights();
    await this.fetchRevenueData();
    await this.fetchStatusData();
    await this.fetchCategoryData();
  },
  methods: {
    formatCurrency(value) {
      if (value === undefined || value === null) return '₹0';
      return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        maximumFractionDigits: 0
      }).format(value);
    },

    exportReport() {
      alert("Preparing PDF report for download...");
      // You can implement actual PDF download logic here later
    },

    // --- API Calls ---

    async fetchSummary() {
      try {
        const res = await api.get('/admin/summary');
        this.summary = res.data;
      } catch (error) {
        console.error("Summary load failed", error);
      }
    },

    async fetchInsights() {
      try {
        const res = await api.get('/admin/performance_insights');
        this.insights = res.data;
      } catch (error) {
        console.error("Insights load failed", error);
      }
    },

    // --- Chart 1: Revenue Trend ---
    async fetchRevenueData() {
      try {
        const res = await api.get('/admin/revenue_trend');
        const apiData = res.data.data; // [{month: '2023-01', revenue: 500}, ...]

        const labels = apiData.map(item => item.month);
        const values = apiData.map(item => item.revenue);

        this.renderRevenueChart(labels, values);
      } catch (error) {
        console.error("Revenue chart failed", error);
      }
    },

    renderRevenueChart(labels, data) {
      const ctx = document.getElementById('revenueChart');
      if (!ctx) return;

      if (this.revenueChart) this.revenueChart.destroy();

      this.revenueChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Revenue (₹)',
            data: data,
            borderColor: '#000000',
            backgroundColor: 'rgba(0, 0, 0, 0.05)',
            tension: 0.4,
            borderWidth: 2,
            pointRadius: 3,
            pointHoverRadius: 6,
            fill: true
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { display: false } },
            y: { 
              grid: { borderDash: [5, 5] }, 
              ticks: { callback: (val) => '₹' + val } 
            }
          }
        }
      });
    },

    // --- Chart 2: Order Status ---
    async fetchStatusData() {
      try {
        const res = await api.get('/admin/order_status');
        const apiData = res.data.data; // {'Delivered': 65, ...}

        const labels = Object.keys(apiData);
        const values = Object.values(apiData);

        this.renderStatusChart(labels, values);
      } catch (error) {
        console.error("Status chart failed", error);
      }
    },

    renderStatusChart(labels, data) {
      const ctx = document.getElementById('statusChart');
      if (!ctx) return;

      if (this.statusChart) this.statusChart.destroy();

      this.statusChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            backgroundColor: ['#198754', '#6c757d', '#ffc107', '#dc3545'],
            borderWidth: 0,
            hoverOffset: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '75%',
          plugins: {
            legend: { 
              position: 'bottom', 
              labels: { usePointStyle: true, boxWidth: 8, padding: 20, font: { size: 11 } } 
            }
          }
        }
      });
    },

    // --- Chart 3: Categories ---
    async fetchCategoryData() {
      try {
        const res = await api.get('/admin/category_stats');
        const apiData = res.data.data; // [{category: 'Name', count: 10}]

        const labels = apiData.map(item => item.category);
        const values = apiData.map(item => item.count);

        this.renderCategoryChart(labels, values);
      } catch (error) {
        console.error("Category chart failed", error);
      }
    },

    renderCategoryChart(labels, data) {
      const ctx = document.getElementById('categoryChart');
      if (!ctx) return;

      if (this.categoryChart) this.categoryChart.destroy();

      this.categoryChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Sales',
            data: data,
            backgroundColor: '#000000',
            borderRadius: 4,
            barThickness: 20
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { display: false } },
            y: { display: false }
          }
        }
      });
    }
  }
};
</script>

<style scoped>
/* ADMIN THEME STYLES */
.bg-light-subtle { background-color: #f9fafb !important; }
.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }

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

.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.transition-all { transition: all 0.2s ease; }

.btn-white {
  background-color: #fff; color: #000; border-color: #dee2e6;
}
.btn-white:hover { border-color: #000; }

.list-group-item {
  background-color: transparent;
}
</style>