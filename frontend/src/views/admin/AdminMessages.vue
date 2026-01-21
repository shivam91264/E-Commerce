<template>
  <div class="d-flex flex-column min-vh-100 bg-light-subtle">

    <main class="flex-grow-1 py-5">
      <div class="container px-lg-5">
        
        <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-center mb-5 gap-3 animate-fade-up">
          <div>
            <h1 class="display-5 fw-bold tracking-tight mb-2">Customer Queries</h1>
            <p class="text-muted lead fs-6 mb-0">Review and respond to messages from the contact page.</p>
          </div>
          <div class="d-flex gap-2">
            <button class="btn btn-white border shadow-sm rounded-pill px-4 py-2 fw-bold text-uppercase extra-small tracking-wide hover-lift" @click="archiveAllResolved">
              <i class="bi bi-archive me-2"></i> Archive Resolved
            </button>
          </div>
        </div>

        <div class="card border-0 shadow-sm rounded-4 p-3 mb-4 animate-fade-up delay-100">
          <div class="row g-3 align-items-center">
            <div class="col-lg-5">
              <div class="position-relative">
                <i class="bi bi-search position-absolute top-50 start-0 translate-middle-y ms-3 text-muted"></i>
                <input type="text" class="form-control border-0 bg-light rounded-pill ps-5" placeholder="Search sender, email, or subject..." v-model="searchQuery">
              </div>
            </div>
            <div class="col-6 col-lg-3 ms-auto">
              <select class="form-select border-0 bg-light rounded-pill fs-6" v-model="filterStatus">
                <option value="All">All Statuses</option>
                <option value="New">New</option>
                <option value="In Progress">In Progress</option>
                <option value="Resolved">Resolved</option>
                <option value="Archived">Archived</option>
              </select>
            </div>
            <div class="col-6 col-lg-2">
              <select class="form-select border-0 bg-light rounded-pill fs-6" v-model="sortOrder">
                <option value="Newest">Newest First</option>
                <option value="Oldest">Oldest First</option>
              </select>
            </div>
          </div>
        </div>

        <div class="card border-0 shadow-sm rounded-4 overflow-hidden animate-fade-up delay-200">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="bg-light">
                <tr>
                  <th class="ps-4 py-3 text-uppercase extra-small text-muted fw-bold border-0">Sender</th>
                  <th class="py-3 text-uppercase extra-small text-muted fw-bold border-0">Subject</th>
                  <th class="py-3 text-uppercase extra-small text-muted fw-bold border-0">Date</th>
                  <th class="py-3 text-uppercase extra-small text-muted fw-bold border-0">Status</th>
                  <th class="pe-4 py-3 text-uppercase extra-small text-muted fw-bold border-0 text-end">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="msg in filteredMessages" :key="msg.id" class="cursor-pointer" :class="{'bg-blue-soft': msg.status === 'New'}" @click="openMessageDrawer(msg)">
                  
                  <td class="ps-4 py-3">
                    <div class="d-flex align-items-center gap-3">
                      <div class="bg-white rounded-circle d-flex align-items-center justify-content-center fw-bold text-secondary border shadow-sm" style="width: 40px; height: 40px; font-size: 0.8rem;">
                        {{ getInitials(msg.name) }}
                      </div>
                      <div>
                        <span class="d-block fw-bold text-dark small" :class="{'text-primary': msg.status === 'New'}">{{ msg.name }}</span>
                        <span class="d-block extra-small text-muted">{{ msg.email }}</span>
                      </div>
                    </div>
                  </td>
                  
                  <td class="py-3 small text-dark fw-medium" style="max-width: 250px;">
                    <div class="text-truncate">{{ msg.subject }}</div>
                  </td>

                  <td class="py-3 small text-muted">{{ msg.date }}</td>

                  <td class="py-3">
                    <span class="badge rounded-pill border px-2 py-1 extra-small fw-bold text-uppercase" :class="getStatusClass(msg.status)">
                      {{ msg.status }}
                    </span>
                  </td>

                  <td class="pe-4 py-3 text-end" @click.stop>
                    <div class="d-flex justify-content-end gap-2">
                      <button class="btn btn-sm btn-white border rounded-circle shadow-sm" title="View" @click="openMessageDrawer(msg)">
                        <i class="bi bi-eye extra-small"></i>
                      </button>
                      
                      <button v-if="msg.status !== 'Resolved'" class="btn btn-sm btn-white border rounded-circle shadow-sm hover-text-success" title="Mark Resolved" @click="updateStatus(msg, 'Resolved')">
                        <i class="bi bi-check2 extra-small"></i>
                      </button>
                      
                      <button class="btn btn-sm btn-white border rounded-circle shadow-sm hover-text-secondary" title="Archive" @click="updateStatus(msg, 'Archived')">
                        <i class="bi bi-archive extra-small"></i>
                      </button>
                    </div>
                  </td>
                </tr>
                
                <tr v-if="filteredMessages.length === 0">
                  <td colspan="5" class="text-center py-5">
                    <div class="d-inline-flex p-3 rounded-circle bg-light mb-3">
                      <i class="bi bi-chat-left-text text-muted fs-3"></i>
                    </div>
                    <h5 class="fw-bold mb-1">No messages found</h5>
                    <p class="text-muted small mb-0">Once customers submit queries, you’ll see them here.</p>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div class="card-footer bg-white border-top p-3">
            <div class="d-flex justify-content-between align-items-center">
              <span class="text-muted extra-small">Showing {{ filteredMessages.length }} messages</span>
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

    <div class="offcanvas offcanvas-end border-0 shadow-2xl" tabindex="-1" id="messageDrawer" ref="messageDrawer" style="width: 500px;">
      
      <div class="offcanvas-header p-4 border-bottom bg-light-subtle">
        <div>
          <h5 class="offcanvas-title fw-bold tracking-tight">Message Details</h5>
          <span class="font-monospace text-muted extra-small" v-if="selectedMessage">ID: #MSG-{{ selectedMessage.id }}</span>
        </div>
        <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      
      <div class="offcanvas-body p-0 d-flex flex-column h-100" v-if="selectedMessage">
        
        <div class="p-4 border-bottom">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <span class="badge rounded-pill border px-3 py-1 extra-small fw-bold text-uppercase" :class="getStatusClass(selectedMessage.status)">
              {{ selectedMessage.status }}
            </span>
            <span class="text-muted extra-small">{{ selectedMessage.fullDate }}</span>
          </div>
          
          <div class="d-flex align-items-center gap-3">
             <div class="bg-dark text-white rounded-circle d-flex align-items-center justify-content-center fw-bold fs-5" style="width: 48px; height: 48px;">
               {{ getInitials(selectedMessage.name) }}
             </div>
             <div>
               <h6 class="fw-bold mb-0">{{ selectedMessage.name }}</h6>
               <a :href="`mailto:${selectedMessage.email}`" class="text-decoration-none small text-muted hover-underline">{{ selectedMessage.email }}</a>
             </div>
          </div>
        </div>

        <div class="p-4 flex-grow-1 overflow-auto custom-scrollbar">
          <h6 class="fw-bold mb-3">{{ selectedMessage.subject }}</h6>
          <div class="p-3 bg-light rounded-3 border-start border-4 border-dark mb-4">
             <p class="text-dark small mb-0 lh-lg" style="white-space: pre-wrap;">{{ selectedMessage.message }}</p>
          </div>

          <div class="mb-4">
             <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Admin Internal Notes</label>
             <textarea class="form-control bg-light border-0" rows="2" placeholder="Add a private note about this ticket..."></textarea>
          </div>

          <div>
            <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Reply to Customer</label>
            <div class="border rounded-3 overflow-hidden">
               <textarea class="form-control border-0" rows="4" placeholder="Type your reply here..."></textarea>
               <div class="bg-light p-2 border-top d-flex justify-content-between align-items-center">
                  <div class="d-flex gap-2">
                     <button class="btn btn-sm btn-link text-muted"><i class="bi bi-paperclip"></i></button>
                     <button class="btn btn-sm btn-link text-muted"><i class="bi bi-emoji-smile"></i></button>
                  </div>
                  <button class="btn btn-dark btn-sm rounded-pill px-3 fw-bold text-uppercase extra-small">Send Reply</button>
               </div>
            </div>
          </div>
        </div>

        <div class="p-4 border-top bg-light-subtle mt-auto">
          <div class="row g-2">
            <div class="col-6">
              <button class="btn btn-white border w-100 py-2 fw-bold text-uppercase extra-small hover-lift" 
                v-if="selectedMessage.status !== 'In Progress'"
                @click="updateStatus(selectedMessage, 'In Progress')">
                Mark In Progress
              </button>
            </div>
            <div class="col-6">
              <button class="btn btn-dark w-100 py-2 fw-bold text-uppercase extra-small hover-lift" 
                v-if="selectedMessage.status !== 'Resolved'"
                @click="updateStatus(selectedMessage, 'Resolved')">
                Resolve Ticket
              </button>
            </div>
             <div class="col-12 mt-2" v-if="selectedMessage.status === 'Resolved'">
               <button class="btn btn-outline-secondary w-100 py-2 fw-bold text-uppercase extra-small hover-bg-gray" 
                 @click="updateStatus(selectedMessage, 'Archived')">
                 Archive Ticket
               </button>
             </div>
          </div>
        </div>

      </div>
    </div>


  </div>
</template>

<script>
/* Global bootstrap variable expected from CDN/main.js */
/* eslint-disable no-undef */
import api from "@/services/api";
import { Offcanvas } from 'bootstrap'; // Explicit Import to prevent crash

export default {
  name: "AdminMessages",
  data() {
    return {
      searchQuery: "",
      filterStatus: "All",
      sortOrder: "Newest",
      selectedMessage: null,
      drawerInstance: null,
      
      // Real Data Container
      messages: [], 
      loading: false
    };
  },
  
  computed: {
    filteredMessages() {
      // 1. Filter Logic
      let result = this.messages.filter(msg => {
        const matchesSearch = msg.name.toLowerCase().includes(this.searchQuery.toLowerCase()) || 
                              msg.email.toLowerCase().includes(this.searchQuery.toLowerCase()) || 
                              msg.subject.toLowerCase().includes(this.searchQuery.toLowerCase());
        const matchesStatus = this.filterStatus === "All" || msg.status === this.filterStatus;
        return matchesSearch && matchesStatus;
      });

      // 2. Sort Logic (Frontend Side)
      if (this.sortOrder === 'Newest') {
         // Assuming API returns sorted by newest, otherwise implement date comparison here
      } else {
         result = result.slice().reverse(); // Create copy and reverse
      }
      
      return result;
    }
  },

  mounted() {
    // Initialize Bootstrap Drawer
    if (this.$refs.messageDrawer) {
      this.drawerInstance = new Offcanvas(this.$refs.messageDrawer);
    }
    // Fetch initial data
    this.fetchMessages();
  },

  methods: {
    // --- 1. Fetch Messages ---
    async fetchMessages() {
      this.loading = true;
      try {
        const response = await api.get('/admin/messages');
        this.messages = response.data.data;
      } catch (error) {
        console.error("Failed to load messages", error);
      } finally {
        this.loading = false;
      }
    },

    // --- 2. Update Single Status ---
    async updateStatus(msg, newStatus) {
      try {
        // Optimistic UI update (update immediately for responsiveness)
        const oldStatus = msg.status;
        msg.status = newStatus;

        await api.put(`/admin/messages/${msg.id}/status`, { status: newStatus });
        
        // If successful, ensure selectedMessage in drawer also reflects this
        if (this.selectedMessage && this.selectedMessage.id === msg.id) {
            this.selectedMessage.status = newStatus;
        }
      } catch (error) {
        // Revert on failure
        msg.status = oldStatus; 
        alert("Failed to update status");
      }
    },

    // --- 3. Bulk Archive ---
    async archiveAllResolved() {
      if(!confirm("Archive all resolved messages?")) return;
      
      try {
        await api.put('/admin/messages/archive-resolved');
        // Refresh list to show changes
        await this.fetchMessages(); 
        alert("Messages archived successfully");
      } catch (error) {
        alert("Failed to archive messages");
      }
    },

    // --- Helper Methods ---
    getInitials(name) {
      if(!name) return "U";
      return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
    },
    
    openMessageDrawer(msg) {
      this.selectedMessage = msg;
      this.drawerInstance?.show();
    },
    
    getStatusClass(status) {
      switch(status) {
        case 'New': return 'bg-primary-subtle text-primary border-primary-subtle';
        case 'In Progress': return 'bg-warning-subtle text-warning-emphasis border-warning-subtle';
        case 'Resolved': return 'bg-success-subtle text-success border-success-subtle';
        case 'Archived': return 'bg-secondary-subtle text-secondary border-secondary-subtle';
        default: return 'bg-light text-dark';
      }
    }
  }
};
</script>

<style scoped>
/* ADMIN THEME STYLES */

/* Backgrounds */
.bg-light-subtle { background-color: #f9fafb !important; }
.bg-blue-soft { background-color: rgba(13, 110, 253, 0.03) !important; } /* Highlight for New messages */

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

.hover-underline:hover { text-decoration: underline !important; }
.hover-bg-gray:hover { background-color: #f8f9fa !important; }

/* Table Styling */
.table-hover tbody tr:hover { background-color: #f1f3f5; }
.cursor-pointer { cursor: pointer; }

.hover-text-success:hover { color: #198754 !important; border-color: #198754 !important; }
.hover-text-secondary:hover { color: #6c757d !important; border-color: #6c757d !important; }

/* Buttons */
.btn-white {
  background-color: #fff; color: #000; border-color: #dee2e6;
}
.btn-white:hover { border-color: #000; }

/* Form Elements */
.form-control:focus, .form-select:focus {
  background-color: #fff;
  border: 1px solid #000 !important;
  box-shadow: none;
}

/* Shadows */
.shadow-2xl { box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); }

/* Custom Scrollbar for Drawer */
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: #f1f1f1; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #ccc; border-radius: 3px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #999; }
</style>