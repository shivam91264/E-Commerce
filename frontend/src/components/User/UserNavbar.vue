<template>
  <nav class="navbar navbar-expand-lg sticky-top bg-white premium-navbar" :class="{ 'scrolled': isScrolled }">
    <div class="container-fluid px-lg-5">

      <button 
        class="btn btn-link text-dark border-0 p-0 me-3 d-lg-none" 
        type="button" 
        @click="toggleNav"
      >
        <i class="bi bi-list fs-2"></i>
      </button>

      <router-link class="navbar-brand fw-bold tracking-tight me-lg-5" to="/">
        MARKETHUB<span class="text-primary">.</span>
      </router-link>

      <div 
        class="collapse navbar-collapse flex-grow-0 me-auto"
        :class="{ 'show': isNavOpen }"
        id="userNav"
      >
        <ul class="navbar-nav gap-4">
          
          <template v-if="userRole === 'admin'">
            <li class="nav-item" @click="closeNav"><router-link class="nav-link hover-underline" to="/admin/dashboard">Dashboard</router-link></li>
            <li class="nav-item" @click="closeNav"><router-link class="nav-link hover-underline" to="/admin/products">Products</router-link></li>
            <li class="nav-item" @click="closeNav"><router-link class="nav-link hover-underline" to="/admin/orders">Orders</router-link></li>
            <li class="nav-item" @click="closeNav"><router-link class="nav-link hover-underline" to="/admin/analytics">Analytics</router-link></li>
          </template>

          <template v-else>
            <li class="nav-item" @click="closeNav"><router-link class="nav-link hover-underline" to="/">Home</router-link></li>
            
            <li class="nav-item dropdown">
              <a class="nav-link hover-underline d-flex align-items-center gap-1 dropdown-toggle" href="#" data-bs-toggle="dropdown">Shop</a>
              <ul class="dropdown-menu border-0 shadow-lg p-3 rounded-3 mt-2">
                <li v-if="categories.length === 0">
                  <span class="dropdown-item text-muted small">Loading categories...</span>
                </li>

                <li v-for="cat in categories" :key="cat.id" @click="closeNav">
                  <router-link 
                    :to="{ path: '/shop', query: { category: cat.slug } }" 
                    class="dropdown-item py-2 rounded-2"
                  >
                    {{ cat.name }}
                  </router-link>
                </li>

                <li><hr class="dropdown-divider"></li>
                <li @click="closeNav"><router-link class="dropdown-item fw-bold" to="/shop">View All</router-link></li>
              </ul>
            </li>

            <li class="nav-item" @click="closeNav"><router-link class="nav-link hover-underline" to="/newarrivals">New Arrivals</router-link></li>
            <li class="nav-item" @click="closeNav"><router-link class="nav-link hover-underline" to="/about">About</router-link></li>
            <li class="nav-item" @click="closeNav"><router-link class="nav-link hover-underline" to="/contact">Contact</router-link></li>
          </template>

        </ul>
      </div>

      <div class="d-flex align-items-center gap-3 gap-lg-4 ms-auto">
        <button v-if="userRole !== 'admin'" class="btn btn-link text-dark p-0 d-lg-none" @click="toggleMobileSearch">
          <i class="bi bi-search fs-5"></i>
        </button>

        <div v-if="userRole !== 'admin'" class="d-none d-lg-block" style="width: 250px;">
           <form class="position-relative" @submit.prevent="handleSearch">
            <input type="text" class="form-control rounded-pill border-0 bg-light py-2 ps-4 pe-5" placeholder="Search..." v-model="searchQuery">
            <button class="btn position-absolute top-50 end-0 translate-middle-y border-0 text-muted pe-3" type="submit"><i class="bi bi-search"></i></button>
          </form>
        </div>

        <div class="dropdown">
          <a class="text-dark d-flex align-items-center gap-2 text-decoration-none" href="#" data-bs-toggle="dropdown">
            <i class="bi bi-person fs-5"></i>
            <span class="d-none d-lg-inline small fw-bold text-uppercase ls-1" v-if="isAuthenticated">
              {{ userRole === 'admin' ? 'Admin' : 'Account' }}
            </span>
          </a>
          <ul class="dropdown-menu dropdown-menu-end border-0 shadow-lg rounded-3 mt-3">
            <template v-if="!isAuthenticated">
              <li @click="closeNav"><router-link class="dropdown-item" to="/login">Login</router-link></li>
              <li @click="closeNav"><router-link class="dropdown-item" to="/register">Register</router-link></li>
            </template>
            <template v-else>
              <template v-if="userRole === 'admin'">
                 </template>
              <template v-else>
                <li @click="closeNav"><router-link class="dropdown-item" to="/profile">My Profile</router-link></li>
                <li @click="closeNav"><router-link class="dropdown-item" to="/order">My Orders</router-link></li>
                <li @click="closeNav"><router-link class="dropdown-item" to="/wishlist">Wishlist</router-link></li>
              </template>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item text-danger" href="#" @click.prevent="handleLogout">Logout</a></li>
            </template>
          </ul>
        </div>

        <router-link v-if="userRole !== 'admin'" class="text-dark position-relative" to="/cart" @click="closeNav">
          <i class="bi bi-bag fs-5"></i>
          <span v-if="cartItemCount > 0" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-dark border border-white text-white" style="font-size: 0.65rem; padding: 0.35em 0.5em;">{{ cartItemCount }}</span>
        </router-link>
      </div>

    </div>
  </nav>

  <div v-if="showMobileSearch" class="container-fluid bg-white py-3 border-bottom position-absolute top-100 start-0 w-100 shadow-sm" style="z-index: 999;">
      <form @submit.prevent="handleSearch">
          <input type="text" class="form-control" placeholder="Search products..." v-model="searchQuery" autoFocus>
      </form>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "UserNavbar",
  // 3. FIX: Define emits to remove console warnings
  emits: ['logout', 'search', 'filterCategory'],
  props: {
    isAuthenticated: { type: Boolean, default: false },
    cartItemCount: { type: Number, default: 0 },
    userRole: { type: String, default: 'guest' }
  },
  data() {
    return {
      searchQuery: "",
      isScrolled: false,
      showMobileSearch: false,
      categories: [],
      isNavOpen: false
    };
  },
  mounted() {
    window.addEventListener("scroll", this.handleScroll);
    this.fetchCategories();
  },
  beforeUnmount() {
    window.removeEventListener("scroll", this.handleScroll);
  },
  methods: {
    toggleNav() {
      this.isNavOpen = !this.isNavOpen;
    },
    closeNav() {
      this.isNavOpen = false;
    },
    handleLogout() {
        this.closeNav();
        this.$emit('logout');
    },
    async fetchCategories() {
      try {
        const response = await api.get('/categories');
        this.categories = response.data.data;
      } catch (error) {
        console.error("Failed to load categories:", error);
      }
    },
    handleSearch() {
      if (this.searchQuery.trim()) {
        this.$emit("search", this.searchQuery);
        this.showMobileSearch = false;
        this.closeNav(); 
        this.$router.push({ path: '/shop', query: { search: this.searchQuery } });
      }
    },
    handleScroll() {
      this.isScrolled = window.scrollY > 10;
    },
    toggleMobileSearch() {
      this.showMobileSearch = !this.showMobileSearch;
      if(this.showMobileSearch) this.closeNav();
    }
  }
};
</script>

<style scoped>
.premium-navbar { transition: all 0.3s ease; padding: 1.25rem 0; }
.premium-navbar.scrolled { box-shadow: 0 4px 20px rgba(0,0,0,0.05); padding: 0.75rem 0; }
.nav-link { font-size: 0.9rem; font-weight: 500; text-transform: uppercase; color: #555; }
.nav-link:hover { color: #000 !important; }
.hover-underline { position: relative; }
.hover-underline::after { content: ''; position: absolute; width: 100%; transform: scaleX(0); height: 2px; bottom: -4px; left: 0; background-color: #000; transition: transform 0.25s; }
.hover-underline:hover::after { transform: scaleX(1); }
.form-control.bg-light { background-color: #f3f4f6 !important; }
.form-control:focus { background-color: #fff !important; border-color: #000 !important; box-shadow: none; }

/* 4. FIX: Handle Mobile Menu Visibility cleanly */
@media (max-width: 991px) {
  .navbar-collapse {
    /* Standard bootstrap collapse is display:none. We override only when .show is present */
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    background: white;
    padding: 1rem;
    box-shadow: 0 10px 15px rgba(0,0,0,0.1);
    z-index: 1000;
  }
  
  /* Force display block when Vue adds the 'show' class */
  .navbar-collapse.show {
    display: block !important;
  }
}
</style>