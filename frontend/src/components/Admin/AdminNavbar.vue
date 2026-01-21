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
        class="navbar-toggler border-0"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#adminNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="adminNav">
        <ul class="navbar-nav ms-auto gap-lg-4 mb-2 mb-lg-0 align-items-lg-center">

          <li class="nav-item"><router-link to="/admin/dashboard" class="nav-link fw-medium" active-class="active">Dashboard</router-link></li>
          <li class="nav-item"><router-link to="/admin/categories" class="nav-link fw-medium" active-class="active">Categories</router-link></li>
          <li class="nav-item"><router-link to="/admin/products" class="nav-link fw-medium" active-class="active">Products</router-link></li>
          <li class="nav-item"><router-link to="/admin/orders" class="nav-link fw-medium" active-class="active">Orders</router-link></li>
          <li class="nav-item"><router-link to="/admin/users" class="nav-link fw-medium" active-class="active">Users</router-link></li>
          <li class="nav-item"><router-link to="/admin/messages" class="nav-link fw-medium" active-class="active">Messages</router-link></li>
          <li class="nav-item"><router-link to="/admin/analytics" class="nav-link fw-medium" active-class="active">Analytics</router-link></li>
          
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
  methods: {
    logout() {
      this.$emit('logout'); // Ensure this matches your App.vue logout handler
      this.$router.push("/login");
    }
  }
};
</script>

<style scoped>
/* Updated link colors for the white background */
.nav-link {
  color: #555 !important;
  position: relative; /* Required for the underline positioning */
  padding-bottom: 5px; /* Adds a little space for the underline */
}

.nav-link:hover, .nav-link.active {
  color: #000 !important;
}

/* The Underline Animation Logic */
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

/* Show underline on hover and when the link is active */
.nav-link:hover::after, 
.nav-link.active::after {
  transform: scaleX(1);
  transform-origin: bottom left;
}

.tracking-tight { letter-spacing: -0.05em; }
</style>