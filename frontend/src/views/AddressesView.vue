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
          <div class="text-center text-md-start">
            <h1 class="display-5 fw-bold tracking-tight mb-2">Saved Addresses</h1>
            <p class="text-muted lead fs-6 mb-0">Manage your delivery locations for faster checkout.</p>
          </div>
          
          <button class="btn btn-dark rounded-pill px-4 py-2 fw-bold text-uppercase extra-small tracking-wide hover-lift shadow-sm" @click="openModal()">
            <i class="bi bi-plus-lg me-2"></i> Add New Address
          </button>
        </div>

        <div v-if="addresses.length === 0" class="text-center py-6 animate-fade-up">
          <div class="bg-white d-inline-flex p-4 rounded-circle shadow-sm mb-4">
            <i class="bi bi-geo-alt display-4 text-muted opacity-25"></i>
          </div>
          <h3 class="fw-bold mb-3">No saved addresses yet</h3>
          <p class="text-muted mb-4">Add an address to speed up your checkout experience.</p>
          <button class="btn btn-outline-dark rounded-pill px-5 py-3 text-uppercase fw-bold tracking-wide hover-fill" @click="openModal()">
            Add Address
          </button>
        </div>

        <div v-else class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
          
          <div 
            class="col" 
            v-for="(addr, index) in addresses" 
            :key="addr.id"
          >
            <div 
              class="card h-100 border-0 shadow-sm rounded-4 p-4 animate-fade-up hover-border-dark transition-all"
              :style="{ animationDelay: `${index * 100}ms` }"
            >
              
              <div class="d-flex justify-content-between align-items-start mb-3">
                <span class="badge bg-light text-dark border fw-bold text-uppercase extra-small tracking-wide px-2 py-1">
                  {{ addr.label }}
                </span>
                <span v-if="addr.isDefault" class="badge bg-dark text-white fw-bold text-uppercase extra-small tracking-wide px-2 py-1">
                  Default
                </span>
                <div class="dropdown" v-if="!addr.isDefault">
                   <button class="btn btn-link text-muted p-0" type="button" data-bs-toggle="dropdown">
                     <i class="bi bi-three-dots"></i>
                   </button>
                   <ul class="dropdown-menu border-0 shadow-lg rounded-3 p-2">
                     <li><button class="dropdown-item rounded-2 small" @click="setAsDefault(addr.id)">Set as Default</button></li>
                     <li><button class="dropdown-item rounded-2 small text-danger" @click="deleteAddress(addr.id)">Delete</button></li>
                   </ul>
                </div>
              </div>

              <div class="mb-4">
                <h6 class="fw-bold mb-1">{{ addr.name }}</h6>
                <p class="text-muted small mb-3">{{ addr.phone }}</p>
                <address class="small text-muted lh-base mb-0 fst-normal">
                  {{ addr.line1 }}<br>
                  <span v-if="addr.line2">{{ addr.line2 }}<br></span>
                  {{ addr.city }}, {{ addr.state }} {{ addr.zip }}<br>
                  {{ addr.country }}
                </address>
              </div>

              <div class="mt-auto pt-3 border-top border-light-subtle d-flex gap-3">
                <button @click="openModal(addr)" class="btn btn-link text-decoration-none text-dark fw-bold text-uppercase extra-small p-0 hover-opacity-75">
                  Edit
                </button>
                <button @click="deleteAddress(addr.id)" class="btn btn-link text-decoration-none text-muted fw-bold text-uppercase extra-small p-0 hover-text-danger ms-auto">
                  Remove
                </button>
              </div>

            </div>
          </div>

        </div>

      </div>
    </main>

    <div class="modal fade" id="addressModal" tabindex="-1" aria-hidden="true" ref="addressModal">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content border-0 rounded-4 shadow-2xl overflow-hidden">
          
          <div class="modal-header border-bottom p-4">
            <h5 class="modal-title fw-bold tracking-tight">{{ isEditing ? 'Edit Address' : 'Add New Address' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          
          <div class="modal-body p-4 p-lg-5">
            <form @submit.prevent="saveAddress" class="row g-3">
              
              <div class="col-md-6">
                <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Full Name</label>
                <input type="text" class="form-control bg-light border-0 rounded-1" v-model="form.name" required>
              </div>
              <div class="col-md-6">
                <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Phone Number</label>
                <input type="tel" class="form-control bg-light border-0 rounded-1" v-model="form.phone" required>
              </div>

              <div class="col-12">
                <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Address Line 1</label>
                <input type="text" class="form-control bg-light border-0 rounded-1" v-model="form.line1" required placeholder="Street address, P.O. box, company name">
              </div>
              <div class="col-12">
                <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Address Line 2 (Optional)</label>
                <input type="text" class="form-control bg-light border-0 rounded-1" v-model="form.line2" placeholder="Apartment, suite, unit, building, floor">
              </div>

              <div class="col-md-5">
                <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">City</label>
                <input type="text" class="form-control bg-light border-0 rounded-1" v-model="form.city" required>
              </div>
              <div class="col-md-4">
                <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">State</label>
                <select class="form-select bg-light border-0 rounded-1" v-model="form.state" required>
                  <option value="" disabled>Select</option>
                  <option>CA</option>
                  <option>NY</option>
                  <option>TX</option>
                  </select>
              </div>
              <div class="col-md-3">
                <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Zip Code</label>
                <input type="text" class="form-control bg-light border-0 rounded-1" v-model="form.zip" required>
              </div>

              <div class="col-12">
                 <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Address Type</label>
                 <div class="d-flex gap-2">
                    <input type="radio" class="btn-check" name="addrType" id="typeHome" value="Home" v-model="form.label">
                    <label class="btn btn-outline-light text-dark border fw-bold text-uppercase extra-small rounded-pill px-4" for="typeHome">Home</label>

                    <input type="radio" class="btn-check" name="addrType" id="typeWork" value="Work" v-model="form.label">
                    <label class="btn btn-outline-light text-dark border fw-bold text-uppercase extra-small rounded-pill px-4" for="typeWork">Work</label>
                    
                    <input type="radio" class="btn-check" name="addrType" id="typeOther" value="Other" v-model="form.label">
                    <label class="btn btn-outline-light text-dark border fw-bold text-uppercase extra-small rounded-pill px-4" for="typeOther">Other</label>
                 </div>
              </div>

              <div class="col-12 mt-4 pt-3 border-top">
                <div class="d-flex justify-content-end gap-3">
                  <button type="button" class="btn btn-link text-muted text-decoration-none fw-bold text-uppercase extra-small" data-bs-dismiss="modal">Cancel</button>
                  <button type="submit" class="btn btn-dark rounded-pill px-5 fw-bold text-uppercase extra-small">Save Address</button>
                </div>
              </div>

            </form>
          </div>
        </div>
      </div>
    </div>

    <PremiumFooter @navigate="handleNavigation" />

  </div>
</template>

<script>
/* Global Bootstrap instance required for Modal control */
/* eslint-disable no-undef */

import PremiumNavbar from '@/components/Navbar.vue';
import PremiumFooter from '@/components/Footer.vue';

export default {
  name: "AddressesView",
  components: {
    PremiumNavbar,
    PremiumFooter
  },
  data() {
    return {
      isEditing: false,
      bsModal: null,
      form: {
        id: null,
        name: "",
        phone: "",
        line1: "",
        line2: "",
        city: "",
        state: "",
        zip: "",
        country: "United States",
        label: "Home"
      },
      addresses: [
        {
          id: 1,
          name: "Alex Morgan",
          phone: "+1 (555) 123-4567",
          line1: "123 Market Street",
          line2: "Suite 400",
          city: "San Francisco",
          state: "CA",
          zip: "94103",
          country: "United States",
          label: "Home",
          isDefault: true
        },
        {
          id: 2,
          name: "Alex Morgan (Office)",
          phone: "+1 (555) 987-6543",
          line1: "4500 Tech Plaza",
          line2: "Floor 12",
          city: "New York",
          state: "NY",
          zip: "10001",
          country: "United States",
          label: "Work",
          isDefault: false
        }
      ]
    };
  },
  mounted() {
    // Initialize Bootstrap Modal
    // Ensure bootstrap.js is loaded in index.html or main.js
    if (typeof bootstrap !== 'undefined') {
      this.bsModal = new bootstrap.Modal(this.$refs.addressModal);
    }
  },
  methods: {
    handleNavigation(page) {
      console.log(`Navigating to: ${page}`);
    },
    openModal(address = null) {
      if (address) {
        this.isEditing = true;
        this.form = { ...address };
      } else {
        this.isEditing = false;
        this.resetForm();
      }
      this.bsModal?.show();
    },
    resetForm() {
      this.form = {
        id: null,
        name: "",
        phone: "",
        line1: "",
        line2: "",
        city: "",
        state: "",
        zip: "",
        country: "United States",
        label: "Home"
      };
    },
    saveAddress() {
      if (this.isEditing) {
        const index = this.addresses.findIndex(a => a.id === this.form.id);
        if (index !== -1) this.addresses[index] = { ...this.form };
      } else {
        const newId = Math.max(...this.addresses.map(a => a.id), 0) + 1;
        this.addresses.push({ ...this.form, id: newId, isDefault: false });
      }
      this.bsModal?.hide();
    },
    deleteAddress(id) {
      if (confirm("Are you sure you want to delete this address?")) {
        this.addresses = this.addresses.filter(a => a.id !== id);
      }
    },
    setAsDefault(id) {
      this.addresses.forEach(a => a.isDefault = (a.id === id));
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

/* Cards */
.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}
.hover-border-dark:hover {
  border-color: #000 !important;
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.05) !important;
}

/* Modal Styling */
.shadow-2xl { box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); }
.modal-backdrop.show { opacity: 0.2; } /* Lighter backdrop for cleaner feel */

/* Form Elements */
.form-control:focus, .form-select:focus {
  background-color: #fff;
  border: 1px solid #000 !important;
  box-shadow: none;
}

/* Buttons */
.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.hover-fill {
  transition: all 0.2s ease;
}
.hover-fill:hover {
  background-color: #000;
  color: #fff;
  border-color: #000;
}

.hover-text-danger:hover {
  color: #dc3545 !important;
}

.hover-opacity-75:hover {
  opacity: 0.75;
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

/* Checkbox/Radio Buttons custom styling */
.btn-check:checked + .btn-outline-light {
    background-color: #000;
    color: #fff;
    border-color: #000;
}
</style>