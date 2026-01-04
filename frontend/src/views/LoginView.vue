<template>
  <div class="d-flex flex-column min-vh-100 bg-white">
    <main class="flex-grow-1 d-flex align-items-center position-relative py-5">
      <div class="container px-lg-5">
        <div class="row g-0 shadow-2xl rounded-5 overflow-hidden border border-light">
          
          <div class="col-lg-6 d-none d-lg-block position-relative bg-light">
            <img 
              src="https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?ixlib=rb-4.0.3&auto=format&fit=crop&w=900&q=80" 
              alt="Login Visual" 
              class="w-100 h-100 object-fit-cover position-absolute top-0 start-0"
            >
            <div class="position-absolute top-0 start-0 w-100 h-100 bg-dark opacity-25"></div>
            
            <div class="position-absolute bottom-0 start-0 p-5 text-white z-2">
              <span class="d-block text-uppercase tracking-wide extra-small fw-bold mb-3 opacity-75">Welcome Back</span>
              <h2 class="display-6 fw-bold mb-3 tracking-tight">Curating your daily<br>rituals.</h2>
              <p class="lead fw-normal opacity-90 mb-0 fs-6">
                Sign in to access your wishlist, track orders, and discover new drops.
              </p>
            </div>
          </div>

          <div class="col-lg-6 bg-white p-5 p-md-6">
            <div class="mx-auto" style="max-width: 420px;">
              
              <div class="mb-5 text-center text-lg-start">
                <h1 class="fw-bold tracking-tight mb-2">Log In</h1>
                <p class="text-muted">
                  Don't have an account? 
                  <a href="#" class="text-dark fw-bold text-decoration-underline" @click.prevent="handleNavigation('register')">Sign up</a>
                </p>
              </div>

              <div v-if="error" class="alert alert-danger rounded-0 small py-2 mb-4 border-0" role="alert">
                <i class="bi bi-exclamation-circle me-2"></i> {{ error }}
              </div>

              <form @submit.prevent="handleLogin">
                <div class="mb-4">
                  <label for="email" class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Email Address</label>
                  <input 
                    type="email" 
                    id="email" 
                    class="form-control form-control-lg bg-light border-0 rounded-0 fs-6" 
                    placeholder="name@example.com"
                    v-model="credentials.email"
                    :disabled="loading"
                    required
                  >
                </div>

                <div class="mb-4">
                  <div class="d-flex justify-content-between align-items-center mb-1">
                    <label for="password" class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted mb-0">Password</label>
                    <a href="#" class="extra-small text-muted text-decoration-none hover-dark" @click.prevent="forgotPassword">Forgot?</a>
                  </div>
                  <div class="position-relative">
                    <input 
                      :type="showPassword ? 'text' : 'password'" 
                      id="password" 
                      class="form-control form-control-lg bg-light border-0 rounded-0 fs-6 pe-5" 
                      placeholder="••••••••"
                      v-model="credentials.password"
                      :disabled="loading"
                      required
                    >
                    <button 
                      type="button"
                      class="btn position-absolute top-50 end-0 translate-middle-y text-muted border-0" 
                      @click="showPassword = !showPassword"
                    >
                      <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                    </button>
                  </div>
                </div>

                <div class="mb-4 form-check">
                  <input type="checkbox" class="form-check-input border-secondary rounded-0 cursor-pointer" id="rememberMe" v-model="rememberMe">
                  <label class="form-check-label small text-muted cursor-pointer" for="rememberMe">Remember me</label>
                </div>

                <button 
                  type="submit" 
                  class="btn btn-dark w-100 py-3 rounded-0 text-uppercase fw-bold tracking-wide hover-lift mb-4 d-flex align-items-center justify-content-center"
                  :disabled="loading"
                >
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  {{ loading ? 'Authenticating...' : 'Log In' }}
                </button>
              </form>

              <div class="mt-5 pt-4 border-top border-light d-flex justify-content-between text-center">
                <div class="d-flex flex-column align-items-center gap-1 opacity-50">
                  <i class="bi bi-shield-lock fs-5"></i>
                  <span class="extra-small fw-bold text-uppercase">Secure</span>
                </div>
                <div class="d-flex flex-column align-items-center gap-1 opacity-50">
                  <i class="bi bi-box-seam fs-5"></i>
                  <span class="extra-small fw-bold text-uppercase">Returns</span>
                </div>
                <div class="d-flex flex-column align-items-center gap-1 opacity-50">
                  <i class="bi bi-chat-dots fs-5"></i>
                  <span class="extra-small fw-bold text-uppercase">Support</span>
                </div>
              </div>

            </div>
          </div>

        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';

const router = useRouter();

const credentials = reactive({
  email: '',
  password: ''
});
const rememberMe = ref(false);
const showPassword = ref(false);
const loading = ref(false);
const error = ref(null);

const handleNavigation = (page) => {
  router.push({ name: page });
};

const handleLogin = async () => {
  error.value = null;
  loading.value = true;

  try {
    const response = await api.post('/auth/login', {
      email: credentials.email,
      password: credentials.password
    });

    if (response.data && response.data.access_token) {
      // 1. Store the token
      localStorage.setItem('access_token', response.data.access_token);
      
      // 2. Store the role and user info
      localStorage.setItem('is_admin', response.data.is_admin);
      localStorage.setItem('user', JSON.stringify(response.data.user));

      // 3. ROLE-BASED REDIRECTION
      if (response.data.is_admin === true) {
        // Redirect to Admin Dashboard
        router.push({ name: 'admindashboard' }).then(() => {
            window.location.reload(); // Refresh to let App.vue pick up the new role
        });
      } else {
        // Redirect to User Home
        router.push({ name: 'home' }).then(() => {
            window.location.reload(); // Refresh to let App.vue pick up the new auth state
        });
      }
    }
  } catch (err) {
    console.error('Login Error:', err);
    error.value = err.response?.data?.msg || 'Invalid email or password. Please try again.';
  } finally {
    loading.value = false;
  }
};

const forgotPassword = () => {
  alert("Redirecting to password recovery...");
};
</script>

<style scoped>
/* Shadows & Spacing */
.shadow-2xl { box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.1) !important; }
.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }
.hover-dark:hover { color: #000 !important; }

/* Form Focus */
.form-control:focus {
  background-color: #fff;
  border: 1px solid #000 !important;
  box-shadow: none;
}

/* Hover Effects */
.hover-lift { transition: transform 0.2s ease, box-shadow 0.2s ease; }
.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.cursor-pointer { cursor: pointer; }
.object-fit-cover { object-fit: cover; }

@media (min-width: 992px) {
  .p-md-6 { padding: 4rem; }
}
</style>