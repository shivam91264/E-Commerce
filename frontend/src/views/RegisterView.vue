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

              <form @submit.prevent="handleRegister">
                
                <div class="mb-4">
                  <label for="fullname" class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Full Name</label>
                  <input 
                    type="text" 
                    id="fullname" 
                    class="form-control form-control-lg bg-light border-0 rounded-0 fs-6" 
                    placeholder="e.g. Alex Morgan"
                    v-model="fullname"
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
                    v-model="email"
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
                        v-model="password"
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
                        v-model="confirmPassword"
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
                  <input type="checkbox" class="form-check-input border-secondary rounded-0 cursor-pointer" id="agreeTerms" v-model="agreeTerms" required>
                  <label class="form-check-label small text-muted cursor-pointer" for="agreeTerms">
                    I agree to the <a href="#" class="text-dark text-decoration-underline">Terms of Service</a> and <a href="#" class="text-dark text-decoration-underline">Privacy Policy</a>.
                  </label>
                </div>

                <button type="submit" class="btn btn-dark w-100 py-3 rounded-0 text-uppercase fw-bold tracking-wide hover-lift mb-4">
                  Create Account
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

    <PremiumFooter @navigate="handleNavigation" />

  </div>
</template>

<script>
import PremiumNavbar from '@/components/Navbar.vue';
import PremiumFooter from '@/components/Footer.vue';

export default {
  name: "RegisterView",
  components: {
    PremiumNavbar,
    PremiumFooter
  },
  data() {
    return {
      fullname: "",
      email: "",
      password: "",
      confirmPassword: "",
      showPassword: false,
      agreeTerms: false
    };
  },
  methods: {
    handleNavigation(page) {
      console.log(`Navigating to: ${page}`);
      // this.$router.push({ name: page });
    },
    handleRegister() {
      // Basic UI Validation logic
      if (this.password !== this.confirmPassword) {
        alert("Passwords do not match.");
        return;
      }
      
      if (this.agreeTerms) {
        console.log("Registering...", { 
          name: this.fullname, 
          email: this.email 
        });
        
        // Simulate API delay
        setTimeout(() => {
          alert(`Account created for ${this.fullname}! Please log in.`);
          this.handleNavigation('login');
        }, 500);
      }
    }
  }
};
</script>

<style scoped>
/* PREMIUM VISUAL LANGUAGE 
   Reusing the system defined in LoginView.vue for consistency.
*/

/* Layout & Shadows */
.shadow-2xl {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.1) !important;
}

/* Typography */
.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }

/* Form Elements */
/* Using borderless inputs with light background for a modern feel */
.form-control:focus {
  background-color: #fff;
  border: 1px solid #000 !important; /* Minimal focus ring */
  box-shadow: none;
}

.hover-border-dark:hover {
  border-color: #000 !important;
  background-color: #f8f9fa;
}

.cursor-pointer { cursor: pointer; }

/* Animations & Interactions */
.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* Responsive Adjustments */
@media (min-width: 992px) {
  .p-md-6 { padding: 4rem; }
}

/* Image styling */
.object-fit-cover { object-fit: cover; }
</style>