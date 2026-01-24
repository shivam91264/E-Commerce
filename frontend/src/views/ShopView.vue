<template>
  <div class="d-flex flex-column min-vh-100 bg-white">
    
    <header class="shop-hero position-relative d-flex align-items-center justify-content-center text-center text-white overflow-hidden">
      <img 
        src="https://images.unsplash.com/photo-1441986300917-64674bd600d8?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80" 
        alt="Shop Banner" 
        class="position-absolute w-100 h-100 object-fit-cover opacity-75"
      >
      <div class="position-absolute top-0 start-0 w-100 h-100 bg-black opacity-25"></div>
      <div class="position-relative z-2 px-4 animate-fade-up">
        <span class="d-block text-uppercase tracking-wide mb-2 small fw-bold text-warning">New Collection</span>
        <h1 class="display-3 fw-bolder tracking-tight mb-3">The Essentials Edit</h1>
        <p class="lead fw-normal text-white-50 mx-auto" style="max-width: 600px;">
          Curated pieces designed for the modern individual. Timeless, functional, and effortlessly stylish.
        </p>
      </div>
    </header>

    <div class="sticky-top bg-white border-bottom z-3">
      <div class="container-fluid px-lg-5 py-3">
        <div class="d-flex justify-content-between align-items-center">
          
          <button 
            class="btn btn-outline-dark rounded-0 px-4 py-2 text-uppercase fw-bold small d-flex align-items-center gap-2 hover-fill" 
            type="button" 
            data-bs-toggle="offcanvas" 
            data-bs-target="#filterOffcanvas"
          >
            <i class="bi bi-sliders2"></i> Filters
          </button>

          <span class="text-muted extra-small text-uppercase tracking-wide d-none d-md-block">
            Showing {{ products.length }} of {{ totalProducts }} Products
          </span>

          <div class="d-flex align-items-center gap-2">
            <span class="text-muted small d-none d-sm-inline">Sort by:</span>
            <select class="form-select form-select-sm border-0 bg-light rounded-0 fw-bold" style="width: auto; cursor: pointer;" v-model="sortBy" @change="resetAndFetch">
              <option value="newest">Newest</option>
              <option value="price_low">Price: Low to High</option>
              <option value="price_high">Price: High to Low</option>
            </select>
          </div>

        </div>
      </div>
    </div>

    <main class="flex-grow-1">
      <div class="container-fluid px-lg-5 py-5">
        
        <div v-if="loading && products.length === 0" class="text-center py-5">
           <div class="spinner-border text-dark" role="status"></div>
        </div>

        <div v-else-if="products.length === 0" class="text-center py-5 my-5 animate-fade-up">
          <i class="bi bi-search display-1 text-light mb-3"></i>
          <h3 class="fw-bold">No products found</h3>
          <p class="text-muted">Try adjusting your filters.</p>
          <button class="btn btn-dark rounded-0 px-5 mt-3" @click="resetFilters">Reset All</button>
        </div>

        <div class="row row-cols-1 row-cols-sm-2 row-cols-lg-4 g-4 g-lg-5" v-else>
          <div class="col" v-for="product in products" :key="product.id">
            <ProductCard 
              :product="product" 
              @add-to-cart="handleAddToCart"
              @click-product="viewProductDetails"
              @add-to-wishlist="handleAddToWishlist"
            />
          </div>
        </div>

        <div class="d-flex justify-content-center mt-6 pt-5" v-if="hasMoreProducts">
          <button 
            class="btn btn-outline-dark rounded-0 px-5 py-3 text-uppercase tracking-wide fw-bold hover-fill"
            @click="loadMore"
            :disabled="loading"
          >
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            {{ loading ? 'Loading...' : 'Load More Products' }}
          </button>
        </div>

      </div>
    </main>

    <div class="offcanvas offcanvas-start" tabindex="-1" id="filterOffcanvas" aria-labelledby="filterOffcanvasLabel">
      <div class="offcanvas-header border-bottom p-4">
        <h5 class="offcanvas-title fw-bold text-uppercase tracking-wide" id="filterOffcanvasLabel">Filter & Sort</h5>
        <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      <div class="offcanvas-body p-4 d-flex flex-column">
        
        <div class="mb-5">
          <h6 class="fw-bold text-uppercase tracking-wide mb-3 extra-small text-muted">Categories</h6>
          <div class="d-flex flex-wrap gap-2">
            <button 
              class="btn btn-sm rounded-0 transition-all"
              :class="selectedCategorySlug === 'all' ? 'btn-dark' : 'btn-outline-secondary'"
              @click="toggleCategory('all')"
            >
              All
            </button>
            
            <button 
              v-for="cat in categories" 
              :key="cat.id" 
              class="btn btn-sm rounded-0 transition-all"
              :class="selectedCategorySlug === cat.slug ? 'btn-dark' : 'btn-outline-secondary'"
              @click="toggleCategory(cat.slug)"
            >
              {{ cat.name }}
            </button>
          </div>
        </div>

        <div class="mb-5">
          <h6 class="fw-bold text-uppercase tracking-wide mb-3 extra-small text-muted">Price Range</h6>
          <div class="d-flex align-items-center gap-2">
            <input type="number" class="form-control rounded-0 bg-light border-0" placeholder="Min" v-model="priceMin">
            <span class="text-muted">-</span>
            <input type="number" class="form-control rounded-0 bg-light border-0" placeholder="Max" v-model="priceMax">
          </div>
        </div>

        <div class="mb-5">
           <h6 class="fw-bold text-uppercase tracking-wide mb-3 extra-small text-muted">Availability</h6>
           <div class="form-check form-switch mb-2">
              <input class="form-check-input cursor-pointer" type="checkbox" id="stockSwitch" v-model="inStockOnly">
              <label class="form-check-label text-muted cursor-pointer" for="stockSwitch">In Stock Only</label>
           </div>
           <div class="form-check form-switch">
              <input class="form-check-input cursor-pointer" type="checkbox" id="saleSwitch" v-model="onSaleOnly">
              <label class="form-check-label text-muted cursor-pointer" for="saleSwitch">On Sale</label>
           </div>
        </div>

        <div class="mt-auto pt-4 border-top">
          <div class="row g-2">
            <div class="col-6">
              <button class="btn btn-outline-dark w-100 rounded-0 py-3 text-uppercase fw-bold" @click="resetFilters">Clear</button>
            </div>
            <div class="col-6">
              <button class="btn btn-dark w-100 rounded-0 py-3 text-uppercase fw-bold" data-bs-dismiss="offcanvas" @click="resetAndFetch">Show Results</button>
            </div>
          </div>
        </div>

      </div>
    </div>

  </div>
</template>

<script>
import ProductCard from '@/components/ProductCard.vue';
import api from "@/services/api";

export default {
  name: "ShopView",
  components: { ProductCard },
  data() {
    return {
      products: [],
      categories: [],
      loading: false,
      
      // Filters
      selectedCategorySlug: 'all', 
      sortBy: 'newest',
      priceMin: null,
      priceMax: null,
      inStockOnly: false,
      onSaleOnly: false,
      
      // Pagination
      page: 1,
      limit: 12,
      totalProducts: 0
    };
  },
  computed: {
    hasMoreProducts() {
      return this.products.length < this.totalProducts;
    }
  },
  watch: {
    // Immediate: true ensures this runs on initial load AND subsequent changes
    '$route.query.category': {
      handler(newSlug) {
        console.log("Route Changed -> Category Slug:", newSlug);
        this.selectedCategorySlug = newSlug || 'all';
        this.resetAndFetch();
      },
      immediate: true 
    }
  },
  mounted() {
    this.fetchCategories();
  },
  methods: {
    // 1. Fetch Categories for Sidebar
    async fetchCategories() {
      try {
        const res = await api.get('/api/categories');
        this.categories = res.data.data;
      } catch (err) {
        console.error("Categories Error:", err);
      }
    },

    // 2. Main Fetch Logic
    async fetchProducts(append = false) {
      this.loading = true;
      try {
        const params = {
          page: this.page,
          limit: this.limit,
          sort: this.sortBy,
          price_min: this.priceMin || undefined,
          price_max: this.priceMax || undefined,
          in_stock: this.inStockOnly ? 'true' : undefined,
          on_sale: this.onSaleOnly ? 'true' : undefined
        };

        const endpoint = `/products/category/${this.selectedCategorySlug}`;
        
        const res = await api.get(endpoint, { params });
        
        if (append) {
          this.products = [...this.products, ...res.data.data];
        } else {
          this.products = res.data.data;
        }
        this.totalProducts = res.data.total;

      } catch (err) {
        console.error("Product Load Error:", err);
      } finally {
        this.loading = false;
      }
    },

    // 3. Actions
    resetAndFetch() {
      this.page = 1;
      this.fetchProducts(false);
    },

    loadMore() {
      this.page++;
      this.fetchProducts(true);
    },

    toggleCategory(slug) {
      const newSlug = this.selectedCategorySlug === slug ? 'all' : slug;
      this.$router.push({ query: { ...this.$route.query, category: newSlug } });
    },

    resetFilters() {
      this.$router.push({ query: {} }); // Clear URL
      this.selectedCategorySlug = 'all';
      this.priceMin = null;
      this.priceMax = null;
      this.inStockOnly = false;
      this.onSaleOnly = false;
      this.sortBy = 'newest';
    },

    // 4. Cart, Wishlist & Details
    async handleAddToCart(product) {
      try {
        await api.post(`/user/cart/${product.id}`);
        alert("Added to cart");
      } catch (err) {
        if(err.response?.status === 401) alert("Please login first");
        else alert("Failed to add to cart");
      }
    },

    // --- NEW: Handle Wishlist Event ---
    async handleAddToWishlist(product) {
      try {
        // Calls POST /user/wishlist/<product_id>
        await api.post(`/user/wishlist/${product.id}`);
        alert(`${product.name} added to Wishlist!`);
      } catch (err) {
        if (err.response?.status === 401) {
          alert("Please login to use the wishlist.");
        } else if (err.response?.status === 400) {
          alert("Product is already in your wishlist.");
        } else {
          console.error("Wishlist Error:", err);
          alert("Failed to add to wishlist.");
        }
      }
    },

    viewProductDetails(product) {
      this.$router.push(`/product/${product.id}`);
    }
  }
};
</script>

<style scoped>
/* Reused styles */
.shop-hero { height: 40vh; background-color: #000; }
.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }
.hover-fill { transition: all 0.3s ease; }
.hover-fill:hover { background-color: #212529; color: #fff; }
.animate-fade-up { animation: fadeUp 0.8s ease-out forwards; opacity: 0; transform: translateY(20px); }
@keyframes fadeUp { to { opacity: 1; transform: translateY(0); } }
.form-control:focus, .form-select:focus { box-shadow: none; border-color: #000; }
</style>