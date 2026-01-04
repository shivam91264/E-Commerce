<template>
  <div class="d-flex flex-column min-vh-100 bg-white">
    
    <PremiumNavbar 
      :is-authenticated="false" 
      :cart-item-count="0" 
      user-role="guest"
      @navigate="handleNavigation"
    />

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

                <div class="d-flex align-items-center mb-4">
                  <hr class="flex-grow-1 border-secondary opacity-10">
                  <span class="mx-3 extra-small text-muted text-uppercase">Or continue with</span>
                  <hr class="flex-grow-1 border-secondary opacity-10">
                </div>

                <div class="row g-2">
                  <div class="col-6">
                    <button type="button" class="btn btn-outline-light border-secondary-subtle text-dark w-100 py-2 rounded-0 d-flex align-items-center justify-content-center gap-2 hover-border-dark">
                      <i class="bi bi-google"></i> <span class="small fw-medium">Google</span>
                    </button>
                  </div>
                  <div class="col-6">
                    <button type="button" class="btn btn-outline-light border-secondary-subtle text-dark w-100 py-2 rounded-0 d-flex align-items-center justify-content-center gap-2 hover-border-dark">
                      <i class="bi bi-apple"></i> <span class="small fw-medium">Apple</span>
                    </button>
                  </div>
                </div>

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

    <PremiumFooter @navigate="handleNavigation" />

  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';
import PremiumNavbar from '@/components/Navbar.vue';
import PremiumFooter from '@/components/Footer.vue';

// Router instance for navigation
const router = useRouter();

// Form and UI state
const credentials = reactive({
  email: '',
  password: ''
});
const rememberMe = ref(false);
const showPassword = ref(false);
const loading = ref(false);
const error = ref(null);

/**
 * Handle page navigation
 */
const handleNavigation = (page) => {
  router.push({ name: page });
};

/**
 * Perform login API request
 */
const handleLogin = async () => {
  error.value = null;
  loading.value = true;

  try {
    const response = await api.post('/auth/login', {
      email: credentials.email,
      password: credentials.password
    });

    // Handle successful login
    if (response.data && response.data.access_token) {
      // Store JWT token
      localStorage.setItem('access_token', response.data.access_token);
      
      // Store user info if provided by the backend
      if (response.data.user) {
        localStorage.setItem('user', JSON.stringify(response.data.user));
      }

      // Redirect to home/dashboard
      router.push({ name: 'home' });
    }
  } catch (err) {
    // Handle error responses from Flask
    console.error('Login Error:', err);
    error.value = err.response?.data?.message || 'Invalid email or password. Please try again.';
  } finally {
    loading.value = false;
  }
};

/**
 * Trigger password recovery alert
 */
const forgotPassword = () => {
  alert("Redirecting to password recovery...");
};
</script>

<style scoped>
/* PREMIUM DESIGN SYSTEM */

/* Layout & Shadows */
.shadow-2xl {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.1) !important;
}

/* Typography */
.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }
.hover-dark:hover { color: #000 !important; }

/* Form Elements */
.form-control:focus {
  background-color: #fff;
  border: 1px solid #000 !important;
  box-shadow: none;
}

.hover-border-dark:hover {
  border-color: #000 !important;
  background-color: #f8f9fa;
}

/* Animations & Interactions */
.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.cursor-pointer { cursor: pointer; }

/* Responsive Adjustments */
@media (min-width: 992px) {
  .p-md-6 { padding: 4rem; }
}

/* Image styling */
.object-fit-cover { object-fit: cover; }
</style>