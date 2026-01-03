<template>
  <nav class="navbar navbar-expand-lg sticky-top bg-white premium-navbar" :class="{ 'scrolled': isScrolled }">
    <div class="container-fluid px-lg-5">

      <button 
        class="btn btn-link text-dark border-0 p-0 me-3 d-lg-none" 
        type="button" 
        data-bs-toggle="offcanvas" 
        data-bs-target="#mobileMenu"
      >
        <i class="bi bi-list fs-2"></i>
      </button>

      <router-link class="navbar-brand fw-bold tracking-tight me-lg-5" to="/">
        MARKETHUB<span class="text-primary">.</span>
        <span v-if="userRole === 'admin'" class="ms-2 badge bg-dark text-white fw-normal ls-1 extra-small">ADMIN</span>
      </router-link>

      <div class="collapse navbar-collapse flex-grow-0 me-auto d-none d-lg-block">
        <ul class="navbar-nav gap-4">
          
          <template v-if="userRole === 'admin'">
            <li class="nav-item">
              <router-link class="nav-link hover-underline" to="/admin/dashboard">Dashboard</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link hover-underline" to="/admin/products">Products</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link hover-underline" to="/admin/orders">Orders</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link hover-underline" to="/admin/analytics">Analytics</router-link>
            </li>
          </template>

          <template v-else>
            <li class="nav-item">
              <router-link class="nav-link hover-underline" to="/">Home</router-link>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link hover-underline d-flex align-items-center gap-1 dropdown-toggle" href="#" data-bs-toggle="dropdown">Shop</a>
              <ul class="dropdown-menu border-0 shadow-lg p-3 rounded-3 mt-2">
                <li v-for="cat in categories" :key="cat.id">
                  <a class="dropdown-item py-2 rounded-2" href="#" @click.prevent="$emit('filter-category', cat.id)">{{ cat.name }}</a>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li><router-link class="dropdown-item fw-bold" to="/shop">View All</router-link></li>
              </ul>
            </li>
            <li class="nav-item">
              <router-link class="nav-link hover-underline" to="/newarrivals">New Arrivals</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link hover-underline" to="/about">About</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link hover-underline" to="/contact">Contact</router-link>
            </li>
          </template>

        </ul>
      </div>

      <div v-if="userRole !== 'admin'" class="d-none d-lg-block mx-auto w-100 px-5" style="max-width: 600px;">
        <form class="position-relative" @submit.prevent="handleSearch">
          <input 
            type="text" 
            class="form-control rounded-pill border-0 bg-light py-2 ps-4 pe-5 focus-ring"
            placeholder="Search for furniture, decor..."
            v-model="searchQuery"
          >
          <button class="btn position-absolute top-50 end-0 translate-middle-y border-0 text-muted pe-3" type="submit">
            <i class="bi bi-search"></i>
          </button>
        </form>
      </div>

      <div class="d-flex align-items-center gap-3 gap-lg-4 ms-auto">
        <button v-if="userRole !== 'admin'" class="btn btn-link text-dark p-0 d-lg-none" @click="toggleMobileSearch">
          <i class="bi bi-search fs-5"></i>
        </button>

        <div class="dropdown">
          <a class="text-dark text-decoration-none d-flex align-items-center gap-2" href="#" role="button" data-bs-toggle="dropdown">
            <i class="bi bi-person fs-5"></i>
            <span class="d-none d-lg-inline small fw-bold text-uppercase ls-1" v-if="isAuthenticated">
              {{ userRole === 'admin' ? 'Admin' : 'Account' }}
            </span>
          </a>
          <ul class="dropdown-menu dropdown-menu-end border-0 shadow-lg rounded-3 mt-3">
            <template v-if="!isAuthenticated">
              <li><router-link class="dropdown-item py-2" to="/login">Login</router-link></li>
              <li><router-link class="dropdown-item py-2" to="/register">Register</router-link></li>
            </template>
            <template v-else>
              <template v-if="userRole === 'admin'">
                <li><router-link class="dropdown-item" to="/admin/dashboard">Admin Dashboard</router-link></li>
                <li><router-link class="dropdown-item" to="/admin/messages">Messages</router-link></li>
              </template>
              <template v-else>
                <li><router-link class="dropdown-item" to="/profile">My Profile</router-link></li>
                <li><router-link class="dropdown-item" to="/orders">My Orders</router-link></li>
                <li><router-link class="dropdown-item" to="/wishlist">Wishlist</router-link></li>
              </template>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item text-danger fw-bold" href="#" @click.prevent="$emit('logout')">Logout</a></li>
            </template>
          </ul>
        </div>

        <router-link v-if="userRole !== 'admin'" class="text-dark position-relative" to="/cart">
          <i class="bi bi-bag fs-5"></i>
          <span v-if="cartItemCount > 0" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-dark border border-white text-white" style="font-size: 0.65rem; padding: 0.35em 0.5em;">
            {{ cartItemCount }}
          </span>
        </router-link>
      </div>
    </div>
  </nav>

  <div class="offcanvas offcanvas-start" tabindex="-1" id="mobileMenu">
    <div class="offcanvas-header border-bottom">
      <h5 class="offcanvas-title fw-bold tracking-tight">MARKETHUB</h5>
      <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas"></button>
    </div>
    <div class="offcanvas-body d-flex flex-column">
      <ul class="nav flex-column gap-3 fs-5 mb-auto">
        
        <template v-if="userRole === 'admin'">
          <li class="nav-item"><router-link class="nav-link text-dark fw-bold" to="/admin/dashboard" @click="closeOffcanvas">Dashboard</router-link></li>
          <li class="nav-item"><router-link class="nav-link text-dark fw-medium" to="/admin/products" @click="closeOffcanvas">Manage Products</router-link></li>
          <li class="nav-item"><router-link class="nav-link text-dark fw-medium" to="/admin/orders" @click="closeOffcanvas">Manage Orders</router-link></li>
        </template>

        <template v-else>
          <li class="nav-item"><router-link class="nav-link text-dark fw-bold" to="/" @click="closeOffcanvas">Home</router-link></li>
          <li class="nav-item"><router-link class="nav-link text-dark fw-medium" to="/shop" @click="closeOffcanvas">Shop</router-link></li>
          <li class="nav-item"><router-link class="nav-link text-dark fw-medium" to="/new-arrivals" @click="closeOffcanvas">New Arrivals</router-link></li>
          <li class="nav-item"><router-link class="nav-link text-dark fw-medium" to="/about" @click="closeOffcanvas">About Us</router-link></li>
          <li class="nav-item"><router-link class="nav-link text-dark fw-medium" to="/contact" @click="closeOffcanvas">Contact</router-link></li>
        </template>

      </ul>
      <div class="mt-4 border-top pt-4">
        <router-link v-if="!isAuthenticated" class="btn btn-dark w-100 py-3 rounded-pill fw-bold mb-3" to="/login" @click="closeOffcanvas">Log In / Sign Up</router-link>
        <button v-else class="btn btn-outline-danger w-100 py-3 rounded-pill fw-bold" @click="$emit('logout'); closeOffcanvas()">Log Out</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "UnifiedNavbar",
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
      categories: [
        { id: 1, name: "Electronics" },
        { id: 2, name: "Fashion" },
        { id: 3, name: "Home & Living" },
        { id: 4, name: "Beauty" }
      ]
    };
  },
  mounted() {
    window.addEventListener("scroll", this.handleScroll);
  },
  beforeUnmount() {
    window.removeEventListener("scroll", this.handleScroll);
  },
  methods: {
    handleSearch() {
      if (this.searchQuery.trim()) {
        this.$emit("search", this.searchQuery);
        this.showMobileSearch = false;
        this.$router.push({ path: '/search', query: { q: this.searchQuery } });
      }
    },
    handleScroll() {
      this.isScrolled = window.scrollY > 10;
    },
    toggleMobileSearch() {
      this.showMobileSearch = !this.showMobileSearch;
      if (this.showMobileSearch) {
        this.$nextTick(() => {
          if (this.$refs.mobileSearchInput) this.$refs.mobileSearchInput.focus();
        });
      }
    },
    closeOffcanvas() {
      const offcanvasEl = document.getElementById('mobileMenu');
      // eslint-disable-next-line
      if (typeof bootstrap !== 'undefined') {
        const bsOffcanvas = bootstrap.Offcanvas.getInstance(offcanvasEl) || new bootstrap.Offcanvas(offcanvasEl);
        bsOffcanvas.hide();
      }
    }
  }
};
</script>

<style scoped>
/* Styles remain unchanged to preserve your layout */
.premium-navbar {
  transition: all 0.3s ease;
  padding-top: 1.25rem;
  padding-bottom: 1.25rem;
}
.premium-navbar.scrolled {
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
}
.tracking-tight { letter-spacing: -0.05em; }
.ls-1 { letter-spacing: 1px; }
.extra-small { font-size: 0.65rem; }

.nav-link {
  color: #555;
  font-weight: 500;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.nav-link:hover, .router-link-active { color: #000 !important; }

.hover-underline { position: relative; }
.hover-underline::after {
  content: ''; position: absolute; width: 100%; transform: scaleX(0); height: 2px;
  bottom: -4px; left: 0; background-color: #000; transform-origin: bottom right; transition: transform 0.25s ease-out;
}
.hover-underline:hover::after, .router-link-active::after { transform: scaleX(1); transform-origin: bottom left; }

.form-control.bg-light { background-color: #f3f4f6 !important; border: 1px solid transparent !important; }
.form-control:focus { background-color: #fff !important; border-color: #000 !important; box-shadow: none; }
</style>