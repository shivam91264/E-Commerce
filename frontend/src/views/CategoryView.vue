<template>
  <div class="d-flex flex-column min-vh-100 bg-white">
    
    <PremiumNavbar 
      :is-authenticated="false" 
      :cart-item-count="3" 
      user-role="guest"
      @navigate="handleNavigation"
    />

    <main class="flex-grow-1">
      
      <header class="bg-light-subtle pt-5 pb-4 border-bottom border-light">
        <div class="container px-lg-5">
          
          <nav aria-label="breadcrumb" class="mb-4 animate-fade-down">
            <ol class="breadcrumb small text-uppercase tracking-wide">
              <li class="breadcrumb-item"><a href="#" class="text-muted text-decoration-none">Home</a></li>
              <li class="breadcrumb-item"><a href="#" class="text-muted text-decoration-none">Shop</a></li>
              <li class="breadcrumb-item active text-dark fw-bold" aria-current="page">{{ currentCategory }}</li>
            </ol>
          </nav>

          <div class="d-flex flex-column flex-md-row justify-content-between align-items-end animate-fade-up position-relative" style="z-index: 100;">
            
            <div class="mb-4 mb-md-0 w-100 text-center text-md-start">
              <h1 class="display-4 fw-bold tracking-tight mb-2 text-dark">
                {{ currentCategory }}
              </h1>
              <p class="text-muted lead fs-6 mb-0" style="max-width: 600px;">
                Explore our curated collection of premium {{ currentCategory.toLowerCase() }}. 
                <span class="d-block d-md-inline mt-1 mt-md-0">
                  Showing <span class="text-dark fw-bold">{{ filteredProducts.length }}</span> products.
                </span>
              </p>
            </div>

            <div v-if="filteredProducts.length > 0" class="d-flex flex-column flex-sm-row gap-2 w-100 w-md-auto">
              
              <div class="dropdown w-100 w-sm-auto">
                <button class="btn btn-white border shadow-sm rounded-pill px-4 py-2 d-flex align-items-center justify-content-center gap-2 small fw-bold text-uppercase tracking-wide w-100" 
                        type="button" data-bs-toggle="dropdown">
                  <span>Filter</span>
                  <i class="bi bi-sliders extra-small"></i>
                </button>
                <ul class="dropdown-menu dropdown-menu-end border-0 shadow-lg rounded-4 p-3 mt-2 w-100 w-sm-300px">
                  <li><h6 class="dropdown-header text-uppercase tracking-wide small mb-2">Price Range</h6></li>
                  <li><div class="px-3 pb-3"><input type="range" class="form-range" id="customRange1"></div></li>
                  <li><hr class="dropdown-divider"></li>
                  <li><h6 class="dropdown-header text-uppercase tracking-wide small mb-2">Brand</h6></li>
                  <li><a class="dropdown-item rounded-2 small py-1" href="#">Brand A</a></li>
                  <li><a class="dropdown-item rounded-2 small py-1" href="#">Brand B</a></li>
                  <li><div class="d-grid mt-2"><button class="btn btn-dark btn-sm rounded-pill">Apply</button></div></li>
                </ul>
              </div>

              <div class="dropdown w-100 w-sm-auto">
                 <button class="btn btn-white border shadow-sm rounded-pill px-4 py-2 d-flex align-items-center justify-content-center gap-2 small fw-bold text-uppercase tracking-wide w-100" 
                         type="button" data-bs-toggle="dropdown">
                   <span class="text-truncate">Sort: {{ sortByLabel }}</span>
                   <i class="bi bi-chevron-down extra-small"></i>
                 </button>
                 <ul class="dropdown-menu dropdown-menu-end border-0 shadow-lg rounded-4 p-2 mt-2 w-100 w-sm-auto">
                   <li><a class="dropdown-item rounded-2 small py-2" href="#" @click.prevent="sortBy = 'relevance'">Relevance</a></li>
                   <li><a class="dropdown-item rounded-2 small py-2" href="#" @click.prevent="sortBy = 'price_low'">Price: Low to High</a></li>
                   <li><a class="dropdown-item rounded-2 small py-2" href="#" @click.prevent="sortBy = 'price_high'">Price: High to Low</a></li>
                   <li><a class="dropdown-item rounded-2 small py-2" href="#" @click.prevent="sortBy = 'newest'">Newest Arrivals</a></li>
                 </ul>
              </div>

            </div>
          </div>
        </div>
      </header>

      <div class="container px-lg-5 py-5">
        
        <div v-if="filteredProducts.length === 0" class="text-center py-6 animate-fade-up">
          <div class="d-inline-flex p-4 rounded-circle bg-light mb-4">
            <i class="bi bi-box-seam display-4 text-muted opacity-50"></i>
          </div>
          <h3 class="fw-bold mb-3">No products found</h3>
          <p class="text-muted mb-4 mx-auto" style="max-width: 450px;">
            We currently don't have any stock in the <strong>{{ currentCategory }}</strong> category. Please check back later or browse our other collections.
          </p>
          <button class="btn btn-dark rounded-pill px-5 py-3 text-uppercase fw-bold tracking-wide hover-lift" @click="currentCategory = 'All'">
            View All Products
          </button>
        </div>

        <div v-else class="row row-cols-1 row-cols-sm-2 row-cols-lg-4 g-4 g-lg-5">
          <div 
            class="col" 
            v-for="(product, index) in filteredProducts" 
            :key="product.id"
          >
            <div 
              class="animate-fade-up" 
              :style="{ animationDelay: `${index * 50}ms` }"
            >
              <ProductCard 
                :product="product" 
                @add-to-cart="handleAddToCart"
                @click-product="viewProductDetails"
              />
            </div>
          </div>
        </div>

        <div class="text-center mt-6 pt-5 border-top" v-if="filteredProducts.length > 0">
           <span class="d-block text-muted small mb-3">Viewing {{ filteredProducts.length }} products</span>
           <button class="btn btn-outline-dark rounded-0 px-5 py-3 text-uppercase fw-bold tracking-wide hover-fill">
             Load More
           </button>
        </div>

      </div>
    </main>

    <PremiumFooter @navigate="handleNavigation" />

  </div>
</template>

<script>
import PremiumNavbar from '@/components/Navbar.vue';
import PremiumFooter from '@/components/Footer.vue';
import ProductCard from '@/components/ProductCard.vue';

export default {
  name: "CategoryView",
  components: {
    PremiumNavbar,
    PremiumFooter,
    ProductCard
  },
  data() {
    return {
      // State mimicking a route parameter (e.g., /category/electronics)
      currentCategory: "Electronics", 
      sortBy: "relevance",
      
      // Master Dummy Data (Mixed Categories to demonstrate filtering)
      allProducts: [
        { id: 101, name: "Noise Cancelling Headphones", category: "Electronics", price: 299, image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=600&q=80", badge: "Best Seller" },
        { id: 102, name: "Smart Fitness Watch", category: "Electronics", price: 199, image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=600&q=80", badge: "New" },
        { id: 103, name: "Leather Weekend Bag", category: "Accessories", price: 249, image: "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=600&q=80", badge: "" },
        { id: 104, name: "Wireless Earbuds", category: "Electronics", price: 129, image: "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=600&q=80", badge: "Sale" },
        { id: 105, name: "4K Action Camera", category: "Electronics", price: 349, image: "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?auto=format&fit=crop&w=600&q=80", badge: "" },
        { id: 106, name: "Minimalist Backpack", category: "Accessories", price: 89, image: "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=600&q=80", badge: "" },
        { id: 107, name: "Mechanical Keyboard", category: "Electronics", price: 159, image: "https://images.unsplash.com/photo-1587829741301-dc798b91add1?auto=format&fit=crop&w=600&q=80", badge: "" },
        { id: 108, name: "Smart Home Speaker", category: "Electronics", price: 99, image: "https://images.unsplash.com/photo-1589492477829-5e65395b66cc?auto=format&fit=crop&w=600&q=80", badge: "Hot" },
      ]
    };
  },
  computed: {
    // Label for the Sort Button
    sortByLabel() {
      switch(this.sortBy) {
        case 'price_low': return 'Price: Low to High';
        case 'price_high': return 'Price: High to Low';
        case 'newest': return 'Newest';
        default: return 'Relevance';
      }
    },
    // Filter by Category AND Sort
    filteredProducts() {
      // 1. Filter by Category
      let items = this.currentCategory === 'All' 
        ? [...this.allProducts]
        : this.allProducts.filter(p => p.category === this.currentCategory);

      // 2. Apply Sorting
      if (this.sortBy === 'price_low') items.sort((a, b) => a.price - b.price);
      else if (this.sortBy === 'price_high') items.sort((a, b) => b.price - a.price);
      else if (this.sortBy === 'newest') items.sort((a, b) => b.id - a.id); // Assuming higher ID = newer

      return items;
    }
  },
  methods: {
    handleNavigation(page) { console.log(`Navigating to: ${page}`); },
    handleAddToCart(product) { alert(`Added ${product.name} to cart!`); },
    viewProductDetails(product) { console.log(`View Product ID: ${product.id}`); }
  }
};
</script>

<style scoped>
/* 🎨 VISUAL STYLE GUIDELINES (Consistent with Site) */

/* Backgrounds */
.bg-light-subtle { background-color: #f9fafb !important; }

/* Typography */
.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }

/* Spacing */
.py-6 { padding-top: 5rem; padding-bottom: 5rem; }
.mt-6 { margin-top: 5rem; }
.w-sm-300px { width: 300px; }

/* Animations */
.animate-fade-up {
  animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
  transform: translateY(20px);
}
@keyframes fadeUp {
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-down {
  animation: fadeDown 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
  transform: translateY(-10px);
}
@keyframes fadeDown {
  to { opacity: 1; transform: translateY(0); }
}

/* Controls / Buttons */
.btn-white {
  background-color: #fff;
  color: #000;
  border-color: #dee2e6;
}
.btn-white:hover {
  border-color: #000;
  background-color: #f8f9fa;
}

.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.hover-fill {
  transition: all 0.3s ease;
}
.hover-fill:hover {
  background-color: #000;
  color: #fff;
}

/* Dropdown Customization */
.dropdown-toggle::after { display: none; }
.dropdown-item:active, .dropdown-item:hover {
    background-color: #f3f4f6;
    color: #000;
    font-weight: 600;
}
</style>