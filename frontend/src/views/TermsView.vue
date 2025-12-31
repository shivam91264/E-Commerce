<template>
  <div class="d-flex flex-column min-vh-100 bg-light-subtle">
    
    <PremiumNavbar 
      :is-authenticated="false" 
      :cart-item-count="0" 
      user-role="guest"
    />

    <main class="flex-grow-1">
      
      <header class="bg-white pt-5 pb-4 border-bottom border-light">
        <div class="container px-lg-5">
          <div class="row justify-content-center">
            <div class="col-12 col-lg-10 col-xl-8 text-center text-md-start animate-fade-up">
              <span class="d-block text-muted extra-small text-uppercase tracking-wide fw-bold mb-2">
                Legal Information
              </span>
              <h1 class="display-5 fw-bold tracking-tight mb-2 text-dark">
                Terms & Conditions
              </h1>
              <p class="text-muted lead fs-6 mb-0">
                Last Updated: <span class="text-dark fw-medium">December 31, 2025</span>
              </p>
            </div>
          </div>
        </div>
      </header>

      <div class="container px-lg-5 py-5">
        <div class="row justify-content-center">
          <div class="col-12 col-lg-10 col-xl-8">
            
            <div class="card border-0 shadow-sm rounded-4 animate-fade-up" style="animation-delay: 0.1s;">
              <div class="card-body p-4 p-md-5">
                
                <section class="mb-5">
                  <h4 class="fw-bold text-dark mb-3">1. Introduction</h4>
                  <p class="text-secondary leading-relaxed">
                    Welcome to <strong>MarketHub</strong>. By accessing our website and using our services, you agree to be bound by the following terms and conditions. Please read them carefully. If you do not agree with any part of these terms, you must discontinue use of our platform immediately.
                  </p>
                  <p class="text-secondary leading-relaxed">
                    These terms apply to all visitors, users, and others who wish to access or use the Service.
                  </p>
                </section>

                <hr class="my-4 text-muted opacity-10">

                <section class="mb-5">
                  <h4 class="fw-bold text-dark mb-3">2. Eligibility & Responsibilities</h4>
                  <ul class="list-unstyled d-flex flex-column gap-2 text-secondary">
                    <li class="d-flex align-items-start">
                      <i class="bi bi-check2 text-dark me-2 mt-1"></i>
                      <span>You must be at least <strong>18 years old</strong> to create an account or place an order.</span>
                    </li>
                    <li class="d-flex align-items-start">
                      <i class="bi bi-check2 text-dark me-2 mt-1"></i>
                      <span>You agree to provide accurate, current, and complete information during the registration process.</span>
                    </li>
                    <li class="d-flex align-items-start">
                      <i class="bi bi-check2 text-dark me-2 mt-1"></i>
                      <span>You are responsible for safeguarding the password that you use to access the Service and for any activities or actions under your password.</span>
                    </li>
                  </ul>
                </section>

                <hr class="my-4 text-muted opacity-10">

                <section class="mb-5">
                  <h4 class="fw-bold text-dark mb-3">3. Products & Pricing</h4>
                  <p class="text-secondary leading-relaxed mb-3">
                    We strive to display accurate price information, however, we may, on occasion, make inadvertent typographical errors, inaccuracies, or omissions related to pricing and availability. We reserve the right to correct any errors, inaccuracies, or omissions at any time.
                  </p>
                  <div class="bg-light p-3 rounded-3 border border-light">
                    <p class="mb-0 small text-muted">
                      <strong class="text-dark">Note:</strong> Prices are subject to change without notice. All prices are listed in USD unless stated otherwise.
                    </p>
                  </div>
                </section>

                <hr class="my-4 text-muted opacity-10">

                <section class="mb-5">
                  <h4 class="fw-bold text-dark mb-3">4. Prohibited Activities</h4>
                  <p class="text-secondary mb-3">You agree not to engage in any of the following activities:</p>
                  <ul class="list-unstyled text-secondary ps-2">
                    <li class="mb-2 position-relative ps-4">
                      <span class="position-absolute top-0 start-0 text-dark">•</span>
                      Using the service for any illegal purpose or in violation of any local, state, national, or international law.
                    </li>
                    <li class="mb-2 position-relative ps-4">
                      <span class="position-absolute top-0 start-0 text-dark">•</span>
                      Attempting to interfere with, compromise the system integrity or security, or decipher any transmissions to or from the servers running the Service.
                    </li>
                    <li class="mb-2 position-relative ps-4">
                      <span class="position-absolute top-0 start-0 text-dark">•</span>
                      Copying, distributing, or disclosing any part of the Service in any medium, including without limitation by any automated or non-automated "scraping".
                    </li>
                  </ul>
                </section>

                <hr class="my-4 text-muted opacity-10">

                <section class="mb-5">
                  <h4 class="fw-bold text-dark mb-3">5. Limitation of Liability</h4>
                  <p class="text-secondary leading-relaxed">
                    In no event shall MarketHub, nor its directors, employees, partners, agents, suppliers, or affiliates, be liable for any indirect, incidental, special, consequential or punitive damages, including without limitation, loss of profits, data, use, goodwill, or other intangible losses, resulting from your access to or use of or inability to access or use the Service.
                  </p>
                </section>

                <section class="bg-light-subtle rounded-3 p-4 border border-light text-center text-md-start d-flex flex-column flex-md-row align-items-center justify-content-between gap-3">
                  <div>
                    <h5 class="fw-bold text-dark mb-1">Have questions about our Terms?</h5>
                    <p class="text-muted small mb-0">Our support team is available to clarify any points.</p>
                  </div>
                  <button class="btn btn-dark rounded-pill px-4 py-2 text-uppercase fw-bold extra-small tracking-wide">
                    Contact Us
                  </button>
                </section>

              </div>
            </div>

            <div class="text-center mt-4">
               <p class="text-muted small">
                 &copy; 2025 MarketHub Inc. All rights reserved.
               </p>
            </div>

          </div>
        </div>
      </div>
    </main>

    <PremiumFooter />

  </div>
</template>

<script>
import PremiumNavbar from '@/components/Navbar.vue';
import PremiumFooter from '@/components/Footer.vue';

export default {
  name: "TermsView",
  components: {
    PremiumNavbar,
    PremiumFooter
  }
};
</script>

<style scoped>
/* 🎨 Typography & Spacing */
.leading-relaxed {
  line-height: 1.8;
}

.extra-small {
  font-size: 0.75rem;
}

.tracking-wide {
  letter-spacing: 0.1em;
}

.bg-light-subtle {
  background-color: #f9fafb !important;
}

/* 🔄 Animations */
.animate-fade-up {
  animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
  transform: translateY(20px);
}

@keyframes fadeUp {
  to { opacity: 1; transform: translateY(0); }
}
</style>