<template>
  <div class="d-flex flex-column min-vh-100 bg-light-subtle">
    
    <AdminNavbar />

    <main class="flex-grow-1 py-5">
      <div class="container px-lg-5">
        
        <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-5 gap-3 animate-fade-up">
          <div>
            <h1 class="display-5 fw-bold tracking-tight mb-2">Manage Users</h1>
            <p class="text-muted lead fs-6 mb-0">View and manage registered customers.</p>
          </div>
          <div class="d-flex gap-2">
            <button class="btn btn-white border shadow-sm rounded-pill px-4 py-2 fw-bold text-uppercase extra-small tracking-wide hover-lift">
              <i class="bi bi-download me-2"></i> Export List
            </button>
          </div>
        </div>

        <div class="card border-0 shadow-sm rounded-4 p-3 mb-4 animate-fade-up delay-100">
          <div class="row g-3 align-items-center">
            <div class="col-lg-5">
              <div class="position-relative">
                <i class="bi bi-search position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                <input type="text" class="form-control border-0 bg-light rounded-pill ps-5" placeholder="Search by name or email..." v-model="searchQuery">
              </div>
            </div>
            <div class="col-6 col-lg-3 ms-auto">
              <select class="form-select border-0 bg-light rounded-pill fs-6" v-model="filterStatus">
                <option value="All">All Statuses</option>
                <option value="Active">Active</option>
                <option value="Blocked">Blocked</option>
              </select>
            </div>
            <div class="col-6 col-lg-2">
              <select class="form-select border-0 bg-light rounded-pill fs-6" v-model="filterRole">
                <option value="All">All Roles</option>
                <option value="User">Customer</option>
                <option value="Admin">Admin</option>
              </select>
            </div>
          </div>
        </div>

        <div class="card border-0 shadow-sm rounded-4 overflow-hidden animate-fade-up delay-200">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="bg-light">
                <tr>
                  <th class="ps-4 py-3 text-uppercase extra-small text-muted fw-bold border-0">User</th>
                  <th class="py-3 text-uppercase extra-small text-muted fw-bold border-0">Email</th>
                  <th class="py-3 text-uppercase extra-small text-muted fw-bold border-0">Phone</th>
                  <th class="py-3 text-uppercase extra-small text-muted fw-bold border-0 text-center">Orders</th>
                  <th class="py-3 text-uppercase extra-small text-muted fw-bold border-0">Status</th>
                  <th class="pe-4 py-3 text-uppercase extra-small text-muted fw-bold border-0 text-end">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in filteredUsers" :key="user.id" class="cursor-pointer" @click="openUserDrawer(user)">
                  
                  <td class="ps-4 py-3">
                    <div class="d-flex align-items-center gap-3">
                      <div class="bg-light rounded-circle d-flex align-items-center justify-content-center fw-bold text-secondary border shadow-sm" style="width: 42px; height: 42px; font-size: 0.85rem;">
                        {{ getInitials(user.name) }}
                      </div>
                      <div>
                        <span class="d-block fw-bold text-dark small">{{ user.name }}</span>
                        <span class="d-block extra-small text-muted">Joined: {{ user.joinedDate }}</span>
                      </div>
                    </div>
                  </td>
                  
                  <td class="py-3 small text-muted">{{ user.email }}</td>

                  <td class="py-3 small text-muted">{{ user.phone }}</td>

                  <td class="py-3 text-center">
                    <span class="badge bg-light text-dark border fw-normal rounded-pill extra-small px-2">
                      {{ user.ordersCount }}
                    </span>
                  </td>

                  <td class="py-3">
                    <span class="badge rounded-pill border px-2 py-1 extra-small fw-bold text-uppercase" :class="user.active ? 'bg-success-subtle text-success border-success-subtle' : 'bg-danger-subtle text-danger border-danger-subtle'">
                      {{ user.active ? 'Active' : 'Blocked' }}
                    </span>
                  </td>

                  <td class="pe-4 py-3 text-end" @click.stop>
                    <div class="d-flex justify-content-end gap-2">
                      <button class="btn btn-sm btn-white border rounded-circle shadow-sm" title="View Details" @click="openUserDrawer(user)">
                        <i class="bi bi-eye extra-small"></i>
                      </button>
                      <button class="btn btn-sm btn-white border rounded-circle shadow-sm" :class="user.active ? 'hover-text-danger' : 'hover-text-success'" :title="user.active ? 'Block User' : 'Unblock User'" @click="confirmBlockToggle(user)">
                        <i :class="user.active ? 'bi bi-slash-circle' : 'bi bi-check-circle'" class="extra-small"></i>
                      </button>
                    </div>
                  </td>
                </tr>
                
                <tr v-if="filteredUsers.length === 0">
                  <td colspan="6" class="text-center py-5">
                    <div class="d-inline-flex p-3 rounded-circle bg-light mb-3">
                      <i class="bi bi-person-x text-muted fs-3"></i>
                    </div>
                    <p class="text-muted small mb-0">No users found matching your criteria.</p>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div class="card-footer bg-white border-top p-3">
            <div class="d-flex justify-content-between align-items-center">
              <span class="text-muted extra-small">Showing {{ filteredUsers.length }} users</span>
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

    <div class="offcanvas offcanvas-end border-0 shadow-2xl" tabindex="-1" id="userDrawer" ref="userDrawer" style="width: 400px;">
      <div class="offcanvas-header p-4 border-bottom">
        <h5 class="offcanvas-title fw-bold tracking-tight">User Profile</h5>
        <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      
      <div class="offcanvas-body p-0" v-if="selectedUser">
        
        <div class="p-5 text-center bg-light border-bottom">
          <div class="mx-auto bg-white rounded-circle d-flex align-items-center justify-content-center fw-bold display-6 text-dark border shadow-sm mb-3" style="width: 80px; height: 80px;">
            {{ getInitials(selectedUser.name) }}
          </div>
          <h5 class="fw-bold mb-1">{{ selectedUser.name }}</h5>
          <p class="text-muted small mb-2">{{ selectedUser.email }}</p>
          <span class="badge rounded-pill border px-3 py-1 extra-small fw-bold text-uppercase" :class="selectedUser.active ? 'bg-success-subtle text-success border-success-subtle' : 'bg-danger-subtle text-danger border-danger-subtle'">
            {{ selectedUser.active ? 'Active Account' : 'Account Blocked' }}
          </span>
        </div>

        <div class="p-4 border-bottom">
          <h6 class="fw-bold mb-3 small text-uppercase tracking-wide text-muted">Details</h6>
          <div class="row g-3">
             <div class="col-12">
               <span class="d-block text-muted extra-small text-uppercase fw-bold">Phone</span>
               <span class="d-block fw-medium small">{{ selectedUser.phone }}</span>
             </div>
             <div class="col-6">
               <span class="d-block text-muted extra-small text-uppercase fw-bold">Joined</span>
               <span class="d-block fw-medium small">{{ selectedUser.joinedDate }}</span>
             </div>
             <div class="col-6">
               <span class="d-block text-muted extra-small text-uppercase fw-bold">Last Login</span>
               <span class="d-block fw-medium small">2 hours ago</span>
             </div>
          </div>
        </div>

        <div class="p-4 bg-light-subtle h-100">
           <h6 class="fw-bold mb-3 small text-uppercase tracking-wide text-muted">Actions</h6>
           <div class="d-grid gap-2">
             <button class="btn btn-white border w-100 text-start d-flex align-items-center justify-content-between p-3 hover-lift">
               <span class="small fw-bold"><i class="bi bi-box-seam me-2 text-muted"></i> View Orders</span>
               <i class="bi bi-chevron-right small text-muted"></i>
             </button>
             <button class="btn btn-white border w-100 text-start d-flex align-items-center justify-content-between p-3 hover-lift">
               <span class="small fw-bold"><i class="bi bi-geo-alt me-2 text-muted"></i> Saved Addresses</span>
               <i class="bi bi-chevron-right small text-muted"></i>
             </button>
             
             <button class="btn w-100 text-start d-flex align-items-center justify-content-center p-3 mt-3 fw-bold text-uppercase extra-small border" 
                     :class="selectedUser.active ? 'btn-outline-danger hover-fill-danger' : 'btn-outline-success hover-fill-success'"
                     @click="confirmBlockToggle(selectedUser)">
               <i :class="selectedUser.active ? 'bi bi-slash-circle me-2' : 'bi bi-check-circle me-2'"></i>
               {{ selectedUser.active ? 'Block User' : 'Unblock User' }}
             </button>
           </div>
        </div>

      </div>
    </div>

    <div class="modal fade" id="blockModal" tabindex="-1" aria-hidden="true" ref="blockModal">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content border-0 rounded-4 shadow-2xl p-3">
          <div class="modal-body text-center">
            <div class="mb-3 d-inline-flex align-items-center justify-content-center bg-opacity-10 rounded-circle" :class="actionTarget?.active ? 'bg-danger text-danger' : 'bg-success text-success'" style="width: 60px; height: 60px;">
              <i :class="actionTarget?.active ? 'bi bi-person-x-fill' : 'bi bi-person-check-fill'" class="fs-3"></i>
            </div>
            <h5 class="fw-bold mb-2">{{ actionTarget?.active ? 'Block User?' : 'Activate User?' }}</h5>
            <p class="text-muted small mb-4">
              {{ actionTarget?.active ? 'This user will no longer be able to log in or place orders.' : 'This user will regain access to their account.' }}
            </p>
            <div class="d-flex justify-content-center gap-2">
              <button type="button" class="btn btn-light border rounded-pill px-4 fw-bold text-uppercase extra-small" data-bs-dismiss="modal">Cancel</button>
              <button type="button" class="btn rounded-pill px-4 fw-bold text-uppercase extra-small" :class="actionTarget?.active ? 'btn-danger' : 'btn-success'" @click="executeBlockToggle">
                {{ actionTarget?.active ? 'Block' : 'Activate' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <AdminFooter />

  </div>
</template>

<script>
/* Global bootstrap variable expected */
/* eslint-disable no-undef */
import AdminNavbar from '@/components/Admin/AdminNavbar.vue';
import AdminFooter from '@/components/Admin/AdminFooter.vue';


export default {
  name: "AdminUsers",
  components: {
    AdminNavbar,
    AdminFooter
  },
  data() {
    return {
      searchQuery: "",
      filterStatus: "All",
      filterRole: "All",
      selectedUser: null,
      actionTarget: null,
      userDrawerInstance: null,
      blockModalInstance: null,
      
      // Mock Users Data
      users: [
        { id: 1, name: "Alex Morgan", email: "alex.morgan@example.com", phone: "+1 (555) 123-4567", role: "User", ordersCount: 12, active: true, joinedDate: "Jan 10, 2025" },
        { id: 2, name: "Sarah Jenkins", email: "sarah.j@example.com", phone: "+1 (555) 987-6543", role: "User", ordersCount: 5, active: true, joinedDate: "Feb 14, 2025" },
        { id: 3, name: "Michael Chen", email: "mike.chen@example.com", phone: "+1 (555) 456-7890", role: "Admin", ordersCount: 0, active: true, joinedDate: "Dec 01, 2024" },
        { id: 4, name: "David Kim", email: "david.k@example.com", phone: "+1 (555) 222-3333", role: "User", ordersCount: 2, active: false, joinedDate: "Mar 05, 2025" },
        { id: 5, name: "Emily Blunt", email: "emily.b@example.com", phone: "+1 (555) 888-9999", role: "User", ordersCount: 8, active: true, joinedDate: "Jan 22, 2025" },
      ]
    };
  },
  computed: {
    filteredUsers() {
      return this.users.filter(u => {
        const matchesSearch = u.name.toLowerCase().includes(this.searchQuery.toLowerCase()) || 
                              u.email.toLowerCase().includes(this.searchQuery.toLowerCase());
        const matchesStatus = this.filterStatus === "All" || 
                              (this.filterStatus === "Active" && u.active) || 
                              (this.filterStatus === "Blocked" && !u.active);
        const matchesRole = this.filterRole === "All" || u.role === this.filterRole;
        
        return matchesSearch && matchesStatus && matchesRole;
      });
    }
  },
  mounted() {
    if (typeof bootstrap !== 'undefined') {
      this.userDrawerInstance = new bootstrap.Offcanvas(this.$refs.userDrawer);
      this.blockModalInstance = new bootstrap.Modal(this.$refs.blockModal);
    }
  },
  methods: {
    getInitials(name) {
      return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
    },
    openUserDrawer(user) {
      this.selectedUser = user;
      this.userDrawerInstance?.show();
    },
    confirmBlockToggle(user) {
      this.actionTarget = user;
      this.blockModalInstance?.show();
    },
    executeBlockToggle() {
      if (this.actionTarget) {
        this.actionTarget.active = !this.actionTarget.active;
        this.blockModalInstance?.hide();
        // If drawer is open and looking at this user, force reactivity update (if needed) or close drawer
        if (this.selectedUser && this.selectedUser.id === this.actionTarget.id) {
           this.selectedUser.active = this.actionTarget.active; 
        }
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

.hover-fill-danger:hover {
  background-color: #dc3545; color: #fff;
}
.hover-fill-success:hover {
  background-color: #198754; color: #fff;
}
.hover-text-danger:hover { color: #dc3545 !important; border-color: #dc3545 !important; }
.hover-text-success:hover { color: #198754 !important; border-color: #198754 !important; }

/* Table Styling */
.table-hover tbody tr:hover { background-color: #f8f9fa; }
.cursor-pointer { cursor: pointer; }

/* Buttons */
.btn-white {
  background-color: #fff; color: #000; border-color: #dee2e6;
}
.btn-white:hover { border-color: #000; }

/* Forms */
.form-control:focus, .form-select:focus {
  background-color: #fff;
  border: 1px solid #000 !important;
  box-shadow: none;
}

/* Shadows */
.shadow-2xl { box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); }
</style>