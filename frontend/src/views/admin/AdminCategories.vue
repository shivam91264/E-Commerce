<template>
  <div class="d-flex flex-column min-vh-100 bg-light-subtle">
    <main class="flex-grow-1 py-5">
      <div class="container px-lg-5">
        
        <div v-if="loading" class="d-flex flex-column align-items-center justify-content-center py-5 my-5 animate-fade-up">
          <div class="spinner-border text-dark mb-3" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <p class="text-muted">Fetching categories...</p>
        </div>

        <div v-else-if="error" class="alert alert-danger border-0 shadow-sm rounded-4 p-4 animate-fade-up" role="alert">
          <div class="d-flex align-items-center gap-3">
            <i class="bi bi-exclamation-octagon-fill fs-3"></i>
            <div>
              <h5 class="alert-heading fw-bold mb-1">System Error</h5>
              <p class="mb-0">{{ error }}</p>
              <button @click="fetchCategories" class="btn btn-danger btn-sm mt-3 px-4 rounded-pill fw-bold text-uppercase extra-small">
                Try Again
              </button>
            </div>
          </div>
        </div>

        <div v-else>
          <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-5 gap-3 animate-fade-up">
            <div>
              <h1 class="display-5 fw-bold tracking-tight mb-2">Manage Categories</h1>
              <p class="text-muted lead fs-6 mb-0">Create, edit, and organize product categories.</p>
            </div>
            
            <button @click="openAddModal" class="btn btn-dark px-4 py-2 rounded-pill fw-bold shadow-sm hover-scale transition-all">
              <i class="bi bi-plus-lg me-2"></i> ADD CATEGORY
            </button>
          </div>

          <div class="card border-0 shadow-sm rounded-4 p-3 mb-4 animate-fade-up delay-100">
            <div class="row g-3">
              <div class="col-12 col-md-6">
                <div class="input-group">
                  <span class="input-group-text bg-white border-end-0 rounded-start-pill ps-3">
                    <i class="bi bi-search text-muted"></i>
                  </span>
                  <input 
                    type="text" 
                    class="form-control border-start-0 rounded-end-pill ps-0" 
                    placeholder="Search categories..." 
                    v-model="searchQuery"
                  >
                </div>
              </div>
            </div>
          </div>

          <div class="card border-0 shadow-sm rounded-4 overflow-hidden animate-fade-up delay-200">
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                <thead class="bg-light">
                  <tr>
                    <th class="ps-4 py-3 text-uppercase extra-small text-muted fw-bold border-0">ID</th>
                    <th class="py-3 text-uppercase extra-small text-muted fw-bold border-0">Category Name</th>
                    <th class="py-3 text-uppercase extra-small text-muted fw-bold border-0 d-none d-md-table-cell">Slug</th>
                    <th class="py-3 text-uppercase extra-small text-muted fw-bold border-0 d-none d-lg-table-cell">Description</th>
                    <th class="py-3 text-uppercase extra-small text-muted fw-bold border-0 d-none d-lg-table-cell">Parent</th>
                    <th class="pe-4 py-3 text-uppercase extra-small text-muted fw-bold border-0 text-end">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="filteredCategories.length === 0">
                    <td colspan="6" class="text-center py-5 text-muted small">
                      <div class="d-flex flex-column align-items-center">
                        <i class="bi bi-folder-x fs-1 mb-2 text-muted opacity-50"></i>
                        No categories found.
                      </div>
                    </td>
                  </tr>
                  
                  <tr v-for="cat in filteredCategories" :key="cat.id" class="cursor-pointer">
                    <td class="ps-4 py-3 fw-bold small font-monospace">#{{ cat.id }}</td>
                    
                    <td class="py-3">
                      <div class="d-flex align-items-center gap-3">
                        <div class="bg-light rounded-3 d-flex align-items-center justify-content-center overflow-hidden border" style="width: 40px; height: 40px;">
                          <img v-if="cat.image_url" :src="cat.image_url" alt="" class="w-100 h-100 object-fit-cover">
                          <i v-else class="bi bi-image text-muted opacity-50"></i>
                        </div>
                        <span class="fw-bold text-dark">{{ cat.name }}</span>
                      </div>
                    </td>

                    <td class="py-3 d-none d-md-table-cell">
                      <span class="badge bg-light text-dark border px-2 py-1 extra-small font-monospace">
                        /{{ cat.slug }}
                      </span>
                    </td>

                    <td class="py-3 d-none d-lg-table-cell text-muted small text-truncate" style="max-width: 200px;">
                      {{ cat.description || '-' }}
                    </td>

                    <td class="py-3 d-none d-lg-table-cell small text-muted">
                      <span v-if="cat.parent_id" class="badge bg-secondary-subtle text-secondary rounded-pill">
                        <i class="bi bi-arrow-return-right me-1"></i> {{ getParentName(cat.parent_id) }}
                      </span>
                      <span v-else class="text-muted opacity-50">-</span>
                    </td>

                    <td class="pe-4 py-3 text-end">
                      <div class="d-flex justify-content-end gap-2">
                        <button @click.stop="openEditModal(cat)" class="btn btn-white btn-sm border rounded-circle shadow-sm hover-scale" style="width: 32px; height: 32px;">
                          <i class="bi bi-pencil-fill extra-small text-muted"></i>
                        </button>
                        <button @click.stop="confirmDelete(cat)" class="btn btn-white btn-sm border rounded-circle shadow-sm hover-scale" style="width: 32px; height: 32px;">
                          <i class="bi bi-trash-fill extra-small text-danger"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </main>

    <div class="modal fade" id="categoryModal" tabindex="-1" aria-hidden="true" ref="categoryModalRef">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 shadow rounded-4">
          <div class="modal-header border-bottom-0 p-4 pb-0">
            <h5 class="modal-title fw-bold">{{ isEditing ? 'Edit Category' : 'New Category' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="saveCategory">
              <div class="mb-3">
                <label class="form-label extra-small fw-bold text-uppercase text-muted">Name</label>
                <input type="text" class="form-control bg-light border-0" v-model="form.name" required>
              </div>
              
              <div class="mb-3">
                <label class="form-label extra-small fw-bold text-uppercase text-muted">Description</label>
                <textarea class="form-control bg-light border-0" v-model="form.description" rows="2"></textarea>
              </div>

              <div class="row g-3 mb-4">
                <div class="col-md-6">
                  <label class="form-label extra-small fw-bold text-uppercase text-muted">Parent Category</label>
                  <select class="form-select bg-light border-0" v-model="form.parent_id">
                    <option :value="null">None (Root)</option>
                    <option v-for="p in dropdownOptions" :key="p.id" :value="p.id" :disabled="p.id === form.id">
                      {{ p.name }}
                    </option>
                  </select>
                </div>
                <div class="col-md-6">
                  <label class="form-label extra-small fw-bold text-uppercase text-muted">Image URL</label>
                  <input type="text" class="form-control bg-light border-0" v-model="form.image_url" placeholder="http://...">
                </div>
              </div>

              <div class="d-grid">
                <button type="submit" class="btn btn-dark py-2 rounded-pill fw-bold">
                  {{ isEditing ? 'Update Category' : 'Create Category' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { Modal } from 'bootstrap';
import api from "@/services/api"; 

const categories = ref([]);
const dropdownOptions = ref([]);
const searchQuery = ref("");
const loading = ref(true);
const error = ref(null);
const isEditing = ref(false);
const categoryModalRef = ref(null);
let modalInstance = null;

// Form State
const form = ref({
  id: null,
  name: "",
  description: "",
  image_url: "",
  parent_id: null
});

// Computed Search Logic
const filteredCategories = computed(() => {
  if (!searchQuery.value) return categories.value;
  const lower = searchQuery.value.toLowerCase();
  return categories.value.filter(cat => 
    cat.name.toLowerCase().includes(lower) || 
    cat.slug.toLowerCase().includes(lower)
  );
});

// --- API ACTIONS ---

const fetchCategories = async () => {
  loading.value = true;
  error.value = null;
  try {
    const res = await api.get('/admin/categories');
    // Your API returns { data: [...] }, Axios adds its own .data
    categories.value = res.data.data; 
    
    // Also refresh dropdown options whenever we fetch the list
    fetchDropdown();
  } catch (err) {
    console.error(err);
    error.value = "Failed to load categories.";
  } finally {
    loading.value = false;
  }
};

const fetchDropdown = async () => {
  try {
    const res = await api.get('/admin/categories/dropdown');
    dropdownOptions.value = res.data.data;
  } catch (err) {
    console.error("Error fetching dropdown options", err);
  }
};

const saveCategory = async () => {
  try {
    const url = isEditing.value 
      ? `/admin/categories/${form.value.id}`
      : `/admin/categories`;
    const method = isEditing.value ? 'put' : 'post';
    
    await api[method](url, form.value);
    
    // Success
    await fetchCategories();
    modalInstance.hide();
    alert(isEditing.value ? "Category updated!" : "Category created!");
  } catch (err) {
    alert(err.response?.data?.msg || "Operation failed");
  }
};

const confirmDelete = async (cat) => {
  if (confirm(`Are you sure you want to delete "${cat.name}"?`)) {
    try {
      await api.delete(`/admin/categories/${cat.id}`);
      fetchCategories(); 
    } catch (err) {
      // Your API returns 400 if products exist, we catch that msg here
      alert(err.response?.data?.msg || "Failed to delete category.");
    }
  }
};

// --- HELPERS ---

// Helper to show Parent Name in table instead of ID
const getParentName = (parentId) => {
  const parent = dropdownOptions.value.find(p => p.id === parentId);
  return parent ? parent.name : `ID: ${parentId}`;
};

const resetForm = () => {
  form.value = { id: null, name: "", description: "", image_url: "", parent_id: null };
};

const openAddModal = () => {
  isEditing.value = false;
  resetForm();
  modalInstance.show();
};

const openEditModal = (cat) => {
  isEditing.value = true;
  // Clone to avoid reactive issues
  form.value = { 
    id: cat.id,
    name: cat.name,
    description: cat.description,
    image_url: cat.image_url,
    parent_id: cat.parent_id
  }; 
  modalInstance.show();
};

// --- LIFECYCLE ---

onMounted(() => {
  // Initialize Bootstrap Modal
  if (categoryModalRef.value) {
    modalInstance = new Modal(categoryModalRef.value);
  }
  fetchCategories();
});
</script>

<style scoped>
/* Matching styles from previous admin pages */
.bg-light-subtle { background-color: #f9fafb !important; }
.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }
.object-fit-cover { object-fit: cover; }
.transition-all { transition: all 0.2s ease; }

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
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.05) !important;
}

.hover-scale:hover { transform: scale(1.05); }
.table-hover tbody tr:hover { background-color: #f8f9fa; }
.cursor-pointer { cursor: pointer; }
.btn-white { background: #fff; color: #000; border-color: #dee2e6; }
.btn-white:hover { border-color: #000; background-color: #f8f9fa; }
.form-control:focus, .form-select:focus {
  box-shadow: none;
  border-color: #dee2e6;
}
</style>