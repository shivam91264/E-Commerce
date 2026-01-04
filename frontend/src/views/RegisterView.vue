<template>
  <div class="d-flex flex-column min-vh-100 bg-white">
    
    <main class="flex-grow-1 d-flex align-items-center position-relative py-5">
      <div class="container px-lg-5">
        <div class="row g-0 shadow-2xl rounded-5 overflow-hidden border border-light">
          
          <div class="col-lg-6 d-none d-lg-block position-relative bg-light">
            <img 
              src="https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" 
              alt="Join MarketHub" 
              class="w-100 h-100 object-fit-cover position-absolute top-0 start-0"
            >
            <div class="position-absolute top-0 start-0 w-100 h-100 bg-black opacity-20"></div>
            
            <div class="position-absolute bottom-0 start-0 p-5 text-white z-2">
              <span class="d-block text-uppercase tracking-wide extra-small fw-bold mb-3 opacity-75">Join the Community</span>
              <h2 class="display-6 fw-bold mb-3 tracking-tight">Design for <br>modern living.</h2>
              <p class="lead fw-normal opacity-90 mb-0 fs-6">
                Create an account to unlock exclusive access to new arrivals, curated lists, and seamless checkout.
              </p>
            </div>
          </div>

          <div class="col-lg-6 bg-white p-5 p-md-6">
            <div class="mx-auto" style="max-width: 440px;">
              
              <div class="mb-5 text-center text-lg-start">
                <h1 class="fw-bold tracking-tight mb-2">Create Account</h1>
                <p class="text-muted">
                  Already a member? 
                  <a href="#" class="text-dark fw-bold text-decoration-underline" @click.prevent="handleNavigation('login')">Log in</a>
                </p>
              </div>

              <div v-if="errorMessage" class="alert alert-danger d-flex align-items-center rounded-0 border-0 small mb-4" role="alert">
                <i class="bi bi-exclamation-triangle-fill me-2"></i>
                <div>{{ errorMessage }}</div>
              </div>

              <form @submit.prevent="handleRegister">
                
                <div class="mb-4">
                  <label for="fullname" class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Full Name</label>
                  <input 
                    type="text" 
                    id="fullname" 
                    class="form-control form-control-lg bg-light border-0 rounded-0 fs-6" 
                    placeholder="e.g. Alex Morgan"
                    v-model="formData.full_name"
                    required
                  >
                </div>

                <div class="mb-4">
                  <label for="email" class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Email Address</label>
                  <input 
                    type="email" 
                    id="email" 
                    class="form-control form-control-lg bg-light border-0 rounded-0 fs-6" 
                    placeholder="name@example.com"
                    v-model="formData.email"
                    required
                  >
                </div>

                <div class="mb-4">
                  <label for="phone" class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Phone Number</label>
                  <input 
                    type="tel" 
                    id="phone" 
                    class="form-control form-control-lg bg-light border-0 rounded-0 fs-6" 
                    placeholder="e.g. 9876543210"
                    v-model="formData.phone"
                    required
                  >
                </div>

                <div class="row g-3 mb-4">
                  <div class="col-md-6">
                    <label for="password" class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Password</label>
                    <div class="position-relative">
                      <input 
                        :type="showPassword ? 'text' : 'password'" 
                        id="password" 
                        class="form-control form-control-lg bg-light border-0 rounded-0 fs-6 pe-5" 
                        placeholder="Min. 8 chars"
                        v-model="formData.password"
                        required
                        minlength="8"
                      >
                    </div>
                  </div>
                  <div class="col-md-6">
                    <label for="confirmPassword" class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Confirm</label>
                    <div class="position-relative">
                      <input 
                        :type="showPassword ? 'text' : 'password'" 
                        id="confirmPassword" 
                        class="form-control form-control-lg bg-light border-0 rounded-0 fs-6 pe-5" 
                        placeholder="Repeat password"
                        v-model="formData.confirmPassword"
                        required
                      >
                      <button 
                        type="button"
                        class="btn position-absolute top-50 end-0 translate-middle-y text-muted border-0" 
                        @click="showPassword = !showPassword"
                        tabindex="-1"
                      >
                        <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                      </button>
                    </div>
                  </div>
                </div>

                <div class="mb-4 form-check">
                  <input type="checkbox" class="form-check-input border-secondary rounded-0 cursor-pointer" id="agreeTerms" v-model="formData.agreeTerms" required>
                  <label class="form-check-label small text-muted cursor-pointer" for="agreeTerms">
                    I agree to the <a href="#" class="text-dark text-decoration-underline">Terms of Service</a> and <a href="#" class="text-dark text-decoration-underline">Privacy Policy</a>.
                  </label>
                </div>

                <button 
                  type="submit" 
                  class="btn btn-dark w-100 py-3 rounded-0 text-uppercase fw-bold tracking-wide hover-lift mb-4 d-flex align-items-center justify-content-center"
                  :disabled="isLoading"
                >
                  <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  {{ isLoading ? 'Creating Account...' : 'Create Account' }}
                </button>

                <div class="d-flex align-items-center mb-4">
                  <hr class="flex-grow-1 border-secondary opacity-10">
                  <span class="mx-3 extra-small text-muted text-uppercase">Or register with</span>
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
                  <i class="bi bi-stars fs-5"></i>
                  <span class="extra-small fw-bold text-uppercase">Rewards</span>
                </div>
                <div class="d-flex flex-column align-items-center gap-1 opacity-50">
                  <i class="bi bi-lightning-charge fs-5"></i>
                  <span class="extra-small fw-bold text-uppercase">Early Access</span>
                </div>
                <div class="d-flex flex-column align-items-center gap-1 opacity-50">
                  <i class="bi bi-person-check fs-5"></i>
                  <span class="extra-small fw-bold text-uppercase">Verified</span>
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

// Form States
const formData = reactive({
  full_name: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: '',
  agreeTerms: false
});

const showPassword = ref(false);
const isLoading = ref(false);
const errorMessage = ref('');

// Logic
const handleNavigation = (page) => {
  router.push({ name: page });
};

const handleRegister = async () => {
  // 1. Reset States
  errorMessage.value = '';
  
  // 2. Client-side Validation
  if (formData.password !== formData.confirmPassword) {
    errorMessage.value = "Passwords do not match.";
    return;
  }

  if (!formData.agreeTerms) {
    errorMessage.value = "You must agree to the Terms of Service.";
    return;
  }

  // 3. API Call
  isLoading.ref = true;
  try {
    const response = await api.post('/auth/register', {
      full_name: formData.full_name,
      email: formData.email,
      password: formData.password,
      phone: formData.phone
    });

    // 4. Success Handling
    // If your API returns a token immediately upon registration
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
      
      // Store user info if returned
      if (response.data.user) {
        localStorage.setItem('user', JSON.stringify(response.data.user));
      }

      // Redirect to Home/Dashboard
      router.push({ name: 'Home' });
    } else {
      // If API requires separate login after registration
      alert("Registration successful! Please log in.");
      router.push({ name: 'login' });
    }
    
  } catch (error) {
    // 5. Error Handling
    console.error("Registration Error:", error);
    errorMessage.value = error.response?.data?.message || "An error occurred during registration. Please try again.";
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* PREMIUM VISUAL LANGUAGE */

.shadow-2xl {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.1) !important;
}

.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }

.form-control:focus {
  background-color: #fff;
  border: 1px solid #000 !important;
  box-shadow: none;
}

.hover-border-dark:hover {
  border-color: #000 !important;
  background-color: #f8f9fa;
}

.cursor-pointer { cursor: pointer; }

.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

@media (min-width: 992px) {
  .p-md-6 { padding: 4rem; }
}

.object-fit-cover { object-fit: cover; }
</style>