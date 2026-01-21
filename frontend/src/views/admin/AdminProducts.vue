<template>
  <div class="d-flex flex-column min-vh-100 bg-light-subtle">
    <main class="flex-grow-1 py-5">
      <div class="container px-lg-5">
        
        <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-5 gap-3 animate-fade-up">
          <div>
            <h1 class="display-5 fw-bold tracking-tight mb-2">Manage Products</h1>
            <p class="text-muted lead fs-6 mb-0">View, edit, and organize your store inventory.</p>
          </div>
          
          <button class="btn btn-dark rounded-pill px-4 py-2 fw-bold text-uppercase extra-small tracking-wide hover-lift shadow-sm" @click="openProductModal()">
            <i class="bi bi-plus-lg me-2"></i> Add New Product
          </button>
        </div>

        <div class="card border-0 shadow-sm rounded-4 p-3 mb-4 animate-fade-up delay-100">
          <div class="row g-3 align-items-center">
            <div class="col-lg-5">
              <div class="position-relative">
                <i class="bi bi-search position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                <input type="text" class="form-control border-0 bg-light rounded-pill ps-5" 
                       placeholder="Search products..." v-model="filters.search" @input="debounceFetch">
              </div>
            </div>
            <div class="col-6 col-lg-3 ms-auto">
              <select class="form-select border-0 bg-light rounded-pill fs-6" v-model="filters.category" @change="fetchProducts">
                <option value="">All Categories</option>
                <option v-for="cat in categories" :key="cat.id" :value="cat.name">{{ cat.name }}</option>
              </select>
            </div>
            <div class="col-6 col-lg-2">
              <select class="form-select border-0 bg-light rounded-pill fs-6" v-model="filters.active" @change="fetchProducts">
                <option value="">All Status</option>
                <option value="true">Active</option>
                <option value="false">Disabled</option>
              </select>
            </div>
          </div>
        </div>

        <div v-if="error" class="alert alert-danger border-0 rounded-4 mb-4 shadow-sm d-flex justify-content-between align-items-center">
          <span><i class="bi bi-exclamation-triangle-fill me-2"></i> {{ error }}</span>
          <button class="btn-close" @click="error = null"></button>
        </div>

        <div class="card border-0 shadow-sm rounded-4 overflow-hidden animate-fade-up delay-200">
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-dark" role="status"></div>
            <p class="text-muted small mt-2">Loading inventory...</p>
          </div>

          <div v-else class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="bg-light">
                <tr>
                  <th class="ps-4 py-3 text-uppercase extra-small text-muted fw-bold border-0">Product</th>
                  <th class="py-3 text-uppercase extra-small text-muted fw-bold border-0">Category</th>
                  <th class="py-3 text-uppercase extra-small text-muted fw-bold border-0">Price</th> 
                  <th class="py-3 text-uppercase extra-small text-muted fw-bold border-0">Sale Price</th> 
                  
                  <th class="py-3 text-uppercase extra-small text-muted fw-bold border-0">Stock</th>
                  <th class="py-3 text-uppercase extra-small text-muted fw-bold border-0">Status</th>
                  <th class="pe-4 py-3 text-uppercase extra-small text-muted fw-bold border-0 text-end">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="product in products" :key="product.id">
                  <td class="ps-4 py-3">
                    <div class="d-flex align-items-center gap-3">
                      <div class="ratio ratio-1x1 rounded-3 overflow-hidden bg-light border" style="width: 48px;">
                        <img :src="product.image || 'https://via.placeholder.com/150'" class="object-fit-cover w-100 h-100" :alt="product.name">
                      </div>
                      <div>
                        <span class="d-block fw-bold text-dark small">{{ product.name }}</span>
                        <span class="d-block extra-small text-muted">SKU: {{ product.sku || product.id }}</span>
                      </div>
                    </div>
                  </td>
                  
                  <td class="py-3">
                    <span class="badge bg-light text-dark border fw-normal px-2 py-1 rounded-pill extra-small">
                      {{ product.category || 'Uncategorized' }}
                    </span>
                  </td>

                  <td class="py-3">
                    <span class="fw-medium small">${{ product.price }}</span>
                  </td>

                  <td class="py-3">
                    <span v-if="product.sale_price && product.sale_price > 0" class="fw-bold text-success small">
                      ${{ product.sale_price }}
                    </span>
                    <span v-else class="text-muted extra-small ps-3">-</span>
                  </td>

                  <td class="py-3 small">
                    <span :class="product.stock_quantity < 10 ? 'text-danger fw-bold' : 'text-muted'">
                      {{ product.stock_quantity }} units
                    </span>
                  </td>

                  <td class="py-3">
                    <div class="form-check form-switch">
                      <input class="form-check-input cursor-pointer" type="checkbox" :checked="product.is_active" @change="toggleStatus(product)">
                      <label class="form-check-label extra-small fw-bold text-uppercase ms-2" :class="product.is_active ? 'text-success' : 'text-muted'">
                        {{ product.is_active ? 'Active' : 'Disabled' }}
                      </label>
                    </div>
                  </td>

                  <td class="pe-4 py-3 text-end">
                    <div class="d-flex justify-content-end gap-2">
                      <button class="btn btn-sm btn-white border rounded-circle shadow-sm" title="Edit" @click="openProductModal(product)">
                        <i class="bi bi-pencil extra-small"></i>
                      </button>
                      <button class="btn btn-sm btn-white border rounded-circle shadow-sm hover-text-danger" title="Delete" @click="confirmDelete(product)">
                        <i class="bi bi-trash extra-small"></i>
                      </button>
                    </div>
                  </td>
                </tr>
                <tr v-if="products.length === 0">
                  <td colspan="7" class="text-center py-5">
                    <i class="bi bi-search text-muted fs-3 mb-2 d-block"></i>
                    <p class="text-muted small mb-0">No products found matching your criteria.</p>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div class="card-footer bg-white border-top p-3" v-if="pagination.total_pages > 1">
            <div class="d-flex justify-content-between align-items-center">
              <span class="text-muted extra-small">Showing {{ products.length }} products</span>
              <nav>
                <ul class="pagination pagination-sm mb-0 gap-1">
                  <li class="page-item" :class="{ disabled: pagination.page === 1 }">
                    <a class="page-link rounded-circle border-0 text-dark" href="#" @click.prevent="changePage(pagination.page - 1)">
                      <i class="bi bi-chevron-left"></i>
                    </a>
                  </li>
                  <li v-for="p in pagination.total_pages" :key="p" class="page-item" :class="{ active: pagination.page === p }">
                    <a class="page-link rounded-circle border-0" :class="pagination.page === p ? 'bg-dark text-white' : 'text-dark'" 
                       href="#" @click.prevent="changePage(p)">{{ p }}</a>
                  </li>
                  <li class="page-item" :class="{ disabled: pagination.page === pagination.total_pages }">
                    <a class="page-link rounded-circle border-0 text-dark" href="#" @click.prevent="changePage(pagination.page + 1)">
                      <i class="bi bi-chevron-right"></i>
                    </a>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </main>

    <div class="modal fade" id="productModal" tabindex="-1" ref="productModalRef">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content border-0 rounded-4 shadow-2xl">
          <div class="modal-header border-bottom p-4">
            <h5 class="modal-title fw-bold tracking-tight">{{ isEditing ? 'Edit Product' : 'Add Product' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="handleSave" class="row g-3">
              <div class="col-md-8">
                <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Product Name</label>
                <input type="text" class="form-control bg-light border-0" v-model="form.name" required>
              </div>
              <div class="col-md-4">
                <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Category</label>
                <select class="form-select bg-light border-0" v-model="form.category_id" required>
                  <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
                </select>
              </div>
              <div class="col-12">
                <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Description</label>
                <textarea class="form-control bg-light border-0" rows="3" v-model="form.description"></textarea>
              </div>
              
              <div class="col-md-4">
                <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Price ($)</label>
                <input type="number" step="0.01" class="form-control bg-light border-0" v-model="form.price" required>
              </div>
              <div class="col-md-4">
                <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Sale Price ($)</label>
                <input type="number" step="0.01" class="form-control bg-light border-0" v-model="form.sale_price" placeholder="Optional">
              </div>
              <div class="col-md-4">
                <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Stock Qty</label>
                <input type="number" class="form-control bg-light border-0" v-model="form.stock_quantity" required>
              </div>
              
              <div class="col-md-6">
                <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">SKU</label>
                <input type="text" class="form-control bg-light border-0" v-model="form.sku" placeholder="CODE-001">
              </div>
              <div class="col-md-6">
                <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Image URL</label>
                <input type="text" class="form-control bg-light border-0" v-model="form.image">
              </div>
              
              <div class="col-12 mt-4 text-end">
                <button type="button" class="btn btn-link text-muted text-decoration-none fw-bold small me-2" data-bs-dismiss="modal">Cancel</button>
                <button type="submit" class="btn btn-dark rounded-pill px-5 fw-bold text-uppercase extra-small" :disabled="submitting">
                  <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
                  {{ isEditing ? 'Save Changes' : 'Publish Product' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="deleteModal" tabindex="-1" ref="deleteModalRef">
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
              <button type="button" class="btn btn-danger rounded-pill px-4 fw-bold text-uppercase extra-small" @click="handleDelete" :disabled="submitting">
                <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from "@/services/api"; // Your Axios instance

const router = useRouter();

// --- State Management ---
const products = ref([]);
const categories = ref([]);
const loading = ref(false);
const submitting = ref(false);
const error = ref(null);
const isEditing = ref(false);
const deleteTarget = ref(null);

// Pagination & Filters
const pagination = reactive({ page: 1, total_pages: 1, limit: 10 });
const filters = reactive({ search: "", category: "", active: "" });

// Form Model (Exact match with Backend keys now)
const form = reactive({
  id: null,
  name: "",
  category_id: null,
  description: "",
  price: 0,
  sale_price: null,
  stock_quantity: 0, 
  sku: "",
  image: "",
  is_active: true
});

// --- Auth Guard ---
const checkAuth = () => {
  const token = localStorage.getItem('access_token');
  if (!token) { router.push('/login'); return false; }
  return true;
};

// --- API Methods ---
const fetchProducts = async () => {
  loading.value = true;
  error.value = null;
  try {
    const params = {
      search: filters.search || undefined,
      category: filters.category || undefined,
      active: filters.active || undefined,
      page: pagination.page,
      limit: pagination.limit
    };
    
    const response = await api.get('/admin/products', { params });
    
    // Direct assignment because API keys match perfectly
    products.value = response.data.data;
    pagination.total_pages = response.data.pages || 1;
  } catch (err) {
    error.value = "Failed to load inventory.";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const fetchCategories = async () => {
  try {
    // 1. Use your preferred working API
    const response = await api.get('/admin/categories/dropdown');
    
    // 2. Fix the Data Path
    // Axios gives 'response.data'. Your API puts the list inside a 'data' key.
    // So we need 'response.data.data' to get the array: [{id: 1, name: "Shoes"}]
    categories.value = response.data.data; 
    
  } catch (err) {
    console.error("Category Dropdown Error:", err);
  }
};

const changePage = (page) => {
  if (page < 1 || page > pagination.total_pages) return;
  pagination.page = page;
  fetchProducts();
};

const debounceFetch = (() => {
  let timeout;
  return () => { clearTimeout(timeout); timeout = setTimeout(fetchProducts, 500); };
})();

// --- CRUD Operations ---
const handleSave = async () => {
  submitting.value = true;
  try {
    // Send form directly (API handles keys correctly now)
    if (isEditing.value) {
      await api.put(`/admin/products/${form.id}`, form);
    } else {
      await api.post('/admin/products', form);
    }
    
    const modalEl = document.getElementById('productModal');
    const modal = bootstrap.Modal.getInstance(modalEl);
    modal.hide();
    
    fetchProducts();
  } catch (err) {
    console.error(err);
    error.value = "Could not save product. Check required fields.";
  } finally {
    submitting.value = false;
  }
};

const handleDelete = async () => {
  if (!deleteTarget.value) return;
  submitting.value = true;
  try {
    await api.delete(`/admin/products/${deleteTarget.value.id}`);
    
    const modalEl = document.getElementById('deleteModal');
    const modal = bootstrap.Modal.getInstance(modalEl);
    modal.hide();
    
    fetchProducts();
  } catch (err) {
    error.value = "Delete failed.";
  } finally {
    submitting.value = false;
    deleteTarget.value = null;
  }
};

const toggleStatus = async (product) => {
  const originalStatus = product.is_active;
  product.is_active = !product.is_active; 
  
  try {
    await api.put(`/admin/products/${product.id}`, { is_active: product.is_active });
  } catch (err) {
    product.is_active = originalStatus; 
    error.value = "Failed to update status.";
  }
};

// --- Modal Handlers ---
const openProductModal = (product = null) => {
  isEditing.value = !!product;
  if (product) {
    // Populate form directly from product object
    Object.assign(form, {
      id: product.id,
      name: product.name,
      category_id: product.category_id, 
      description: product.description,
      price: product.price,
      sale_price: product.sale_price,
      stock_quantity: product.stock_quantity,
      sku: product.sku,
      image: product.image,
      is_active: product.is_active
    });
  } else {
    resetForm();
  }
  const modalEl = document.getElementById('productModal');
  const modal = new bootstrap.Modal(modalEl);
  modal.show();
};

const confirmDelete = (product) => {
  deleteTarget.value = product;
  const modalEl = document.getElementById('deleteModal');
  const modal = new bootstrap.Modal(modalEl);
  modal.show();
};

const resetForm = () => {
  Object.assign(form, { 
    id: null, 
    name: "", 
    category_id: categories.value[0]?.id || null, 
    description: "",
    price: 0, 
    sale_price: null, 
    stock_quantity: 0, 
    is_active: true, 
    sku: "", 
    image: "" 
  });
};

onMounted(() => {
  if (checkAuth()) {
    fetchProducts();
    fetchCategories();
  }
});
</script>

<style scoped>
/* Keeping your existing styles */
.bg-light-subtle { background-color: #f9fafb !important; }
.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }

.form-control:focus, .form-select:focus {
  background-color: #fff;
  border: 1px solid #000 !important;
  box-shadow: none;
}

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

.hover-lift { transition: transform 0.2s ease, box-shadow 0.2s ease; }
.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.hover-text-danger:hover {
  color: #dc3545 !important;
  border-color: #dc3545 !important;
}

.cursor-pointer { cursor: pointer; }
.btn-white { background-color: #fff; color: #000; border-color: #dee2e6; }
.btn-white:hover { border-color: #000; }
.shadow-2xl { box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); }
</style>