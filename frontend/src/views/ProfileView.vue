<template>
  <div class="d-flex flex-column min-vh-100 bg-light-subtle">
    
    <main class="flex-grow-1 py-5">
      <div class="container px-lg-5">
        
        <div class="mb-5 text-center text-lg-start animate-fade-up">
          <h1 class="display-5 fw-bold tracking-tight mb-2">My Account</h1>
          <p class="text-muted lead fs-6 mb-0">Manage your personal details and preferences.</p>
        </div>

        <div class="row g-4 g-lg-5">
          
          <div class="col-lg-4 col-xl-3 animate-fade-up delay-100">
            
            <div class="d-flex align-items-center gap-3 mb-4 d-lg-none" v-if="user">
              <div class="bg-dark text-white rounded-circle d-flex align-items-center justify-content-center fw-bold fs-4" style="width: 60px; height: 60px;">
                {{ userInitials }}
              </div>
              <div>
                <h6 class="fw-bold mb-0">{{ user.name }}</h6>
                <span class="text-muted small">{{ user.email }}</span>
              </div>
            </div>

            <div class="card border-0 shadow-sm rounded-4 overflow-hidden sticky-lg-top" style="top: 100px; z-index: 1;">
              <div class="list-group list-group-flush p-2">
                
                <a href="#" 
                   class="list-group-item list-group-item-action border-0 rounded-3 d-flex align-items-center gap-3 py-3 px-3 mb-1 transition-all"
                   :class="activeTab === 'profile' ? 'bg-dark text-white fw-bold' : 'text-muted hover-bg-light'"
                   @click.prevent="activeTab = 'profile'"
                >
                  <i class="bi bi-person fs-5"></i>
                  <span class="small text-uppercase tracking-wide">Profile Details</span>
                </a>

                <a href="#" 
                   class="list-group-item list-group-item-action border-0 rounded-3 d-flex align-items-center gap-3 py-3 px-3 mb-1 transition-all"
                   :class="activeTab === 'orders' ? 'bg-dark text-white fw-bold' : 'text-muted hover-bg-light'"
                   @click.prevent="handleNavigation('orders')"
                >
                  <i class="bi bi-box-seam fs-5"></i>
                  <span class="small text-uppercase tracking-wide">Order History</span>
                </a>

                <a href="#" 
                   class="list-group-item list-group-item-action border-0 rounded-3 d-flex align-items-center gap-3 py-3 px-3 mb-1 transition-all"
                   :class="activeTab === 'wishlist' ? 'bg-dark text-white fw-bold' : 'text-muted hover-bg-light'"
                   @click.prevent="handleNavigation('wishlist')"
                >
                  <i class="bi bi-heart fs-5"></i>
                  <span class="small text-uppercase tracking-wide">Wishlist</span>
                </a>

                <a href="#" 
                   class="list-group-item list-group-item-action border-0 rounded-3 d-flex align-items-center gap-3 py-3 px-3 mb-1 transition-all"
                   :class="activeTab === 'addresses' ? 'bg-dark text-white fw-bold' : 'text-muted hover-bg-light'"
                   @click.prevent="handleNavigation('addresses')"
                >
                  <i class="bi bi-geo-alt fs-5"></i>
                  <span class="small text-uppercase tracking-wide">Saved Addresses</span>
                </a>

                <div class="my-2 border-top"></div>

                <a href="#" class="list-group-item list-group-item-action border-0 rounded-3 d-flex align-items-center gap-3 py-3 px-3 text-danger hover-bg-danger-subtle transition-all" @click.prevent="logout">
                  <i class="bi bi-box-arrow-right fs-5"></i>
                  <span class="small text-uppercase tracking-wide fw-bold">Log Out</span>
                </a>

              </div>
            </div>
          </div>

          <div class="col-lg-8 col-xl-9 animate-fade-up delay-200">
            
            <div v-if="loading" class="text-center py-5">
               <div class="spinner-border text-dark" role="status"></div>
            </div>

            <div v-else class="card border-0 shadow-sm rounded-4 p-4 p-lg-5 mb-4">
              
              <div class="d-flex justify-content-between align-items-center mb-4 pb-3 border-bottom border-light">
                <h5 class="fw-bold mb-0">Profile Information</h5>
                <button v-if="!isEditing" @click="toggleEdit" class="btn btn-outline-dark rounded-pill px-4 btn-sm fw-bold tracking-wide text-uppercase hover-lift">
                  Edit Details
                </button>
              </div>

              <div v-if="!isEditing" class="row g-4">
                <div class="col-md-6">
                  <span class="d-block text-muted extra-small text-uppercase tracking-wide fw-bold mb-1">Full Name</span>
                  <p class="mb-0 fw-medium">{{ user.name || 'Not set' }}</p>
                </div>
                <div class="col-md-6">
                  <span class="d-block text-muted extra-small text-uppercase tracking-wide fw-bold mb-1">Email Address</span>
                  <p class="mb-0 fw-medium">{{ user.email }}</p>
                </div>
                <div class="col-md-6">
                  <span class="d-block text-muted extra-small text-uppercase tracking-wide fw-bold mb-1">Phone Number</span>
                  <p class="mb-0 fw-medium">{{ user.phone || 'Not set' }}</p>
                </div>
                <div class="col-md-6">
                  <span class="d-block text-muted extra-small text-uppercase tracking-wide fw-bold mb-1">Gender</span>
                  <p class="mb-0 fw-medium">{{ user.gender || 'Not specified' }}</p>
                </div>
                 <div class="col-md-6">
                  <span class="d-block text-muted extra-small text-uppercase tracking-wide fw-bold mb-1">Date of Birth</span>
                  <p class="mb-0 fw-medium">{{ user.dob || 'Not set' }}</p>
                </div>
              </div>

              <form v-else @submit.prevent="saveChanges">
                <div class="row g-4">
                  <div class="col-md-6">
                    <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Full Name</label>
                    <input type="text" class="form-control bg-light border-0 rounded-1" v-model="editForm.name">
                  </div>
                  <div class="col-md-6">
                    <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Email Address</label>
                    <input type="email" class="form-control bg-light border-0 rounded-1 text-muted" v-model="editForm.email" disabled title="Email cannot be changed">
                  </div>
                  <div class="col-md-6">
                    <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Phone Number</label>
                    <input type="tel" class="form-control bg-light border-0 rounded-1" v-model="editForm.phone">
                  </div>
                  <div class="col-md-6">
                    <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Gender</label>
                    <select class="form-select bg-light border-0 rounded-1" v-model="editForm.gender">
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                      <option value="Non-binary">Non-binary</option>
                      <option value="Prefer not to say">Prefer not to say</option>
                    </select>
                  </div>
                  <div class="col-md-6">
                    <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Date of Birth</label>
                    <input type="date" class="form-control bg-light border-0 rounded-1" v-model="editForm.dob">
                  </div>
                </div>

                <div class="d-flex gap-3 mt-4 pt-3 border-top border-light">
                  <button type="submit" class="btn btn-dark rounded-pill px-4 btn-sm fw-bold tracking-wide text-uppercase hover-lift" :disabled="saving">
                    <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
                    Save Changes
                  </button>
                  <button type="button" @click="cancelEdit" class="btn btn-link text-muted text-decoration-none btn-sm fw-bold tracking-wide text-uppercase" :disabled="saving">
                    Cancel
                  </button>
                </div>
              </form>

            </div>

            <div class="card border-0 shadow-sm rounded-4 p-4 p-lg-5">
              <div class="mb-4 border-bottom border-light pb-3">
                <h5 class="fw-bold mb-0">Account Security</h5>
              </div>

              <div class="d-flex align-items-center justify-content-between mb-4">
                <div>
                  <h6 class="fw-bold mb-1 fs-6">Password</h6>
                  <p class="text-muted small mb-0">Last changed 3 months ago</p>
                </div>
                <button class="btn btn-outline-dark rounded-pill px-3 btn-sm fw-bold tracking-wide text-uppercase">Change</button>
              </div>

              <hr class="border-secondary opacity-10 my-4">

              <div class="d-flex align-items-center justify-content-between">
                <div>
                  <h6 class="fw-bold mb-1 fs-6">Two-Factor Authentication</h6>
                  <p class="text-muted small mb-0">Add an extra layer of security to your account.</p>
                </div>
                <div class="form-check form-switch">
                  <input class="form-check-input" type="checkbox" role="switch" id="2faSwitch">
                </div>
              </div>

              <div class="mt-4 pt-3 bg-light rounded-3 p-3 d-flex align-items-start gap-3">
                 <i class="bi bi-shield-check text-success fs-5"></i>
                 <div>
                    <span class="d-block fw-bold small text-dark">Login Activity</span>
                    <span class="d-block text-muted extra-small">Last login: Today, 10:42 AM from Pune, India</span>
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
  name: "ProfileView",
  data() {
    return {
      activeTab: 'profile',
      isEditing: false,
      loading: true,
      saving: false,
      
      // User Data Structure
      user: {
        name: "",
        email: "",
        phone: "",
        gender: "",
        dob: ""
      },
      
      editForm: {}
    };
  },
  computed: {
    userInitials() {
      if (!this.user.name) return 'U';
      return this.user.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
    }
  },
  mounted() {
    this.fetchUserProfile();
  },
  methods: {
    async fetchUserProfile() {
      this.loading = true;
      try {
        const response = await api.get('/user/profile');
        this.user = response.data.data;
      } catch (error) {
        console.error("Failed to fetch profile:", error);
        if (error.response && error.response.status === 401) {
          this.$router.push('/login');
        }
      } finally {
        this.loading = false;
      }
    },

    handleNavigation(page) {
      this.$router.push(`/${page}`);
    },

    logout() {
      if(confirm("Are you sure you want to log out?")) {
        localStorage.removeItem('token'); 
        this.$router.push('/login');
      }
    },

    toggleEdit() {
      this.editForm = { ...this.user };
      // Format DOB for date input if necessary (API sends YYYY-MM-DD which works for inputs)
      this.isEditing = true;
    },

    cancelEdit() {
      this.isEditing = false;
      this.editForm = {};
    },

    async saveChanges() {
      this.saving = true;
      try {
        const payload = {
          name: this.editForm.name,
          phone: this.editForm.phone,
          gender: this.editForm.gender,
          dob: this.editForm.dob
        };

        const response = await api.patch('/user/profile', payload);
        
        // Update local user data with response
        this.user = response.data.data;
        this.isEditing = false;
        alert("Profile updated successfully.");
      } catch (error) {
        console.error("Failed to update profile:", error);
        alert("Failed to update profile. Please try again.");
      } finally {
        this.saving = false;
      }
    }
  }
};
</script>

<style scoped>
/* Reusing your exact styles */
.bg-light-subtle { background-color: #f9fafb !important; }
.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }
.form-control:focus, .form-select:focus { background-color: #fff; border: 1px solid #000 !important; box-shadow: none; }
.animate-fade-up { animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; opacity: 0; transform: translateY(20px); }
.delay-100 { animation-delay: 0.1s; }
.delay-200 { animation-delay: 0.2s; }
@keyframes fadeUp { to { opacity: 1; transform: translateY(0); } }
.transition-all { transition: all 0.2s ease; }
.hover-bg-light:hover { background-color: #f8f9fa; color: #000 !important; }
.hover-bg-danger-subtle:hover { background-color: #fff5f5; color: #dc3545 !important; }
.hover-lift { transition: transform 0.2s ease, box-shadow 0.2s ease; }
.hover-lift:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.sticky-lg-top { position: -webkit-sticky; position: sticky; top: 100px; }
</style>