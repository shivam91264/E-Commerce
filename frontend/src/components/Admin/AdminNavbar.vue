<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white sticky-top py-3 border-bottom">
    <div class="container px-lg-5">
      <router-link
        class="navbar-brand fw-bold tracking-tight fs-4 text-dark"
        to="/admin/dashboard"
      >
        MARKETHUB
        <span class="text-muted fw-normal fs-6 ps-2">| &nbsp;Admin</span>
      </router-link>

      <button 
        class="btn btn-link text-dark border-0 p-0 d-lg-none" 
        type="button" 
        @click="toggleNav"
      >
        <i class="bi bi-list fs-2"></i>
      </button>

      <div 
        class="collapse navbar-collapse" 
        :class="{ show: isNavOpen }" 
        id="adminNav"
      >
        <ul class="navbar-nav ms-auto gap-lg-4 mb-2 mb-lg-0 align-items-lg-center">

          <li class="nav-item" @click="closeNav">
            <router-link to="/admin/dashboard" class="nav-link fw-medium" active-class="active">Dashboard</router-link>
          </li>
          <li class="nav-item" @click="closeNav">
            <router-link to="/admin/categories" class="nav-link fw-medium" active-class="active">Categories</router-link>
          </li>
          <li class="nav-item" @click="closeNav">
            <router-link to="/admin/products" class="nav-link fw-medium" active-class="active">Products</router-link>
          </li>
          <li class="nav-item" @click="closeNav">
            <router-link to="/admin/orders" class="nav-link fw-medium" active-class="active">Orders</router-link>
          </li>
          <li class="nav-item" @click="closeNav">
            <router-link to="/admin/users" class="nav-link fw-medium" active-class="active">Users</router-link>
          </li>
          <li class="nav-item" @click="closeNav">
            <router-link to="/admin/messages" class="nav-link fw-medium" active-class="active">Messages</router-link>
          </li>
          <li class="nav-item" @click="closeNav">
            <router-link to="/admin/analytics" class="nav-link fw-medium" active-class="active">Analytics</router-link>
          </li>
          
          <li class="nav-item ms-lg-3">
            <button class="btn btn-dark rounded-pill px-4 btn-sm fw-bold text-uppercase tracking-wide" @click="logout">
              Log Out
            </button>
          </li>

        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "AdminNavbar",
  data() {
    return {
      isNavOpen: false
    };
  },
  methods: {
    toggleNav() {
      this.isNavOpen = !this.isNavOpen;
    },
    closeNav() {
      this.isNavOpen = false;
    },
    logout() {
      this.isNavOpen = false;
      this.$emit('logout'); 
      this.$router.push("/login");
    }
  }
};
</script>

<style scoped>
/* Existing Link Styles */
.nav-link {
  color: #555 !important;
  position: relative;
  padding-bottom: 5px;
}

.nav-link:hover, .nav-link.active {
  color: #000 !important;
}

.nav-link::after {
  content: '';
  position: absolute;
  width: 100%;
  transform: scaleX(0);
  height: 2px;
  bottom: 0;
  left: 0;
  background-color: #000;
  transform-origin: bottom right;
  transition: transform 0.25s ease-out;
}

.nav-link:hover::after, 
.nav-link.active::after {
  transform: scaleX(1);
  transform-origin: bottom left;
}

.tracking-tight { letter-spacing: -0.05em; }

/* 3. NEW: This Media Query copies the behavior from UserNavbar */
@media (max-width: 991px) {
  .navbar-collapse {
    /* Absolute positioning allows it to overlay content instead of pushing it down */
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    background: white;
    padding: 1rem;
    box-shadow: 0 10px 15px rgba(0,0,0,0.1); /* Adds the "floating" effect */
    z-index: 1000;
  }
  
  /* Ensures the menu actually appears when Vue adds the 'show' class */
  .navbar-collapse.show {
    display: block !important;
  }

  /* Optional: Adds a little spacing between items on mobile */
  .nav-item {
    padding: 10px 0;
    border-bottom: 1px solid #f8f9fa;
  }
  .nav-item:last-child {
    border-bottom: none;
  }
}
</style>