<template>
  <div class="d-flex flex-column min-vh-100 bg-white">
    
    <header class="hero-section position-relative d-flex align-items-center text-white overflow-hidden">
      <img 
        src="https://images.unsplash.com/photo-1483985988355-763728e1935b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80" 
        alt="New Arrivals" 
        class="position-absolute w-100 h-100 object-fit-cover hero-bg"
      >
      <div class="position-absolute top-0 start-0 w-100 h-100 bg-black opacity-30"></div>
      
      <div class="container position-relative z-2">
        <div class="row justify-content-center justify-content-lg-center">
          <div class="col-12 col-lg-8 text-start text-lg-center animate-fade-up">
            <span class="d-inline-block bg-white text-dark px-3 py-1 rounded-0 text-uppercase tracking-wide fw-bold small mb-3">
              Just Dropped
            </span>
            <h1 class="display-3 fw-bolder tracking-tight mb-3">New Arrivals</h1>
            <p class="lead fw-normal text-white-90 mb-4 mx-lg-auto" style="max-width: 600px;">
              Discover the latest additions designed for modern living. Curated pieces that define this season's aesthetic.
            </p>
            <button class="btn btn-light rounded-0 px-5 py-3 text-uppercase fw-bold tracking-wide hover-lift" @click="scrollToGrid">
              Shop New In
            </button>
          </div>
        </div>
      </div>
    </header>

    <div class="sticky-top bg-white border-bottom z-3" id="new-arrivals-grid">
      <div class="container px-lg-5 py-3">
        <div class="d-flex justify-content-between align-items-center">
          <span class="text-muted extra-small text-uppercase tracking-wide">
            Showing {{ products.length }} of {{ totalProducts }} new products
          </span>

          <div class="d-flex align-items-center gap-2">
            <span class="text-muted small d-none d-sm-inline">Sort by:</span>
            <select class="form-select form-select-sm border-0 bg-light rounded-0 fw-bold" style="width: auto; cursor: pointer;" v-model="sortBy">
              <option value="newest">Newest First</option>
              <option value="price_low">Price: Low to High</option>
              <option value="price_high">Price: High to Low</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <main class="flex-grow-1 py-5">
      <div class="container px-lg-5">
        
        <div v-if="loading && products.length === 0" class="text-center py-5">
            <div class="spinner-border text-dark" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>

        <div v-else-if="error" class="alert alert-danger text-center rounded-0">
            {{ error }}
            <br>
            <button class="btn btn-sm btn-outline-danger mt-2" @click="fetchProducts(true)">Retry</button>
        </div>

        <div v-else class="row row-cols-1 row-cols-sm-2 row-cols-lg-4 g-4 g-lg-5">
          <div class="col" v-for="product in products" :key="product.id">
            <ProductCard 
              :product="product" 
              @add-to-cart="handleAddToCart"
              @click-product="viewProductDetails"
            />
          </div>
        </div>

        <div class="text-center mt-5 pt-4" v-if="products.length > 0">
           <span class="d-block text-muted small mb-3">Viewing {{ products.length }} of {{ totalProducts }} New Items</span>
           
           <div class="progress mx-auto mb-4" style="height: 2px; max-width: 200px;">
             <div class="progress-bar bg-dark" :style="{ width: (products.length / totalProducts) * 100 + '%' }"></div>
           </div>
           
           <button 
             v-if="currentPage < totalPages"
             class="btn btn-outline-dark rounded-0 px-5 py-3 text-uppercase fw-bold tracking-wide hover-fill"
             @click="loadMore"
             :disabled="loading"
           >
             {{ loading ? 'Loading...' : 'Load More' }}
           </button>
        </div>

      </div>
    </main>

    <section class="bg-light py-5">
      <div class="container px-lg-5">
        <div class="row align-items-center g-0 border bg-white shadow-sm overflow-hidden">
          <div class="col-lg-6 order-1 order-lg-1">
            <div class="h-100 position-relative" style="min-height: 400px;">
              <img 
                src="https://images.unsplash.com/photo-1556905055-8f358a7a47b2?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80" 
                alt="Fresh Picks" 
                class="position-absolute w-100 h-100 object-fit-cover"
              >
            </div>
          </div>
          <div class="col-lg-6 order-2 order-lg-2 p-5 text-center text-lg-start">
            <span class="text-uppercase tracking-wide text-muted extra-small fw-bold mb-2 d-block">Editorial</span>
            <h2 class="display-6 fw-bold mb-3">Fresh Picks This Week</h2>
            <p class="text-muted mb-4 lead fs-6">
              Our design team has hand-selected their favorites from the latest drop. 
              Explore textures, earthy tones, and sustainable materials.
            </p>
            <button class="btn btn-dark rounded-0 px-4 py-3 text-uppercase fw-bold tracking-wide hover-lift">
              Explore Collection
            </button>
          </div>
        </div>
      </div>
    </section>

    <section class="py-6 container px-lg-5">
      <div class="bg-dark text-white rounded-4 p-5 text-center position-relative overflow-hidden">
        <div class="position-absolute top-0 start-0 w-100 h-100 bg-gradient-overlay opacity-50"></div>
        
        <div class="position-relative z-2">
          <h2 class="fw-bold mb-2">Be the First to Know</h2>
          <p class="text-white-50 mb-4" style="max-width: 500px; margin: 0 auto;">
            Get early access to new drops, exclusive offers, and editorial content.
          </p>
          <form @submit.prevent="handleNewsletter" class="d-flex justify-content-center gap-2 flex-column flex-sm-row" style="max-width: 500px; margin: 0 auto;">
            <input 
                v-model="email"
                type="email" 
                class="form-control form-control-lg rounded-pill border-0" 
                placeholder="Your email address"
                required
            >
            <button type="submit" class="btn btn-light rounded-pill px-4 fw-bold">Notify Me</button>
          </form>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import ProductCard from '@/components/ProductCard.vue';
import api from '@/services/api'; // This is your raw Axios instance

// --- State Variables ---
const products = ref([]);
const loading = ref(false);
const error = ref(null);
const sortBy = ref('newest');
const currentPage = ref(1);
const totalPages = ref(1);
const totalProducts = ref(0);
const email = ref('');

const limit = 8;
const router = useRouter();

// --- Fetch Logic ---
const fetchProducts = async (reset = false) => {
  loading.value = true;
  error.value = null;

  try {
    if (reset) {
      currentPage.value = 1;
      products.value = [];
    }

    const params = {
      sort: sortBy.value,
      page: currentPage.value,
      limit: limit
    };

    // --- FIX IS HERE: Use api.get() directly ---
    // We call the URL endpoint string directly instead of a helper function
    const response = await api.get('/products/new-arrivals', { params });

    // --- Data Mapping ---
    // Ensure the structure matches what your Flask API returns
    const mappedProducts = response.data.data.map(item => {
      return {
        id: item.id,
        name: item.product_name || item.name, 
        price: item.price,
        category: item.category_name || 'General', 
        badge: 'New', 
        image: item.image_url || `https://source.unsplash.com/random/300x400?sig=${item.id}&furniture`,
        rating: 4.5 
      };
    });
    
    if (reset) {
      products.value = mappedProducts;
    } else {
      products.value = [...products.value, ...mappedProducts];
    }

    totalProducts.value = response.data.total;
    totalPages.value = response.data.pages;

  } catch (err) {
    console.error("Fetch Error:", err);
    if (err.message === "Network Error") {
      error.value = "Cannot connect to Backend. Is Flask running on port 5000?";
    } else {
      error.value = "Unable to load products. " + (err.response?.data?.message || err.message);
    }
  } finally {
    loading.value = false;
  }
};

// --- Watchers ---
watch(sortBy, () => {
  fetchProducts(true);
});

// --- Event Handlers ---
const loadMore = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
    fetchProducts(false);
  }
};

const handleAddToCart = async (product) => {
  try {
    // --- FIX IS HERE: Use api.post() directly ---
    // Assuming your endpoint expects product_id and quantity
    await api.post('/cart/add', { 
      product_id: product.id, 
      quantity: 1 
    });
    
    alert(`${product.name} added to cart!`);
  } catch (err) {
    if (err.response && err.response.status === 401) {
      alert("Please log in to add items to your cart.");
      // Optional: router.push('/login');
    } else {
      console.error("Add to cart error", err);
      alert("Failed to add to cart.");
    }
  }
};

const viewProductDetails = (product) => {
  router.push(`/product/${product.id}`);
};

const handleNewsletter = async () => {
  // Use api.post directly if you have this endpoint
  // await api.post('/newsletter/subscribe', { email: email.value });
  alert(`Subscribed ${email.value} to newsletter!`);
  email.value = '';
};

const scrollToGrid = () => {
  const el = document.getElementById('new-arrivals-grid');
  if (el) el.scrollIntoView({ behavior: 'smooth' });
};

// --- Lifecycle ---
onMounted(() => {
  fetchProducts(true);
});
</script>


<style scoped>
/* PAGE STYLES */

/* Hero Section */
.hero-section {
  height: 60vh;
  background-color: #1a1a1a;
}
.hero-bg {
  opacity: 0.9;
}
.text-white-90 {
  color: rgba(255, 255, 255, 0.9);
}

/* Typography */
.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }

/* Interactions */
.hover-lift {
  transition: transform 0.3s ease;
}
.hover-lift:hover {
  transform: translateY(-3px);
}

.hover-fill {
  transition: all 0.3s ease;
}
.hover-fill:hover {
  background-color: #000;
  color: #fff;
}

/* Animations */
.animate-fade-up {
  animation: fadeUp 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
  transform: translateY(30px);
}
@keyframes fadeUp {
  to { opacity: 1; transform: translateY(0); }
}

/* Newsletter Gradient */
.bg-gradient-overlay {
  background: radial-gradient(circle at top right, rgba(255,255,255,0.1) 0%, transparent 60%);
}

.py-6 { padding-top: 5rem; padding-bottom: 5rem; }

/* Remove Focus Glow */
.form-control:focus, .form-select:focus {
  box-shadow: none;
  border-color: #000;
}
</style>