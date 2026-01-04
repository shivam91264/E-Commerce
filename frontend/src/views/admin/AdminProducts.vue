<template>
  <div class="d-flex flex-column min-vh-100 bg-light-subtle">
    
    <AdminNavbar />

    <main class="flex-grow-1 py-5">
      <div class="container px-lg-5">
        
        <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-5 gap-3 animate-fade-up">
          <div>
            <h1 class="display-5 fw-bold tracking-tight mb-2">Manage Products</h1>
            <p class="text-muted lead fs-6 mb-0">View, edit, and organize your store inventory.</p>
          </div>
          
          <button class="btn btn-dark rounded-pill px-4 py-2 fw-bold text-uppercase extra-small tracking-wide hover-lift shadow-sm" @click="openModal()">
            <i class="bi bi-plus-lg me-2"></i> Add New Product
          </button>
        </div>

        <div class="card border-0 shadow-sm rounded-4 p-3 mb-4 animate-fade-up delay-100">
          <div class="row g-3 align-items-center">
            <div class="col-lg-5">
              <div class="position-relative">
                <i class="bi bi-search position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                <input type="text" class="form-control border-0 bg-light rounded-pill ps-5" placeholder="Search products..." v-model="searchQuery">
              </div>
            </div>
            <div class="col-6 col-lg-3 ms-auto">
              <select class="form-select border-0 bg-light rounded-pill fs-6" v-model="filterCategory">
                <option value="All">All Categories</option>
                <option>Furniture</option>
                <option>Lighting</option>
                <option>Decor</option>
                <option>Electronics</option>
              </select>
            </div>
            <div class="col-6 col-lg-2">
              <select class="form-select border-0 bg-light rounded-pill fs-6" v-model="filterStatus">
                <option value="All">All Status</option>
                <option value="Active">Active</option>
                <option value="Disabled">Disabled</option>
              </select>
            </div>
          </div>
        </div>

        <div class="card border-0 shadow-sm rounded-4 overflow-hidden animate-fade-up delay-200">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="bg-light">
                <tr>
                  <th class="ps-4 py-3 text-uppercase extra-small text-muted fw-bold border-0">Product</th>
                  <th class="py-3 text-uppercase extra-small text-muted fw-bold border-0">Category</th>
                  <th class="py-3 text-uppercase extra-small text-muted fw-bold border-0">Price</th>
                  <th class="py-3 text-uppercase extra-small text-muted fw-bold border-0">Stock</th>
                  <th class="py-3 text-uppercase extra-small text-muted fw-bold border-0">Status</th>
                  <th class="pe-4 py-3 text-uppercase extra-small text-muted fw-bold border-0 text-end">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="product in filteredProducts" :key="product.id">
                  <td class="ps-4 py-3">
                    <div class="d-flex align-items-center gap-3">
                      <div class="ratio ratio-1x1 rounded-3 overflow-hidden bg-light border" style="width: 48px;">
                        <img :src="product.image" class="object-fit-cover w-100 h-100" :alt="product.name">
                      </div>
                      <div>
                        <span class="d-block fw-bold text-dark small">{{ product.name }}</span>
                        <span class="d-block extra-small text-muted">ID: {{ product.id }}</span>
                      </div>
                    </div>
                  </td>
                  
                  <td class="py-3">
                    <span class="badge bg-light text-dark border fw-normal px-2 py-1 rounded-pill extra-small">
                      {{ product.category }}
                    </span>
                  </td>

                  <td class="py-3 fw-medium small">${{ product.price }}</td>

                  <td class="py-3 small">
                    <span :class="product.stock < 10 ? 'text-danger fw-bold' : 'text-muted'">
                      {{ product.stock }} units
                    </span>
                  </td>

                  <td class="py-3">
                    <div class="form-check form-switch">
                      <input class="form-check-input cursor-pointer" type="checkbox" :checked="product.active" @change="toggleStatus(product)">
                      <label class="form-check-label extra-small fw-bold text-uppercase ms-2" :class="product.active ? 'text-success' : 'text-muted'">
                        {{ product.active ? 'Active' : 'Disabled' }}
                      </label>
                    </div>
                  </td>

                  <td class="pe-4 py-3 text-end">
                    <div class="d-flex justify-content-end gap-2">
                      <button class="btn btn-sm btn-white border rounded-circle shadow-sm" title="Edit" @click="openModal(product)">
                        <i class="bi bi-pencil extra-small"></i>
                      </button>
                      <button class="btn btn-sm btn-white border rounded-circle shadow-sm hover-text-danger" title="Delete" @click="confirmDelete(product)">
                        <i class="bi bi-trash extra-small"></i>
                      </button>
                    </div>
                  </td>
                </tr>
                
                <tr v-if="filteredProducts.length === 0">
                  <td colspan="6" class="text-center py-5">
                    <i class="bi bi-search text-muted fs-3 mb-2 d-block"></i>
                    <p class="text-muted small mb-0">No products found matching your criteria.</p>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div class="card-footer bg-white border-top p-3">
            <div class="d-flex justify-content-between align-items-center">
              <span class="text-muted extra-small">Showing {{ filteredProducts.length }} products</span>
              <nav>
                <ul class="pagination pagination-sm mb-0 gap-1">
                  <li class="page-item disabled"><a class="page-link rounded-circle border-0 text-dark" href="#"><i class="bi bi-chevron-left"></i></a></li>
                  <li class="page-item active"><a class="page-link rounded-circle border-0 bg-dark text-white fw-bold" href="#">1</a></li>
                  <li class="page-item"><a class="page-link rounded-circle border-0 text-dark" href="#">2</a></li>
                  <li class="page-item"><a class="page-link rounded-circle border-0 text-dark" href="#"><i class="bi bi-chevron-right"></i></a></li>
                </ul>
              </nav>
            </div>
          </div>
        </div>

      </div>
    </main>

    <AdminFooter />

    <div class="modal fade" id="productModal" tabindex="-1" aria-hidden="true" ref="productModal">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content border-0 rounded-4 shadow-2xl">
          <div class="modal-header border-bottom p-4">
            <h5 class="modal-title fw-bold tracking-tight">{{ isEditing ? 'Edit Product' : 'Add Product' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="saveProduct" class="row g-3">
              <div class="col-md-8">
                <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Product Name</label>
                <input type="text" class="form-control bg-light border-0" v-model="form.name" required>
              </div>
              <div class="col-md-4">
                <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Category</label>
                <select class="form-select bg-light border-0" v-model="form.category">
                  <option>Furniture</option>
                  <option>Lighting</option>
                  <option>Decor</option>
                  <option>Electronics</option>
                </select>
              </div>
              <div class="col-12">
                <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Description</label>
                <textarea class="form-control bg-light border-0" rows="3" v-model="form.description"></textarea>
              </div>
              <div class="col-md-4">
                <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Price ($)</label>
                <input type="number" class="form-control bg-light border-0" v-model="form.price" required>
              </div>
              <div class="col-md-4">
                <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Discount Price</label>
                <input type="number" class="form-control bg-light border-0" v-model="form.salePrice">
              </div>
              <div class="col-md-4">
                <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Stock Qty</label>
                <input type="number" class="form-control bg-light border-0" v-model="form.stock" required>
              </div>
              <div class="col-12">
                <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Image URL (Mock)</label>
                <input type="text" class="form-control bg-light border-0" v-model="form.image" placeholder="https://...">
              </div>
              
              <div class="col-12 mt-4 text-end">
                <button type="button" class="btn btn-link text-muted text-decoration-none fw-bold small me-2" data-bs-dismiss="modal">Cancel</button>
                <button type="submit" class="btn btn-dark rounded-pill px-5 fw-bold text-uppercase extra-small">
                  {{ isEditing ? 'Save Changes' : 'Publish Product' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="deleteModal" tabindex="-1" aria-hidden="true" ref="deleteModal">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 rounded-4 shadow-2xl p-3">
          <div class="modal-body text-center">
            <div class="mb-3 d-inline-flex align-items-center justify-content-center bg-danger bg-opacity-10 rounded-circle text-danger" style="width: 60px; height: 60px;">
              <i class="bi bi-exclamation-triangle fs-3"></i>
            </div>
            <h5 class="fw-bold mb-2">Delete Product?</h5>
            <p class="text-muted small mb-4">Are you sure you want to remove <strong>{{ deleteTarget?.name }}</strong>? This action cannot be undone.</p>
            <div class="d-flex justify-content-center gap-2">
              <button type="button" class="btn btn-light border rounded-pill px-4 fw-bold text-uppercase extra-small" data-bs-dismiss="modal">Cancel</button>
              <button type="button" class="btn btn-danger rounded-pill px-4 fw-bold text-uppercase extra-small" @click="executeDelete">Delete</button>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
/* Global bootstrap variable expected from CDN or main.js */
/* eslint-disable no-undef */
import AdminNavbar from '@/components/Admin/AdminNavbar.vue';
import AdminFooter from '@/components/Admin/AdminFooter.vue';


export default {
  name: "AdminProducts",
  components: {
    AdminNavbar,
    AdminFooter
  },
  data() {
    return {
      searchQuery: "",
      filterCategory: "All",
      filterStatus: "All",
      isEditing: false,
      productModalInstance: null,
      deleteModalInstance: null,
      deleteTarget: null,
      
      // Form Model
      form: {
        id: null,
        name: "",
        category: "Furniture",
        price: 0,
        salePrice: null,
        stock: 0,
        description: "",
        image: "",
        active: true
      },

      // Mock Data
      products: [
        { id: 101, name: "Linen Lounge Chair", category: "Furniture", price: 299, stock: 12, active: true, image: "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?auto=format&fit=crop&w=100&q=80" },
        { id: 102, name: "Ceramic Vase Set", category: "Decor", price: 89, stock: 45, active: true, image: "https://images.unsplash.com/photo-1612196808214-b7e239e5f6b7?auto=format&fit=crop&w=100&q=80" },
        { id: 103, name: "Minimal Desk Lamp", category: "Lighting", price: 120, stock: 8, active: true, image: "https://images.unsplash.com/photo-1507473888900-52e1ad145986?auto=format&fit=crop&w=100&q=80" },
        { id: 104, name: "Wireless Headphones", category: "Electronics", price: 299, stock: 0, active: false, image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=100&q=80" },
      ]
    };
  },
  computed: {
    filteredProducts() {
      return this.products.filter(p => {
        const matchesSearch = p.name.toLowerCase().includes(this.searchQuery.toLowerCase());
        const matchesCat = this.filterCategory === "All" || p.category === this.filterCategory;
        const matchesStatus = this.filterStatus === "All" || 
                              (this.filterStatus === "Active" && p.active) || 
                              (this.filterStatus === "Disabled" && !p.active);
        return matchesSearch && matchesCat && matchesStatus;
      });
    }
  },
  mounted() {
    if (typeof bootstrap !== 'undefined') {
      this.productModalInstance = new bootstrap.Modal(this.$refs.productModal);
      this.deleteModalInstance = new bootstrap.Modal(this.$refs.deleteModal);
    }
  },
  methods: {
    openModal(product = null) {
      if (product) {
        this.isEditing = true;
        this.form = { ...product };
      } else {
        this.isEditing = false;
        this.resetForm();
      }
      this.productModalInstance?.show();
    },
    resetForm() {
      this.form = { id: null, name: "", category: "Furniture", price: 0, stock: 0, active: true, image: "https://via.placeholder.com/150" };
    },
    saveProduct() {
      if (this.isEditing) {
        const index = this.products.findIndex(p => p.id === this.form.id);
        if (index !== -1) this.products[index] = { ...this.form };
      } else {
        const newId = Math.max(...this.products.map(p => p.id), 100) + 1;
        this.products.push({ ...this.form, id: newId });
      }
      this.productModalInstance?.hide();
    },
    toggleStatus(product) {
      product.active = !product.active;
    },
    confirmDelete(product) {
      this.deleteTarget = product;
      this.deleteModalInstance?.show();
    },
    executeDelete() {
      this.products = this.products.filter(p => p.id !== this.deleteTarget.id);
      this.deleteModalInstance?.hide();
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

/* Form Controls */
.form-control:focus, .form-select:focus {
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
.delay-100 { animation-delay: 0.1s; }
.delay-200 { animation-delay: 0.2s; }

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

.hover-text-danger:hover {
  color: #dc3545 !important;
  border-color: #dc3545 !important;
}

.cursor-pointer { cursor: pointer; }

/* Table specific styling */
.table-hover tbody tr:hover { background-color: #f8f9fa; }

.btn-white {
  background-color: #fff;
  color: #000;
  border-color: #dee2e6;
}
.btn-white:hover { border-color: #000; }

/* Modal Shadow */
.shadow-2xl { box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); }
</style>