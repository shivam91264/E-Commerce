<template>
  <div class="home-wrapper">
    
    <PremiumNavbar 
      :is-authenticated="isAuthenticated"
      :cart-item-count="cartCount"
      user-role="customer"
      @navigate="handleNavigation"
      @logout="handleLogout"
      @search="handleSearch"
      @filter-category="handleCategory"
    />

    <main>

      <section class="hero-section position-relative d-flex align-items-center">
        <div class="container-fluid px-lg-5">
          <div class="row align-items-center flex-lg-row-reverse g-5">
            
            <div class="col-lg-6 position-relative animate-fade-in">
              <div class="image-wrapper rounded-5 overflow-hidden shadow-xl">
                <img 
                  src="https://images.unsplash.com/photo-1441986300917-64674bd600d8?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80" 
                  alt="New Season Collection" 
                  class="img-fluid w-100 object-fit-cover"
                  style="min-height: 500px;"
                >
              </div>
            </div>

            <div class="col-lg-6 text-center text-lg-start animate-slide-up">
              <span class="badge bg-light text-dark border rounded-pill px-3 py-2 mb-4 text-uppercase tracking-wide fw-bold">
                Spring Collection 2025
              </span>
              <h1 class="display-3 fw-bolder mb-4 lh-sm text-balance">
                Elevate Your <br>
                <span class="text-gradient">Everyday Rituals.</span>
              </h1>
              <p class="lead text-muted mb-5 fw-normal" style="max-width: 550px; margin: 0 auto 0 0;">
                Discover our curated selection of premium essentials. 
                Designed for longevity, crafted for the modern lifestyle.
              </p>
              <div class="d-flex gap-3 justify-content-center justify-content-lg-start">
                <button class="btn btn-dark btn-lg rounded-pill px-5 py-3 fw-semibold shadow-hover" @click="handleNavigation('shop')">
                  Shop New Arrivals
                </button>
                <button class="btn btn-outline-dark btn-lg rounded-pill px-5 py-3 fw-semibold" @click="handleNavigation('about')">
                  Our Story
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="py-6 bg-surface">
        <div class="container px-lg-5">
          <div class="d-flex justify-content-between align-items-end mb-5">
            <h2 class="fw-bold mb-0">Curated Collections</h2>
            <a href="#" class="btn-link-dark fw-bold text-decoration-none">View All</a>
          </div>

          <div class="row g-4">
            <div v-for="cat in categories" :key="cat.id" class="col-md-6 col-lg-3">
              <div class="card category-card border-0 text-white rounded-4 overflow-hidden h-100 cursor-pointer" @click="handleCategory(cat.id)">
                <img :src="cat.image" class="card-img h-100 object-fit-cover transition-scale" :alt="cat.name">
                <div class="card-img-overlay d-flex align-items-end p-4 gradient-overlay">
                  <div>
                    <h5 class="fw-bold mb-1">{{ cat.name }}</h5>
                    <span class="small text-white-50">{{ cat.count }} Products</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="py-6">
        <div class="container px-lg-5">
          <div class="text-center mb-5">
            <h2 class="fw-bold">Trending This Week</h2>
            <p class="text-muted">Top picks loved by our community</p>
          </div>

          <div class="row row-cols-1 row-cols-sm-2 row-cols-lg-4 g-4">
            <div v-for="product in trendingProducts" :key="product.id" class="col">
              <div class="product-card h-100 border-0">
                <div class="position-relative bg-light rounded-4 overflow-hidden mb-3 aspect-square group">
                  <span v-if="product.tag" class="position-absolute top-0 start-0 m-3 badge bg-white text-dark shadow-sm rounded-pill px-3">
                    {{ product.tag }}
                  </span>
                  <img :src="product.image" class="w-100 h-100 object-fit-cover transition-scale" :alt="product.name">
                  <div class="action-overlay position-absolute bottom-0 w-100 p-3">
                    <button class="btn btn-white w-100 rounded-pill fw-bold shadow-sm" @click="addToCart(product)">
                      Quick Add - ${{ product.price }}
                    </button>
                  </div>
                </div>
                <div class="px-2">
                  <h6 class="fw-bold mb-1 text-truncate">{{ product.name }}</h6>
                  <p class="text-muted small mb-0">{{ product.category }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="py-5 bg-light border-top border-bottom">
        <div class="container px-lg-5">
          <div class="row g-4 text-center justify-content-center">
            <div class="col-6 col-md-3">
              <div class="py-3">
                <i class="bi bi-box-seam fs-1 text-dark mb-3 d-block"></i>
                <h6 class="fw-bold mb-1">Free Shipping</h6>
                <p class="text-muted extra-small mb-0">On orders over $150</p>
              </div>
            </div>
            <div class="col-6 col-md-3">
              <div class="py-3">
                <i class="bi bi-arrow-repeat fs-1 text-dark mb-3 d-block"></i>
                <h6 class="fw-bold mb-1">Easy Returns</h6>
                <p class="text-muted extra-small mb-0">30-day hassle-free</p>
              </div>
            </div>
            <div class="col-6 col-md-3">
              <div class="py-3">
                <i class="bi bi-shield-check fs-1 text-dark mb-3 d-block"></i>
                <h6 class="fw-bold mb-1">Secure Payment</h6>
                <p class="text-muted extra-small mb-0">100% protected checkout</p>
              </div>
            </div>
            <div class="col-6 col-md-3">
              <div class="py-3">
                <i class="bi bi-chat-heart fs-1 text-dark mb-3 d-block"></i>
                <h6 class="fw-bold mb-1">24/7 Support</h6>
                <p class="text-muted extra-small mb-0">Expert assistance</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="py-0">
        <div class="container-fluid p-0">
          <div class="row g-0">
            <div class="col-lg-12">
              <div class="bg-dark text-white p-5 py-lg-6 text-center position-relative overflow-hidden">
                <div class="position-absolute top-50 start-50 translate-middle rounded-circle bg-secondary opacity-25" style="width: 600px; height: 600px; filter: blur(80px);"></div>
                
                <div class="position-relative z-1">
                  <span class="text-warning fw-bold tracking-wide text-uppercase small mb-3 d-block">Limited Time Offer</span>
                  <h2 class="display-4 fw-bolder mb-4">Summer Clearance Sale</h2>
                  <p class="lead text-white-50 mb-5">Up to 50% off on selected items. Don't miss out on these exclusive deals.</p>
                  <button class="btn btn-light rounded-pill px-5 py-3 fw-bold shadow-hover" @click="handleNavigation('sale')">
                    Access Sale
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="py-6">
        <div class="container px-lg-5">
          <h2 class="fw-bold mb-5">Best Sellers</h2>
          
          <div class="row flex-nowrap overflow-auto pb-4 hide-scrollbar g-4">
            <div v-for="item in bestSellers" :key="item.id" class="col-10 col-md-6 col-lg-3">
              <div class="card h-100 border-0 bg-transparent">
                <div class="position-relative rounded-4 overflow-hidden mb-3 aspect-portrait">
                  <img :src="item.image" class="w-100 h-100 object-fit-cover" :alt="item.name">
                  <span class="position-absolute top-0 end-0 m-3 badge bg-dark">Best Seller</span>
                </div>
                <div class="d-flex justify-content-between align-items-start">
                  <div>
                    <h6 class="fw-bold mb-1">{{ item.name }}</h6>
                    <span class="text-muted">${{ item.price }}</span>
                  </div>
                  <button class="btn btn-outline-dark btn-sm rounded-circle p-2 lh-1" @click="addToCart(item)">
                    <i class="bi bi-plus-lg"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="py-6 bg-surface">
        <div class="container">
          <div class="row justify-content-center">
            <div class="col-lg-6 text-center">
              <i class="bi bi-envelope-open display-4 text-muted mb-4 d-block"></i>
              <h2 class="fw-bold mb-3">Join the Inner Circle</h2>
              <p class="text-muted mb-4">Subscribe to our newsletter to receive early access to new drops and exclusive editorial content.</p>
              
              <form @submit.prevent class="d-flex gap-2">
                <input type="email" class="form-control form-control-lg rounded-pill border-0 shadow-sm ps-4" placeholder="Your email address">
                <button class="btn btn-dark rounded-pill px-4 fw-bold shadow-sm">Sign Up</button>
              </form>
              <p class="text-muted extra-small mt-3">We respect your privacy. Unsubscribe at any time.</p>
            </div>
          </div>
        </div>
      </section>

    </main>

    <PremiumFooter @navigate="handleNavigation" />

  </div>
</template>

<script>
// Mock Imports - Ensure these files exist in your project structure
import PremiumNavbar from '@/components/Navbar.vue';
import PremiumFooter from '@/components/Footer.vue';

export default {
  name: "HomeView",
  components: {
    PremiumNavbar,
    PremiumFooter
  },
  data() {
    return {
      isAuthenticated: false, // Toggle to test logged-in state
      cartCount: 2,
      
      // Mock Data
      categories: [
        { id: 1, name: "Workspace", count: 24, image: "https://images.unsplash.com/photo-1497215728101-856f4ea42174?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" },
        { id: 2, name: "Audio", count: 12, image: "https://images.unsplash.com/photo-1546435770-a3e426bf472b?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" },
        { id: 3, name: "Travel", count: 18, image: "https://images.unsplash.com/photo-1551107696-a4b0c5a0d9a2?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" },
        { id: 4, name: "Living", count: 32, image: "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" }
      ],
      
      trendingProducts: [
        { id: 101, name: "Minimal Desk Lamp", category: "Lighting", price: 89, tag: "New", image: "https://images.unsplash.com/photo-1507473888900-52e1ad145986?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" },
        { id: 102, name: "Mechanical Keyboard", category: "Tech", price: 159, tag: "", image: "https://images.unsplash.com/photo-1587829741301-dc798b91add4?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" },
        { id: 103, name: "Leather Tote", category: "Accessories", price: 210, tag: "Hot", image: "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" },
        { id: 104, name: "Ceramic Vase", category: "Decor", price: 45, tag: "", image: "https://images.unsplash.com/photo-1612196808214-b7e239e5f6b7?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" }
      ],
      
      bestSellers: [
        { id: 201, name: "Analog Watch", price: 299, image: "https://images.unsplash.com/photo-1524592094714-0f0654e20314?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" },
        { id: 202, name: "Noise Cancelling Headphones", price: 349, image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" },
        { id: 203, name: "Modern Chair", price: 199, image: "https://images.unsplash.com/photo-1592078615290-033ee584e267?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" },
        { id: 204, name: "Smart Speaker", price: 129, image: "https://images.unsplash.com/photo-1589492477829-5e65395b66cc?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" }
      ]
    };
  },
  methods: {
    handleNavigation(page) {
      console.log(`Navigating to: ${page}`);
      // In real app: this.$router.push({ name: page });
    },
    handleLogout() {
      this.isAuthenticated = false;
      alert("Logged out successfully");
    },
    handleSearch(query) {
      console.log(`Search: ${query}`);
    },
    handleCategory(id) {
      console.log(`Filtering Category ID: ${id}`);
    },
    addToCart(product) {
      this.cartCount++;
      alert(`Added ${product.name} to cart.`);
    }
  }
};
</script>

<style scoped>
/* GLOBAL PREMIUM THEME OVERRIDES */

/* Layout & Spacing */
.py-6 { padding-top: 5rem; padding-bottom: 5rem; }
.bg-surface { background-color: #f8f9fa; }
.text-balance { text-wrap: balance; }

/* 1. Hero Section */
.hero-section {
  min-height: 80vh;
  background-color: #fff;
  overflow: hidden;
}

.text-gradient {
  background: linear-gradient(90deg, #1a1a1a 0%, #6c757d 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.shadow-xl { box-shadow: 0 20px 40px rgba(0,0,0,0.1); }

/* 2. Animations */
.animate-fade-in { animation: fadeIn 1s ease-out; }
.animate-slide-up { animation: slideUp 1s ease-out 0.3s backwards; }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }

/* 3. Cards & Hover Effects */
.transition-scale { transition: transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94); }
.group:hover .transition-scale, .category-card:hover .transition-scale { transform: scale(1.05); }

.gradient-overlay {
  background: linear-gradient(to top, rgba(0,0,0,0.6) 0%, transparent 100%);
}

.aspect-square { aspect-ratio: 1/1; }
.aspect-portrait { aspect-ratio: 3/4; }

/* 4. Product Action Button */
.action-overlay {
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.3s ease;
}
.group:hover .action-overlay {
  opacity: 1;
  transform: translateY(0);
}

.btn-white {
  background: rgba(255,255,255,0.95);
  color: #000;
  transition: all 0.2s;
}
.btn-white:hover {
  background: #000;
  color: #fff;
}

/* 5. Utility & Buttons */
.btn-link-dark {
  color: #1a1a1a;
  position: relative;
}
.btn-link-dark::after {
  content: ''; position: absolute; bottom: -2px; left: 0; width: 0; height: 2px;
  background: #1a1a1a; transition: width 0.3s;
}
.btn-link-dark:hover::after { width: 100%; }

.shadow-hover:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.15) !important;
}

/* 6. Mobile Scrollbar Hiding */
.hide-scrollbar::-webkit-scrollbar { display: none; }
.hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }

/* Responsive Adjustments */
@media (max-width: 991px) {
  .hero-section { text-align: center; min-height: auto; padding-top: 2rem; padding-bottom: 2rem; }
  .display-3 { font-size: 2.5rem; }
  
  /* On mobile, action overlay is always visible or handled differently */
  .action-overlay { opacity: 1; transform: translateY(0); position: relative; bottom: auto; padding: 1rem; }
}
</style>