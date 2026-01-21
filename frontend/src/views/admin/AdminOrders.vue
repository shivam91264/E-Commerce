<template>
  <div class="d-flex flex-column min-vh-100 bg-light-subtle">
    <main class="flex-grow-1 py-5">
      <div class="container px-lg-5">
        <div
          class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-5 gap-3 animate-fade-up"
        >
          <div>
            <h1 class="display-5 fw-bold tracking-tight mb-2">Manage Orders</h1>
            <p class="text-muted lead fs-6 mb-0">
              Track, review, and update customer orders.
            </p>
          </div>
          <div class="d-flex gap-2">
            <button
              class="btn btn-white border shadow-sm rounded-pill px-4 py-2 fw-bold text-uppercase extra-small tracking-wide"
            >
              <i class="bi bi-download me-2"></i> Export CSV
            </button>
          </div>
        </div>

        <div
          class="card border-0 shadow-sm rounded-4 p-3 mb-4 animate-fade-up delay-100"
        >
          <div class="row g-3 align-items-center">
            <div class="col-lg-5">
              <div class="position-relative">
                <i
                  class="bi bi-search position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"
                ></i>
                <input
                  type="text"
                  class="form-control border-0 bg-light rounded-pill ps-5"
                  placeholder="Search Order ID, Customer..."
                  v-model="searchQuery"
                />
              </div>
            </div>
            <div class="col-6 col-lg-3 ms-auto">
              <select
                class="form-select border-0 bg-light rounded-pill fs-6"
                v-model="filterStatus"
              >
                <option value="All">All Statuses</option>
                <option>Pending</option>
                <option>Processing</option>
                <option>Shipped</option>
                <option>Delivered</option>
                <option>Cancelled</option>
              </select>
            </div>
            <div class="col-6 col-lg-2">
              <input
                type="date"
                class="form-control border-0 bg-light rounded-pill fs-6 text-muted"
              />
            </div>
          </div>
        </div>

        <div
          class="card border-0 shadow-sm rounded-4 overflow-hidden animate-fade-up delay-200"
        >
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="bg-light">
                <tr>
                  <th
                    class="ps-4 py-3 text-uppercase extra-small text-muted fw-bold border-0"
                  >
                    Order ID
                  </th>
                  <th
                    class="py-3 text-uppercase extra-small text-muted fw-bold border-0"
                  >
                    Customer
                  </th>
                  <th
                    class="py-3 text-uppercase extra-small text-muted fw-bold border-0"
                  >
                    Date
                  </th>
                  <th
                    class="py-3 text-uppercase extra-small text-muted fw-bold border-0"
                  >
                    Items
                  </th>
                  <th
                    class="py-3 text-uppercase extra-small text-muted fw-bold border-0"
                  >
                    Total
                  </th>
                  <th
                    class="py-3 text-uppercase extra-small text-muted fw-bold border-0"
                  >
                    Status
                  </th>
                  <th
                    class="pe-4 py-3 text-uppercase extra-small text-muted fw-bold border-0 text-end"
                  >
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="order in filteredOrders"
                  :key="order.id"
                  class="cursor-pointer"
                  @click="openDetailsDrawer(order)"
                >
                  <td class="ps-4 py-3 fw-bold small font-monospace text-dark">
                    {{ order.id }}
                  </td>

                  <td class="py-3">
                    <div class="d-flex align-items-center gap-2">
                      <div
                        class="bg-light rounded-circle d-flex align-items-center justify-content-center fw-bold extra-small text-muted border"
                        style="width: 32px; height: 32px"
                      >
                        {{ order.initials }}
                      </div>
                      <div>
                        <span class="d-block fw-bold text-dark small">{{
                          order.customer
                        }}</span>
                        <span class="d-block extra-small text-muted">{{
                          order.email
                        }}</span>
                      </div>
                    </div>
                  </td>

                  <td class="py-3 small text-muted">{{ order.date }}</td>

                  <td class="py-3 small">{{ order.itemsCount }} items</td>

                  <td class="py-3 fw-bold small text-dark">
                    {{ order.total }}
                  </td>

                  <td class="py-3">
                    <span
                      class="badge rounded-pill border px-2 py-1 extra-small fw-bold text-uppercase"
                      :class="getStatusClass(order.status)"
                    >
                      {{ order.status }}
                    </span>
                  </td>

                  <td class="pe-4 py-3 text-end" @click.stop>
                    <div class="d-flex justify-content-end gap-2">
                      <button
                        class="btn btn-sm btn-white border rounded-circle shadow-sm"
                        title="View Details"
                        @click="openDetailsDrawer(order)"
                      >
                        <i class="bi bi-eye extra-small"></i>
                      </button>
                      <button
                        class="btn btn-sm btn-white border rounded-circle shadow-sm"
                        title="Update Status"
                        @click="openStatusModal(order)"
                      >
                        <i class="bi bi-pencil-square extra-small"></i>
                      </button>
                    </div>
                  </td>
                </tr>

                <tr v-if="filteredOrders.length === 0">
                  <td colspan="7" class="text-center py-5">
                    <div class="d-inline-flex p-3 rounded-circle bg-light mb-3">
                      <i class="bi bi-inbox text-muted fs-3"></i>
                    </div>
                    <p class="text-muted small mb-0">
                      No orders found matching your criteria.
                    </p>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="card-footer bg-white border-top p-3">
            <div class="d-flex justify-content-between align-items-center">
              <span class="text-muted extra-small"
                >Showing {{ filteredOrders.length }} orders</span
              >
              <nav>
                <ul class="pagination pagination-sm mb-0 gap-1">
                  <li class="page-item disabled">
                    <a
                      class="page-link rounded-circle border-0 text-dark"
                      href="#"
                      ><i class="bi bi-chevron-left"></i
                    ></a>
                  </li>
                  <li class="page-item active">
                    <a
                      class="page-link rounded-circle border-0 bg-dark text-white fw-bold"
                      href="#"
                      >1</a
                    >
                  </li>
                  <li class="page-item">
                    <a
                      class="page-link rounded-circle border-0 text-dark"
                      href="#"
                      >2</a
                    >
                  </li>
                  <li class="page-item">
                    <a
                      class="page-link rounded-circle border-0 text-dark"
                      href="#"
                      ><i class="bi bi-chevron-right"></i
                    ></a>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </main>

    <div
      class="modal fade"
      id="statusModal"
      tabindex="-1"
      aria-hidden="true"
      ref="statusModal"
    >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 rounded-4 shadow-2xl">
          <div class="modal-header border-bottom p-4">
            <h5 class="modal-title fw-bold tracking-tight">Update Status</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body p-4">
            <div v-if="selectedOrder">
              <div class="mb-3">
                <span class="text-muted extra-small text-uppercase fw-bold"
                  >Order ID</span
                >
                <p class="fw-bold font-monospace mb-0">
                  {{ selectedOrder.id }}
                </p>
              </div>

              <div class="mb-3">
                <label
                  class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted"
                  >New Status</label
                >
                <select
                  class="form-select bg-light border-0"
                  v-model="newStatus"
                >
                  <option>Pending</option>
                  <option>Processing</option>
                  <option>Shipped</option>
                  <option>Delivered</option>
                  <option>Cancelled</option>
                </select>
              </div>

              <div class="mb-4">
                <label
                  class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted"
                  >Notes / Tracking ID</label
                >
                <textarea
                  class="form-control bg-light border-0"
                  rows="3"
                  placeholder="Optional notes for customer..."
                ></textarea>
              </div>

              <div class="d-flex justify-content-end gap-2">
                <button
                  type="button"
                  class="btn btn-link text-muted text-decoration-none fw-bold small"
                  data-bs-dismiss="modal"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  class="btn btn-dark rounded-pill px-4 fw-bold text-uppercase extra-small"
                  @click="updateOrderStatus"
                >
                  Update
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      class="offcanvas offcanvas-end border-0 shadow-2xl"
      tabindex="-1"
      id="orderDetailsDrawer"
      ref="detailsDrawer"
      style="width: 400px"
    >
      <div class="offcanvas-header p-4 border-bottom">
        <div>
          <h5 class="offcanvas-title fw-bold tracking-tight">Order Details</h5>
          <span class="font-monospace text-muted small" v-if="selectedOrder">{{
            selectedOrder.id
          }}</span>
        </div>
        <button
          type="button"
          class="btn-close text-reset"
          data-bs-dismiss="offcanvas"
          aria-label="Close"
        ></button>
      </div>

      <div class="offcanvas-body p-0" v-if="selectedOrder">
        <div class="p-4 bg-light border-bottom">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="extra-small text-uppercase fw-bold text-muted"
              >Current Status</span
            >
            <span
              class="badge rounded-pill border px-2 py-1 extra-small fw-bold text-uppercase"
              :class="getStatusClass(selectedOrder.status)"
            >
              {{ selectedOrder.status }}
            </span>
          </div>
          <div class="progress" style="height: 4px">
            <div
              class="progress-bar bg-dark"
              role="progressbar"
              :style="{ width: getProgressWidth(selectedOrder.status) }"
            ></div>
          </div>
        </div>

        <div class="p-4 border-bottom">
          <h6
            class="fw-bold mb-3 small text-uppercase tracking-wide text-muted"
          >
            Customer
          </h6>
          <div class="d-flex align-items-center gap-3 mb-3">
            <div
              class="bg-light rounded-circle d-flex align-items-center justify-content-center fw-bold text-muted border"
              style="width: 48px; height: 48px"
            >
              {{ selectedOrder.initials }}
            </div>
            <div>
              <span class="d-block fw-bold text-dark">{{
                selectedOrder.customer
              }}</span>
              <span class="d-block small text-muted">{{
                selectedOrder.email
              }}</span>
            </div>
          </div>
          <div class="d-flex gap-2">
            <button
              class="btn btn-outline-dark btn-sm rounded-pill w-100 fw-bold extra-small text-uppercase"
            >
              <i class="bi bi-envelope me-1"></i> Email
            </button>
            <button
              class="btn btn-outline-dark btn-sm rounded-pill w-100 fw-bold extra-small text-uppercase"
            >
              <i class="bi bi-person me-1"></i> Profile
            </button>
          </div>
        </div>

        <div class="p-4 border-bottom">
          <h6
            class="fw-bold mb-3 small text-uppercase tracking-wide text-muted"
          >
            Ordered Items ({{ selectedOrder.itemsCount }})
          </h6>
          <div class="d-flex flex-column gap-3">
            <div
              class="d-flex gap-3 align-items-center"
              v-for="(item, index) in selectedOrder.items"
              :key="index"
            >
              <div
                class="ratio ratio-1x1 bg-light rounded border"
                style="width: 50px"
              >
                <img :src="item.image" class="object-fit-cover" />
              </div>
              <div class="flex-grow-1">
                <span class="d-block fw-bold small text-dark">{{
                  item.name
                }}</span>
                <span class="d-block extra-small text-muted"
                  >Qty: {{ item.quantity }}</span
                >
              </div>
              <span class="fw-bold small">${{ item.price }}</span>
            </div>
          </div>
        </div>

        <div class="p-4 bg-light-subtle h-100">
          <div class="d-flex justify-content-between mb-2 small">
            <span class="text-muted">Subtotal</span>
            <span>{{ selectedOrder.subtotal }}</span>
          </div>
          <div class="d-flex justify-content-between mb-2 small">
            <span class="text-muted">Shipping</span>
            <span>{{ selectedOrder.shipping }}</span>
          </div>
          <div class="d-flex justify-content-between mb-3 small">
            <span class="text-muted">Tax</span>
            <span>{{ selectedOrder.tax }}</span>
          </div>
          <div
            class="d-flex justify-content-between border-top border-dark-subtle pt-3"
          >
            <span class="fw-bold">Total</span>
            <span class="fw-bold">{{ selectedOrder.total }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";
// 1. IMPORT BOOTSTRAP CLASSES EXPLICITLY
import { Modal, Offcanvas } from 'bootstrap'; 

export default {
  name: "AdminOrders",
  data() {
    return {
      searchQuery: "",
      filterStatus: "All",
      selectedOrder: null,
      newStatus: "",
      statusModalInstance: null,
      detailsDrawerInstance: null,
      orders: [], // Will be populated by API
    };
  },
  computed: {
    filteredOrders() {
      // Safety check if orders is null
      if (!this.orders) return [];
      
      return this.orders.filter(o => {
        const matchesSearch = o.id.toLowerCase().includes(this.searchQuery.toLowerCase()) || 
                              o.customer.toLowerCase().includes(this.searchQuery.toLowerCase());
        const matchesStatus = this.filterStatus === "All" || o.status === this.filterStatus;
        return matchesSearch && matchesStatus;
      });
    }
  },
  mounted() {
    // 2. INITIALIZE BOOTSTRAP COMPONENTS SAFELY
    // We use the imported classes (Modal, Offcanvas) instead of window.bootstrap
    if (this.$refs.statusModal) {
      this.statusModalInstance = new Modal(this.$refs.statusModal);
    }
    if (this.$refs.detailsDrawer) {
      this.detailsDrawerInstance = new Offcanvas(this.$refs.detailsDrawer);
    }
    
    // 3. LOAD DATA
    this.fetchOrders();
  },
  methods: {
    async fetchOrders() {
      try {
        const response = await api.get("/admin/orders");
        this.orders = response.data.data;
      } catch (error) {
        console.error("Failed to load orders", error);
      }
    },

    async updateOrderStatus() {
      if (this.selectedOrder && this.selectedOrder.db_id) {
        try {
          await api.put(
            `/admin/orders/${this.selectedOrder.db_id}/status`,
            { status: this.newStatus }
          );

          // Update local UI immediately
          this.selectedOrder.status = this.newStatus;

          // Hide Modal
          this.statusModalInstance?.hide();
        } catch (error) {
          alert("Failed to update status");
          console.error(error);
        }
      }
    },

    openStatusModal(order) {
      this.selectedOrder = order;
      this.newStatus = order.status;
      this.statusModalInstance?.show();
    },
    
    openDetailsDrawer(order) {
      this.selectedOrder = order;
      this.detailsDrawerInstance?.show();
    },
    
    getStatusClass(status) {
      switch (status) {
        case "New": return "bg-primary-subtle text-primary border-primary-subtle";
        case "Pending": return "bg-secondary-subtle text-secondary border-secondary-subtle";
        case "Shipped": return "bg-info-subtle text-info-emphasis border-info-subtle";
        case "Processing": return "bg-warning-subtle text-warning-emphasis border-warning-subtle";
        case "Delivered": return "bg-success-subtle text-success border-success-subtle";
        case "Cancelled": return "bg-danger-subtle text-danger border-danger-subtle";
        default: return "bg-light text-dark";
      }
    },
    
    getProgressWidth(status) {
      switch (status) {
        case "New": return "10%";
        case "Processing": return "40%";
        case "Shipped": return "75%";
        case "Delivered": return "100%";
        default: return "0%";
      }
    },
  },
};
</script>

<style scoped>
/* ADMIN THEME STYLES */

/* Backgrounds */
.bg-light-subtle {
  background-color: #f9fafb !important;
}

/* Typography */
.tracking-wide {
  letter-spacing: 0.1em;
}
.tracking-tight {
  letter-spacing: -0.03em;
}
.extra-small {
  font-size: 0.75rem;
}

/* Form Controls */
.form-control:focus,
.form-select:focus {
  background-color: #fff;
  border: 1px solid #000 !important;
  box-shadow: none;
}

/* Animations */
.animate-fade-up {
  animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
  transform: translateY(20px);
}
.delay-100 {
  animation-delay: 0.1s;
}
.delay-200 {
  animation-delay: 0.2s;
}

@keyframes fadeUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Interactions */
.hover-lift {
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}
.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Table */
.table-hover tbody tr:hover {
  background-color: #f8f9fa;
}
.cursor-pointer {
  cursor: pointer;
}

/* Buttons */
.btn-white {
  background-color: #fff;
  color: #000;
  border-color: #dee2e6;
}
.btn-white:hover {
  border-color: #000;
}

/* Shadows */
.shadow-2xl {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

/* Hide Scrollbar */
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
