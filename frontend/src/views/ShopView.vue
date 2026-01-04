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
            Showing {{ filteredProducts.length }} Products
          </span>

          <div class="d-flex align-items-center gap-2">
            <span class="text-muted small d-none d-sm-inline">Sort by:</span>
            <select class="form-select form-select-sm border-0 bg-light rounded-0 fw-bold" style="width: auto; cursor: pointer;" v-model="sortBy">
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
        
        <div v-if="filteredProducts.length === 0" class="text-center py-5 my-5 animate-fade-up">
          <i class="bi bi-search display-1 text-light mb-3"></i>
          <h3 class="fw-bold">No products found</h3>
          <p class="text-muted">Try adjusting your filters.</p>
          <button class="btn btn-dark rounded-0 px-5 mt-3" @click="resetFilters">Reset All</button>
        </div>

        <div class="row row-cols-1 row-cols-sm-2 row-cols-lg-4 g-4 g-lg-5" v-else>
          <div class="col" v-for="product in filteredProducts" :key="product.id">
            <ProductCard 
              :product="product" 
              @add-to-cart="handleAddToCart"
              @click-product="viewProductDetails"
            />
          </div>
        </div>

        <div class="d-flex justify-content-center mt-6 pt-5" v-if="filteredProducts.length > 0">
          <button class="btn btn-outline-dark rounded-0 px-5 py-3 text-uppercase tracking-wide fw-bold hover-fill">
            Load More Products
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
              v-for="cat in categories" 
              :key="cat.id" 
              class="btn btn-sm rounded-0 transition-all"
              :class="selectedCategory === cat.id ? 'btn-dark' : 'btn-outline-secondary'"
              @click="toggleCategory(cat.id)"
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
              <button class="btn btn-dark w-100 rounded-0 py-3 text-uppercase fw-bold" data-bs-dismiss="offcanvas">Show Results</button>
            </div>
          </div>
        </div>

      </div>
    </div>

  </div>
</template>

<script>
import ProductCard from '@/components/ProductCard.vue';

export default {
  name: "ShopView",
  components: {
    ProductCard
  },
  data() {
    return {
      sortBy: 'newest',
      selectedCategory: null,
      priceMin: null,
      priceMax: null,
      inStockOnly: false,
      onSaleOnly: false,
      categories: [
        { id: 1, name: "Furniture" },
        { id: 2, name: "Lighting" },
        { id: 3, name: "Decor" },
        { id: 4, name: "Electronics" },
        { id: 5, name: "Accessories" }
      ],
      allProducts: [
        { id: 101, name: "Linen Lounge Chair", category: 1, price: 299, rating: 4.8, image: "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?auto=format&fit=crop&w=600&q=80", badge: "Best Seller" },
        { id: 102, name: "Ceramic Vase Set", category: 3, price: 89, rating: 4.5, image: "https://images.unsplash.com/photo-1612196808214-b7e239e5f6b7?auto=format&fit=crop&w=600&q=80", badge: "New" },
        { id: 103, name: "Minimal Desk Lamp", category: 2, price: 120, rating: 4.9, image: "https://images.unsplash.com/photo-1507473888900-52e1ad145986?auto=format&fit=crop&w=600&q=80", badge: "" },
        { id: 104, name: "Leather Tote Bag", category: 5, price: 195, rating: 4.7, image: "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?auto=format&fit=crop&w=600&q=80", badge: "" },
        { id: 105, name: "Smart Speaker Mini", category: 4, price: 49, rating: 4.2, image: "https://images.unsplash.com/photo-1589492477829-5e65395b66cc?auto=format&fit=crop&w=600&q=80", badge: "Sale" },
        { id: 106, name: "Oak Coffee Table", category: 1, price: 450, rating: 5.0, image: "https://images.unsplash.com/photo-1533090481720-856c6e3c1fdc?auto=format&fit=crop&w=600&q=80", badge: "" },
        { id: 107, name: "Cotton Throw", category: 3, price: 65, rating: 4.4, image: "https://images.unsplash.com/photo-1512914890207-6bf613254978?auto=format&fit=crop&w=600&q=80", badge: "" },
        { id: 108, name: "Wireless Headphones", category: 4, price: 299, rating: 4.8, image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=600&q=80", badge: "New" },
      ]
    };
  },
  computed: {
    filteredProducts() {
      let result = [...this.allProducts];
      if (this.selectedCategory) result = result.filter(p => p.category === this.selectedCategory);
      if (this.onSaleOnly) result = result.filter(p => p.badge === 'Sale');
      if (this.sortBy === 'price_low') result.sort((a, b) => a.price - b.price);
      else if (this.sortBy === 'price_high') result.sort((a, b) => b.price - a.price);
      else if (this.sortBy === 'newest') result.sort((a, b) => b.id - a.id);
      return result;
    }
  },
  methods: {
    handleNavigation(page) { console.log("Nav:", page); },
    toggleCategory(id) { this.selectedCategory = this.selectedCategory === id ? null : id; },
    handleAddToCart(p) { alert(`Added ${p.name}`); },
    viewProductDetails(p) { console.log("View:", p.id); },
    resetFilters() {
      this.selectedCategory = null;
      this.priceMin = null;
      this.priceMax = null;
      this.onSaleOnly = false;
      this.sortBy = 'newest';
    }
  }
};
</script>

<style scoped>
/* PREMIUM DESIGN OVERRIDES */

.shop-hero {
  height: 40vh; /* Takes up 40% of viewport height */
  background-color: #000;
}

/* Typography */
.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }

/* Buttons */
.hover-fill {
  transition: all 0.3s ease;
}
.hover-fill:hover {
  background-color: #212529;
  color: #fff;
}

/* Animations */
.animate-fade-up {
  animation: fadeUp 0.8s ease-out forwards;
  opacity: 0;
  transform: translateY(20px);
}
@keyframes fadeUp {
  to { opacity: 1; transform: translateY(0); }
}

/* Remove Form Focus Glow for Cleaner Look */
.form-control:focus, .form-select:focus {
  box-shadow: none;
  border-color: #000;
}
</style>