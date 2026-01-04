<template>
  <div class="d-flex flex-column min-vh-100 bg-light-subtle">
    
    <main class="flex-grow-1 py-5">
      <div class="container px-lg-5">
        
        <div class="row justify-content-center justify-content-lg-start mb-5 animate-fade-up">
          <div class="col-12 col-lg-8 text-center text-lg-start">
            <span class="d-inline-block border border-dark border-opacity-10 px-3 py-1 rounded-pill text-uppercase tracking-wide extra-small fw-bold mb-3 text-muted">
              Support Center
            </span>
            <h1 class="display-5 fw-bold tracking-tight mb-3">How can we help?</h1>
            <p class="text-muted lead fs-6 mb-0" style="max-width: 600px;">
              We’re here to help. Reach out anytime and we’ll get back to you as soon as possible.
            </p>
          </div>
        </div>

        <div class="row g-4 mb-5 pb-lg-3">
          
          <div class="col-md-4 animate-fade-up delay-100">
            <div class="card h-100 border-0 shadow-sm rounded-4 p-4 text-center hover-lift transition-all">
              <div class="mb-3 d-inline-flex align-items-center justify-content-center bg-light rounded-circle text-dark" style="width: 56px; height: 56px;">
                <i class="bi bi-envelope fs-4"></i>
              </div>
              <h5 class="fw-bold mb-2">Email Us</h5>
              <p class="text-muted small mb-4">For general inquiries and support.</p>
              <a href="mailto:support@markethub.com" class="btn btn-outline-dark rounded-pill px-4 fw-bold text-uppercase extra-small tracking-wide w-100">
                support@markethub.com
              </a>
            </div>
          </div>

          <div class="col-md-4 animate-fade-up delay-200">
            <div class="card h-100 border-0 shadow-sm rounded-4 p-4 text-center hover-lift transition-all">
              <div class="mb-3 d-inline-flex align-items-center justify-content-center bg-light rounded-circle text-dark" style="width: 56px; height: 56px;">
                <i class="bi bi-telephone fs-4"></i>
              </div>
              <h5 class="fw-bold mb-2">Call Us</h5>
              <p class="text-muted small mb-4">Mon–Sat, 10AM–6PM EST</p>
              <a href="tel:+15551234567" class="btn btn-outline-dark rounded-pill px-4 fw-bold text-uppercase extra-small tracking-wide w-100">
                +1 (555) 123-4567
              </a>
            </div>
          </div>

          <div class="col-md-4 animate-fade-up delay-300">
            <div class="card h-100 border-0 shadow-sm rounded-4 p-4 text-center hover-lift transition-all">
              <div class="mb-3 d-inline-flex align-items-center justify-content-center bg-light rounded-circle text-dark" style="width: 56px; height: 56px;">
                <i class="bi bi-chat-text fs-4"></i>
              </div>
              <h5 class="fw-bold mb-2">Live Chat</h5>
              <p class="text-muted small mb-4">Get instant responses from our team.</p>
              <button class="btn btn-dark rounded-pill px-4 fw-bold text-uppercase extra-small tracking-wide w-100 hover-lift">
                Start Chat
              </button>
            </div>
          </div>

        </div>

        <div class="row g-5">
          
          <div class="col-lg-7 animate-fade-up delay-100">
            <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
              <div class="card-header bg-white p-4 border-bottom border-light-subtle">
                <h5 class="fw-bold mb-0">Send us a message</h5>
              </div>
              <div class="card-body p-4 p-lg-5">
                <form @submit.prevent="submitForm">
                  <div class="row g-4">
                    <div class="col-md-6">
                      <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Full Name</label>
                      <input type="text" class="form-control bg-light border-0 rounded-1" v-model="form.name" required placeholder="Alex Morgan">
                    </div>
                    <div class="col-md-6">
                      <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Email Address</label>
                      <input type="email" class="form-control bg-light border-0 rounded-1" v-model="form.email" required placeholder="alex@example.com">
                    </div>
                    <div class="col-12">
                      <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Subject (Optional)</label>
                      <input type="text" class="form-control bg-light border-0 rounded-1" v-model="form.subject" placeholder="e.g. Order Status">
                    </div>
                    <div class="col-12">
                      <label class="form-label extra-small text-uppercase tracking-wide fw-bold text-muted">Message</label>
                      <textarea class="form-control bg-light border-0 rounded-1" rows="5" v-model="form.message" required placeholder="How can we help you today?"></textarea>
                    </div>
                    <div class="col-12 pt-2">
                      <button type="submit" class="btn btn-dark rounded-pill px-5 py-3 fw-bold text-uppercase extra-small tracking-wide hover-lift w-100 w-md-auto">
                        Submit Message
                      </button>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>

          <div class="col-lg-5 animate-fade-up delay-200">
            <div class="ps-lg-4">
              <h5 class="fw-bold mb-4">Frequently Asked Questions</h5>
              
              <div class="accordion accordion-flush" id="faqAccordion">
                
                <div class="accordion-item bg-transparent border-bottom border-dark border-opacity-10" v-for="(faq, index) in faqs" :key="index">
                  <h2 class="accordion-header">
                    <button 
                      class="accordion-button collapsed bg-transparent shadow-none px-0 py-4 fw-bold text-dark" 
                      type="button" 
                      data-bs-toggle="collapse" 
                      :data-bs-target="'#faq'+index"
                    >
                      {{ faq.question }}
                    </button>
                  </h2>
                  <div :id="'faq'+index" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                    <div class="accordion-body px-0 pb-4 text-muted small lh-lg">
                      {{ faq.answer }}
                    </div>
                  </div>
                </div>

              </div>

              <div class="mt-5 p-4 bg-white border rounded-4 text-center">
                 <p class="small text-muted mb-3">Can't find what you're looking for?</p>
                 <a href="#" class="text-dark fw-bold text-decoration-underline extra-small text-uppercase tracking-wide">Visit Help Center</a>
              </div>

            </div>
          </div>

        </div>

      </div>
    </main>

  </div>
</template>

<script>

export default {
  name: "ContactView",
  data() {
    return {
      form: {
        name: "",
        email: "",
        subject: "",
        message: ""
      },
      faqs: [
        {
          question: "How do I track my order?",
          answer: "Once your order ships, you will receive a confirmation email with a tracking number. You can also track the status in your Order History page."
        },
        {
          question: "What is your return policy?",
          answer: "We accept returns within 30 days of delivery. Items must be unused and in original packaging. Visit our Returns page to initiate a request."
        },
        {
          question: "Do you ship internationally?",
          answer: "Yes, we ship to select countries worldwide. Shipping costs and delivery times vary by location and are calculated at checkout."
        },
        {
          question: "How can I change my shipping address?",
          answer: "If your order hasn't shipped yet, please contact our support team immediately. You can also manage saved addresses in your Profile."
        }
      ]
    };
  },
  methods: {
    handleNavigation(page) {
      console.log(`Navigating to: ${page}`);
      // this.$router.push({ name: page });
    },
    submitForm() {
      // Dummy UI Submission
      console.log("Submitting form:", this.form);
      alert(`Thanks, ${this.form.name}! We've received your message.`);
      this.form = { name: "", email: "", subject: "", message: "" }; // Reset
    }
  }
};
</script>

<style scoped>
/* PREMIUM VISUAL LANGUAGE */

/* Background */
.bg-light-subtle { background-color: #f9fafb !important; }

/* Typography */
.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }

/* Transitions & Animations */
.transition-all { transition: all 0.2s ease; }

.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.hover-lift:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.05) !important;
}

.animate-fade-up {
  animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
  transform: translateY(20px);
}
.delay-100 { animation-delay: 0.1s; }
.delay-200 { animation-delay: 0.2s; }
.delay-300 { animation-delay: 0.3s; }

@keyframes fadeUp {
  to { opacity: 1; transform: translateY(0); }
}

/* Form Styling */
.form-control:focus {
  background-color: #fff;
  border: 1px solid #000 !important;
  box-shadow: none;
}

/* Accordion Customization (Clean/Minimal) */
.accordion-button:not(.collapsed) {
  background-color: transparent;
  color: #000;
  box-shadow: none;
}
.accordion-button:focus {
  box-shadow: none;
  border-color: transparent;
}
.accordion-button::after {
  background-size: 0.8rem;
  opacity: 0.5;
}
.accordion-item:last-child {
  border-bottom: 0 !important;
}
</style>