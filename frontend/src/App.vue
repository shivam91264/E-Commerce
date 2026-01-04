<template>
  <div id="app">
    <UserNavbar 
      v-if="showUserNavbar"
      :is-authenticated="isAuthenticated" 
      :cart-item-count="cartCount" 
      @logout="handleLogout"
      @search="handleSearch"
      @filter-category="handleCategory"
    />

    <AdminNavbar 
      v-if="showAdminNavbar" 
      @logout="handleLogout"
    />

    <main class="content-area">
      <RouterView />
    </main>

    <UserFooter v-if="showUserNavbar" />
    
    <AdminFooter v-if="showAdminNavbar" />
  </div>
</template>

<script>
// Component Imports
// Check if your files are inside a 'User' subfolder or just 'components'
import UserNavbar from './components/User/UserNavbar.vue'; 
import UserFooter from './components/User/UserFooter.vue'; // Added /User/ here

import AdminNavbar from './components/Admin/AdminNavbar.vue'; // Check if these need /Admin/
import AdminFooter from './components/Admin/AdminFooter.vue';



export default {
  name: 'App',
  components: { 
    UserNavbar, 
    UserFooter, 
    AdminNavbar, 
    AdminFooter 
  },
  data() {
    return {
    // Check localStorage on load
      isAuthenticated: !!localStorage.getItem('access_token'),
      userRole: localStorage.getItem('is_admin') === 'true' ? 'admin' : 'customer',
      cartCount: 0
    };
  },
  computed: {
    // Checks if the current URL path starts with /admin
    isAdminRoute() {
      return this.$route.path.startsWith('/admin');
    },
    // Checks if the current page is Login or Register
    isAuthPage() {
      return ['/login', '/register'].includes(this.$route.path);
    },
    // Logic for User Layout
    showUserNavbar() {
      return !this.isAdminRoute && !this.isAuthPage;
    },
    // Logic for Admin Layout
    showAdminNavbar() {
      // In a real app, also verify if userRole === 'admin'
      return this.isAdminRoute && !this.isAuthPage;
    }
  },
  methods: {
    handleLogout() {
      console.log("User logged out");
      this.isAuthenticated = false;
      this.userRole = 'guest';
      this.cartCount = 0;
      localStorage.removeItem('token'); // Clear your session
      this.$router.push('/login');
    },
    handleSearch(query) {
      this.$router.push({ path: '/search', query: { q: query } });
    },
    handleCategory(id) {
      this.$router.push({ path: '/shop', query: { category: id } });
    }
  }
}
</script>

<style>
/* Global Layout Styles */
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content-area {
  flex: 1; /* Pushes the footer to the bottom of the screen */
}
</style>