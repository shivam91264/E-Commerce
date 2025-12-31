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
                Trust & Safety
              </span>
              <h1 class="display-5 fw-bold tracking-tight mb-2 text-dark">
                Privacy Policy
              </h1>
              <p class="text-muted lead fs-6 mb-0">
                Learn how we collect, use, and protect your personal information.
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
                  <h4 class="fw-bold text-dark mb-4">1. Information We Collect</h4>
                  
                  <div class="row g-4 mb-3">
                    <div class="col-md-6">
                      <div class="p-3 bg-light rounded-3 h-100">
                        <div class="d-flex align-items-center mb-2">
                          <i class="bi bi-person-badge fs-5 text-dark me-2"></i>
                          <h6 class="fw-bold mb-0">Personal Information</h6>
                        </div>
                        <p class="small text-secondary mb-0">
                          Name, email address, shipping address, and phone number provided during checkout.
                        </p>
                      </div>
                    </div>
                    <div class="col-md-6">
                      <div class="p-3 bg-light rounded-3 h-100">
                        <div class="d-flex align-items-center mb-2">
                          <i class="bi bi-credit-card fs-5 text-dark me-2"></i>
                          <h6 class="fw-bold mb-0">Payment Data</h6>
                        </div>
                        <p class="small text-secondary mb-0">
                          Payment details are processed securely by our payment partners. We do not store raw card data.
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <p class="text-secondary leading-relaxed">
                    We also automatically collect certain information about your device, including information about your web browser, IP address, time zone, and some of the cookies that are installed on your device.
                  </p>
                </section>

                <hr class="my-4 text-muted opacity-10">

                <section class="mb-5">
                  <h4 class="fw-bold text-dark mb-3">2. How We Use Your Information</h4>
                  <p class="text-secondary mb-3">We use the Order Information that we collect generally to fulfill any orders placed through the Site. Additionally, we use this information to:</p>
                  <ul class="list-unstyled text-secondary ps-2">
                    <li class="mb-2 position-relative ps-4">
                      <span class="position-absolute top-0 start-0 text-primary">•</span>
                      Communicate with you regarding your order status.
                    </li>
                    <li class="mb-2 position-relative ps-4">
                      <span class="position-absolute top-0 start-0 text-primary">•</span>
                      Screen our orders for potential risk or fraud.
                    </li>
                    <li class="mb-2 position-relative ps-4">
                      <span class="position-absolute top-0 start-0 text-primary">•</span>
                      Provide you with information or advertising relating to our products or services (based on preferences).
                    </li>
                  </ul>
                </section>

                <hr class="my-4 text-muted opacity-10">

                <section class="mb-5">
                  <h4 class="fw-bold text-dark mb-3">3. Cookies & Tracking</h4>
                  <p class="text-secondary leading-relaxed">
                    We use "cookies" to improve your experience on our site. A cookie is a small piece of data sent from a website and stored on the user's computer by the user's web browser while the user is browsing.
                  </p>
                  <p class="text-secondary leading-relaxed">
                    You can instruct your browser to refuse all cookies or to indicate when a cookie is being sent. However, if you do not accept cookies, you may not be able to use some portions of our Service.
                  </p>
                </section>

                <hr class="my-4 text-muted opacity-10">

                <section class="mb-5">
                  <h4 class="fw-bold text-dark mb-3">4. Data Security</h4>
                  <p class="text-secondary leading-relaxed mb-3">
                    The security of your data is important to us, but remember that no method of transmission over the Internet, or method of electronic storage is 100% secure. While we strive to use commercially acceptable means to protect your Personal Data, we cannot guarantee its absolute security.
                  </p>
                  <div class="alert alert-light border border-light d-flex gap-3 align-items-start">
                    <i class="bi bi-shield-lock text-dark fs-4"></i>
                    <div>
                      <h6 class="fw-bold mb-1">SSL Encryption</h6>
                      <p class="mb-0 small text-muted">Our entire website is secured using 256-bit SSL encryption to ensure your data remains private.</p>
                    </div>
                  </div>
                </section>

                 <section class="mb-5">
                  <h4 class="fw-bold text-dark mb-3">5. Your Rights</h4>
                  <p class="text-secondary leading-relaxed">
                    If you are a European resident, you have the right to access personal information we hold about you and to ask that your personal information be corrected, updated, or deleted. If you would like to exercise this right, please contact us through the contact information below.
                  </p>
                </section>

                <section class="bg-dark text-white rounded-3 p-4 text-center text-md-start d-flex flex-column flex-md-row align-items-center justify-content-between gap-3 shadow-sm">
                  <div>
                    <h5 class="fw-bold mb-1">Privacy Concerns?</h5>
                    <p class="text-white-50 small mb-0">Contact our Data Protection Officer.</p>
                  </div>
                  <button class="btn btn-white text-dark rounded-pill px-4 py-2 text-uppercase fw-bold extra-small tracking-wide">
                    Email Support
                  </button>
                </section>

              </div>
            </div>

            <div class="text-center mt-4">
               <p class="text-muted small">
                 Last updated: December 31, 2025
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
  name: "PrivacyView",
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

/* Button override for the footer CTA */
.btn-white {
  background-color: white;
  border: 1px solid white;
}
.btn-white:hover {
  background-color: #f8f9fa;
  border-color: #f8f9fa;
}
</style>