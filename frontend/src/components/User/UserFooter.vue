<template>
  <footer class="premium-footer text-white pt-5 pb-4">
    <div class="container px-lg-5">
      
      <div class="row g-5 mb-5">
        
        <div class="col-lg-4 col-md-12">
          <a class="navbar-brand fw-bold tracking-tight text-white fs-3 mb-3 d-block" href="#">
            MARKETHUB<span class="text-primary">.</span>
          </a>
          <p class="text-white-50 mb-4 small" style="max-width: 300px; line-height: 1.6;">
            Elevating your everyday with curated essentials. Quality, sustainability, and design in every detail.
          </p>
          <div class="d-flex gap-3 social-icons">
            <a v-for="icon in socialIcons" :key="icon.name" href="#" class="rounded-circle bg-white bg-opacity-10 d-flex align-items-center justify-content-center text-white text-decoration-none transition-all">
              <i :class="icon.class"></i>
            </a>
          </div>
        </div>

        <div class="col-lg-2 col-md-4 col-6">
          <h6 class="fw-bold mb-4 tracking-wide text-uppercase extra-small text-white">Shop</h6>
          <ul class="list-unstyled d-flex flex-column gap-2">
            <li v-for="link in shopLinks" :key="link.text">
              <a href="#" class="footer-link text-white-50" @click.prevent="$emit('navigate', link.action)">
                {{ link.text }}
              </a>
            </li>
          </ul>
        </div>

        <div class="col-lg-2 col-md-4 col-6">
          <h6 class="fw-bold mb-4 tracking-wide text-uppercase extra-small text-white">Support</h6>
          <ul class="list-unstyled d-flex flex-column gap-2">
            <li v-for="link in supportLinks" :key="link.text">
              <a href="#" class="footer-link text-white-50" @click.prevent="$emit('navigate', link.action)">
                {{ link.text }}
              </a>
            </li>
          </ul>
        </div>

        <div class="col-lg-4 col-md-4">
          <h6 class="fw-bold mb-4 tracking-wide text-uppercase extra-small text-white">Stay in the loop</h6>
          <p class="text-white-50 small mb-3">Subscribe to receive exclusive offers and updates.</p>
          
          <form @submit.prevent="handleSubscribe" class="position-relative mt-2">
            <input 
              type="email" 
              class="form-control bg-transparent border-bottom border-secondary border-opacity-75 text-white rounded-0 ps-0 pe-5 py-2 shadow-none placeholder-light" 
              placeholder="Enter your email"
              v-model="email"
              required
            >
            <button class="btn p-0 position-absolute top-50 end-0 translate-middle-y text-white" type="submit">
              <i class="bi bi-arrow-right fs-5"></i>
            </button>
          </form>
        </div>

      </div>

      <div class="border-top border-secondary border-opacity-25 pt-4">
        <div class="row align-items-center">
          <div class="col-md-6 text-center text-md-start mb-3 mb-md-0">
            <p class="mb-0 text-white-50 extra-small">
              &copy; {{ new Date().getFullYear() }} MarketHub Inc. All rights reserved.
            </p>
          </div>
          <div class="col-md-6 text-center text-md-end">
            <div class="d-flex gap-3 justify-content-center justify-content-md-end opacity-50 text-white">
              <i class="bi bi-credit-card-2-front fs-5"></i>
              <i class="bi bi-paypal fs-5"></i>
              <i class="bi bi-apple fs-5"></i>
            </div>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: "PremiumFooter",
  data() {
    return {
      email: "",
      shopLinks: [
        { text: "New Arrivals", action: "new" },
        { text: "Best Sellers", action: "best-sellers" },
        { text: "Home & Living", action: "home" },
        { text: "Accessories", action: "accessories" }
      ],
      supportLinks: [
        { text: "Order Status", action: "orders" },
        { text: "Shipping & Returns", action: "shipping" },
        { text: "FAQ", action: "faq" },
        { text: "Privacy Policy", action: "privacy" }
      ],
      socialIcons: [
        { name: "Instagram", class: "bi bi-instagram" },
        { name: "Twitter", class: "bi bi-twitter-x" },
        { name: "Facebook", class: "bi bi-facebook" }
      ]
    };
  },
  methods: {
    handleSubscribe() {
      if (this.email) {
        alert(`Subscribed: ${this.email}`);
        this.email = "";
      }
    }
  }
};
</script>

<style scoped>
.premium-footer {
  background-color: #111111;
  font-family: 'Inter', system-ui, sans-serif;
}
.tracking-tight { letter-spacing: -0.03em; }
.tracking-wide { letter-spacing: 0.1em; }
.extra-small { font-size: 0.75rem; }

.footer-link {
  text-decoration: none;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  display: inline-block;
}
.footer-link:hover {
  color: #fff !important;
  transform: translateX(5px);
}

/* Fix input placeholder color */
.placeholder-light::placeholder {
  color: rgba(255,255,255,0.5);
}

.social-icons a { width: 36px; height: 36px; }
.social-icons a:hover {
  background-color: #fff !important;
  color: #000 !important;
  transform: translateY(-3px);
}
</style>