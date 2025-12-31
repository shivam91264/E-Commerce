<template>
  <div class="d-flex flex-column min-vh-100 bg-white">
    
    <PremiumNavbar 
      :is-authenticated="false" 
      :cart-item-count="2" 
      user-role="guest"
      @navigate="handleNavigation"
    />

    <main class="flex-grow-1">
      
      <header class="bg-light-subtle py-5 border-bottom border-light">
        <div class="container px-lg-5">
          <div class="d-flex flex-column flex-md-row justify-content-between align-items-end animate-fade-up position-relative" style="z-index: 100;">
            
            <div class="mb-4 mb-md-0 w-100">
              <span class="d-block text-muted extra-small text-uppercase tracking-wide fw-bold mb-2">
                Search Results
              </span>
              <h1 class="display-4 fw-bold tracking-tight mb-2 text-break text-dark">
                "{{ searchQuery }}"
              </h1>
              <p class="text-muted lead fs-6 mb-0">
                We found <span class="text-dark fw-bold">{{ sortedProducts.length }}</span> products matching your search.
              </p>
            </div>

            <div v-if="sortedProducts.length > 0" class="d-flex flex-column flex-sm-row gap-2 w-100 w-md-auto">
              
              <div class="dropdown w-100 w-sm-auto">
                 <button class="btn btn-white border shadow-sm rounded-pill px-4 py-2 d-flex align-items-center justify-content-center gap-2 small fw-bold text-uppercase tracking-wide w-100" type="button" data-bs-toggle="dropdown">
                   <span>Category</span>
                   <i class="bi bi-chevron-down extra-small"></i>
                 </button>
                 <ul class="dropdown-menu dropdown-menu-end border-0 shadow-lg rounded-4 p-2 mt-2 w-100 w-sm-auto">
                   <li><a class="dropdown-item rounded-2 small py-2" href="#">All Categories</a></li>
                   <li><a class="dropdown-item rounded-2 small py-2" href="#">Furniture</a></li>
                   <li><a class="dropdown-item rounded-2 small py-2" href="#">Lighting</a></li>
                 </ul>
              </div>

              <div class="dropdown w-100 w-sm-auto">
                 <button class="btn btn-white border shadow-sm rounded-pill px-4 py-2 d-flex align-items-center justify-content-center gap-2 small fw-bold text-uppercase tracking-wide w-100" type="button" data-bs-toggle="dropdown">
                   <span class="text-truncate">Sort: {{ sortByLabel }}</span>
                   <i class="bi bi-chevron-down extra-small"></i>
                 </button>
                 <ul class="dropdown-menu dropdown-menu-end border-0 shadow-lg rounded-4 p-2 mt-2 w-100 w-sm-auto">
                   <li><a class="dropdown-item rounded-2 small py-2" href="#" @click.prevent="sortBy = 'relevance'">Relevance</a></li>
                   <li><a class="dropdown-item rounded-2 small py-2" href="#" @click.prevent="sortBy = 'price_low'">Price: Low to High</a></li>
                   <li><a class="dropdown-item rounded-2 small py-2" href="#" @click.prevent="sortBy = 'price_high'">Price: High to Low</a></li>
                 </ul>
              </div>

            </div>
          </div>
        </div>
      </header>

      <div class="container px-lg-5 py-5">
        
        <div v-if="sortedProducts.length === 0" class="text-center py-6 animate-fade-up">
          <div class="d-inline-flex p-4 rounded-circle bg-light mb-4">
            <i class="bi bi-search display-4 text-muted opacity-50"></i>
          </div>
          <h3 class="fw-bold mb-3">No results found</h3>
          <p class="text-muted mb-4 mx-auto" style="max-width: 450px;">
            We couldn't find any products matching "{{ searchQuery }}". Try checking for typos or using general keywords like "Chair" or "Lamp".
          </p>
          <button class="btn btn-dark rounded-pill px-5 py-3 text-uppercase fw-bold tracking-wide hover-lift" @click="clearSearch">
            Clear Search
          </button>
        </div>

        <div v-else class="row row-cols-1 row-cols-sm-2 row-cols-lg-4 g-4 g-lg-5">
          <div 
            class="col" 
            v-for="(product, index) in sortedProducts" 
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

        <div class="text-center mt-6 pt-5 border-top" v-if="sortedProducts.length > 0">
           <span class="d-block text-muted small mb-3">Viewing {{ sortedProducts.length }} of 42 results</span>
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
  name: "SearchResultsView",
  components: {
    PremiumNavbar,
    PremiumFooter,
    ProductCard
  },
  data() {
    return {
      searchQuery: "Modern Chair", 
      sortBy: "relevance",
      
      // Mock Products Array
      products: [
        { id: 101, name: "Linen Lounge Chair", category: "Furniture", price: 299, image: "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?auto=format&fit=crop&w=600&q=80", badge: "Best Seller" },
        { id: 102, name: "Velvet Accent Chair", category: "Furniture", price: 349, image: "https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?auto=format&fit=crop&w=600&q=80", badge: "" },
        { id: 103, name: "Minimal Desk Lamp", category: "Lighting", price: 120, image: "https://images.unsplash.com/photo-1507473888900-52e1ad145986?auto=format&fit=crop&w=600&q=80", badge: "New" },
        { id: 104, name: "Oak Side Table", category: "Furniture", price: 149, image: "https://images.unsplash.com/photo-1533090481720-856c6e3c1fdc?auto=format&fit=crop&w=600&q=80", badge: "" },
        { id: 105, name: "Woven Jute Rug", category: "Decor", price: 199, image: "https://images.unsplash.com/photo-1575414769150-b828f724ff0c?auto=format&fit=crop&w=600&q=80", badge: "" },
        { id: 106, name: "Ceramic Vase Set", category: "Decor", price: 89, image: "https://images.unsplash.com/photo-1612196808214-b7e239e5f6b7?auto=format&fit=crop&w=600&q=80", badge: "Sale" },
        { id: 107, name: "Cotton Throw", category: "Accessories", price: 65, image: "https://images.unsplash.com/photo-1512914890207-6bf613254978?auto=format&fit=crop&w=600&q=80", badge: "" },
        { id: 108, name: "Leather Tote Bag", category: "Accessories", price: 195, image: "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?auto=format&fit=crop&w=600&q=80", badge: "Limited" },
      ]
    };
  },
  computed: {
    sortByLabel() {
      switch(this.sortBy) {
        case 'price_low': return 'Price: Low to High';
        case 'price_high': return 'Price: High to Low';
        case 'newest': return 'Newest';
        default: return 'Relevance';
      }
    },
    sortedProducts() {
      let items = [...this.products];
      if (this.sortBy === 'price_low') items.sort((a, b) => a.price - b.price);
      else if (this.sortBy === 'price_high') items.sort((a, b) => b.price - a.price);
      else if (this.sortBy === 'newest') items.sort((a, b) => b.id - a.id);
      return items;
    }
  },
  methods: {
    handleNavigation(page) { console.log(`Navigating to: ${page}`); },
    handleAddToCart(product) { alert(`Added ${product.name} to cart!`); },
    viewProductDetails(product) { console.log(`View Product: ${product.id}`); },
    clearSearch() { 
      this.searchQuery = ""; 
      alert("Search cleared.");
    }
  }
};
</script>

<style scoped>
/* PREMIUM VISUAL LANGUAGE */

/* Backgrounds */
.bg-light-subtle { background-color: #f9fafb !important; }

/* Typography */
.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }

/* Spacing */
.py-6 { padding-top: 5rem; padding-bottom: 5rem; }
.mt-6 { margin-top: 5rem; }

/* Animations */
.animate-fade-up {
  animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
  transform: translateY(20px);
}
@keyframes fadeUp {
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
.dropdown-item:active {
    background-color: #f8f9fa;
    color: #000;
    font-weight: bold;
}
</style>