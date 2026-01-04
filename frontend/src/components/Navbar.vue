<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-black sticky-top py-3">
    <div class="container px-lg-5">
      <router-link
        class="navbar-brand fw-bold tracking-tight fs-4"
        to="/admin/dashboard"
      >
        MARKETHUB
        <span class="text-secondary fw-normal fs-6 ps-2">| &nbsp;Admin</span>
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

          <li class="nav-item">
            <router-link
              to="/admin/dashboard"
              class="nav-link fw-medium"
              active-class="active"
            >
              Dashboard
            </router-link>
          </li>

          <li class="nav-item">
            <router-link
              to="/admin/products"
              class="nav-link fw-medium"
              active-class="active"
            >
              Products
            </router-link>
          </li>

          <li class="nav-item">
            <router-link
              to="/admin/orders"
              class="nav-link fw-medium"
              active-class="active"
            >
              Orders
            </router-link>
          </li>

          <li class="nav-item">
            <router-link
              to="/admin/analytics"
              class="nav-link fw-medium"
              active-class="active"
            >
              Analytics
            </router-link>
          </li>

          <li class="nav-item ms-lg-3">
            <button
              class="btn btn-outline-light rounded-pill px-4 btn-sm fw-bold text-uppercase tracking-wide"
              @click="logout"
            >
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
      // later connect API / clear token
      this.$router.push("/login");
    }
  }
};
</script>

<style scoped>
/* keeps your original navbar color behavior */
.nav-link {
  color: rgba(255, 255, 255, 0.5);
}
.nav-link.active {
  color: #fff;
}
</style>
