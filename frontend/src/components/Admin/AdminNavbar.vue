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

          <li class="nav-item"><router-link to="/admindashboard" class="nav-link fw-medium" active-class="active">Dashboard</router-link></li>
          <li class="nav-item"><router-link to="/adminproducts" class="nav-link fw-medium" active-class="active">Products</router-link></li>
          <li class="nav-item"><router-link to="/adminorders" class="nav-link fw-medium" active-class="active">Orders</router-link></li>
          <li class="nav-item"><router-link to="/adminusers" class="nav-link fw-medium" active-class="active">Users</router-link></li>
          <li class="nav-item"><router-link to="/adminmessages" class="nav-link fw-medium" active-class="active">Messages</router-link></li>
          <li class="nav-item"><router-link to="/adminanalytics" class="nav-link fw-medium" active-class="active">Analytics</router-link></li>
          
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
}
.nav-link:hover, .nav-link.active {
  color: #000 !important;
}

.tracking-tight { letter-spacing: -0.05em; }
</style>