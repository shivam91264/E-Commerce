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

      <a class="navbar-brand fw-bold tracking-tight me-lg-5" href="#" @click.prevent="$emit('navigate', 'home')">
        MARKETHUB<span class="text-primary">.</span>
      </a>

      <div class="collapse navbar-collapse flex-grow-0 me-auto d-none d-lg-block">
        <ul class="navbar-nav gap-4">
          <li class="nav-item">
            <a class="nav-link hover-underline active" href="#" @click.prevent="$emit('navigate', 'home')">Home</a>
          </li>
          
          <li class="nav-item dropdown">
            <a 
              class="nav-link hover-underline d-flex align-items-center gap-1 dropdown-toggle" 
              href="#" 
              role="button" 
              data-bs-toggle="dropdown" 
              aria-expanded="false"
            >
              Shop
            </a>
            <ul class="dropdown-menu border-0 shadow-lg p-3 rounded-3 mt-2">
              <li v-for="cat in categories" :key="cat.id">
                <a class="dropdown-item py-2 rounded-2" href="#" @click.prevent="$emit('filter-category', cat.id)">
                  {{ cat.name }}
                </a>
              </li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item fw-bold" href="#">View All</a></li>
            </ul>
          </li>

          <li class="nav-item">
            <a class="nav-link hover-underline" href="#">New Arrivals</a>
          </li>
          <li class="nav-item">
            <a class="nav-link hover-underline" href="#">About</a>
          </li>
        </ul>
      </div>

      <div class="d-none d-lg-block mx-auto w-100 px-5" style="max-width: 600px;">
        <form class="position-relative" @submit.prevent="handleSearch">
          <input 
            type="text" 
            class="form-control rounded-pill border-0 bg-light py-2 ps-4 pe-5 focus-ring"
            placeholder="Search for products..."
            v-model="searchQuery"
          >
          <button class="btn position-absolute top-50 end-0 translate-middle-y border-0 text-muted pe-3" type="submit">
            <i class="bi bi-search"></i>
          </button>
        </form>
      </div>

      <div class="d-flex align-items-center gap-3 gap-lg-4 ms-auto">
        
        <button class="btn btn-link text-dark p-0 d-lg-none" @click="toggleMobileSearch">
          <i class="bi bi-search fs-5"></i>
        </button>

        <div class="dropdown">
          <a 
            class="text-dark text-decoration-none d-flex align-items-center gap-2" 
            href="#" 
            role="button" 
            data-bs-toggle="dropdown" 
            aria-expanded="false"
          >
            <i class="bi bi-person fs-5"></i>
            <span class="d-none d-lg-inline small fw-medium" v-if="isAuthenticated">Account</span>
          </a>
          <ul class="dropdown-menu dropdown-menu-end border-0 shadow-lg rounded-3 mt-3">
            <template v-if="!isAuthenticated">
              <li><a class="dropdown-item py-2" href="#" @click.prevent="$emit('navigate', 'login')">Login</a></li>
              <li><a class="dropdown-item py-2" href="#" @click.prevent="$emit('navigate', 'register')">Register</a></li>
            </template>
            <template v-else>
              <li class="px-3 py-2"><small class="text-muted">Signed in as <strong>{{ userRole }}</strong></small></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="#" @click.prevent="$emit('navigate', 'profile')">Profile</a></li>
              <li><a class="dropdown-item" href="#" @click.prevent="$emit('navigate', 'orders')">Orders</a></li>
              <li><a class="dropdown-item text-danger" href="#" @click.prevent="$emit('logout')">Logout</a></li>
            </template>
          </ul>
        </div>

        <a class="text-dark position-relative" href="#" @click.prevent="$emit('navigate', 'cart')">
          <i class="bi bi-bag fs-5"></i>
          <span 
            v-if="cartItemCount > 0" 
            class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-dark border border-white text-white"
            style="font-size: 0.65rem; padding: 0.35em 0.5em;"
          >
            {{ cartItemCount }}
          </span>
        </a>
      </div>
    </div>

    <div class="w-100 bg-white border-bottom p-3 d-lg-none mobile-search-bar" v-if="showMobileSearch">
      <form @submit.prevent="handleSearch" class="position-relative">
        <input 
          type="text" 
          class="form-control rounded-pill border bg-light py-2 px-4" 
          placeholder="Search..."
          v-model="searchQuery"
          ref="mobileSearchInput"
        >
      </form>
    </div>
  </nav>

  <div class="offcanvas offcanvas-start" tabindex="-1" id="mobileMenu">
    <div class="offcanvas-header border-bottom">
      <h5 class="offcanvas-title fw-bold tracking-tight">MENU</h5>
      <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body d-flex flex-column">
      <ul class="nav flex-column gap-3 fs-5 mb-auto">
        <li class="nav-item">
          <a class="nav-link text-dark fw-medium" href="#" @click.prevent="navigateMobile('home')">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link text-dark fw-medium d-flex justify-content-between align-items-center" data-bs-toggle="collapse" href="#shopCollapse" role="button">
            Shop <i class="bi bi-chevron-down fs-6"></i>
          </a>
          <div class="collapse mt-2 ps-3" id="shopCollapse">
            <ul class="list-unstyled d-flex flex-column gap-3 border-start ps-3 my-2">
              <li v-for="cat in categories" :key="cat.id">
                <a href="#" class="text-decoration-none text-muted" @click.prevent="navigateMobile('category', cat)">{{ cat.name }}</a>
              </li>
            </ul>
          </div>
        </li>
        <li class="nav-item"><a class="nav-link text-dark fw-medium" href="#">New Arrivals</a></li>
        <li class="nav-item"><a class="nav-link text-dark fw-medium" href="#">About Us</a></li>
      </ul>
      <div class="mt-4 border-top pt-4">
        <button v-if="!isAuthenticated" class="btn btn-dark w-100 py-3 rounded-pill fw-bold mb-3" @click="navigateMobile('login')">Log In / Sign Up</button>
        <button v-else class="btn btn-outline-danger w-100 py-3 rounded-pill fw-bold" @click="$emit('logout')">Log Out</button>
      </div>
    </div>
  </div>
</template>

<script>
/* Ensure Bootstrap JS is loaded in your main.js or index.html for this to work */
export default {
  name: "PremiumNavbar",
  props: {
    isAuthenticated: Boolean,
    cartItemCount: Number,
    userRole: String
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
    navigateMobile(route, payload) {
      // Use pure DOM selector if Bootstrap import isn't available in component
      const offcanvasEl = document.getElementById('mobileMenu');
      // eslint-disable-next-line
      if (typeof bootstrap !== 'undefined') {
        const bsOffcanvas = bootstrap.Offcanvas.getInstance(offcanvasEl) || new bootstrap.Offcanvas(offcanvasEl);
        bsOffcanvas.hide();
      }
      
      if (payload) this.$emit('filter-category', payload.id);
      else this.$emit('navigate', route);
    }
  }
};
</script>

<style scoped>
.premium-navbar {
  transition: box-shadow 0.3s ease, padding 0.3s ease;
  padding-top: 1rem;
  padding-bottom: 1rem;
}
.premium-navbar.scrolled {
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
}
.tracking-tight { letter-spacing: -0.05em; }

.nav-link {
  color: #4a4a4a;
  font-weight: 500;
  font-size: 0.95rem;
  transition: color 0.2s ease;
}
.nav-link:hover, .nav-link.active, .nav-link.show {
  color: #000;
}

.hover-underline { position: relative; }
.hover-underline::after {
  content: ''; position: absolute; width: 100%; transform: scaleX(0); height: 2px;
  bottom: 0; left: 0; background-color: #000; transform-origin: bottom right; transition: transform 0.25s ease-out;
}
.hover-underline:hover::after { transform: scaleX(1); transform-origin: bottom left; }

.form-control.bg-light { background-color: #f3f4f6 !important; }
.form-control:focus { background-color: #fff !important; box-shadow: 0 0 0 2px rgba(0,0,0,0.1); }

.mobile-search-bar { animation: slideDown 0.3s ease-out; }
@keyframes slideDown { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
</style>