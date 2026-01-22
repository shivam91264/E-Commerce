<template>
  <div class="d-flex flex-column min-vh-100 bg-white">
    
    <div v-if="loading" class="flex-grow-1 d-flex align-items-center justify-content-center" style="min-height: 50vh;">
      <div class="spinner-border text-dark" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="!product" class="flex-grow-1 d-flex flex-column align-items-center justify-content-center text-center py-5">
      <i class="bi bi-exclamation-circle display-1 text-muted mb-3"></i>
      <h3>Product Not Found</h3>
      <button @click="$router.push('/shop')" class="btn btn-dark mt-3 rounded-pill px-4">Back to Shop</button>
    </div>

    <div v-else class="flex-grow-1 pb-5 mb-5 mb-lg-0">
      
      <div class="container px-lg-5 pt-4 pb-2">
        <nav aria-label="breadcrumb">
          <ol class="breadcrumb bg-transparent p-0 mb-0 small text-muted text-uppercase tracking-wide">
            <li class="breadcrumb-item"><a href="#" class="text-decoration-none text-muted hover-dark" @click.prevent="handleNavigation('home')">Home</a></li>
            <li class="breadcrumb-item"><a href="#" class="text-decoration-none text-muted hover-dark" @click.prevent="handleNavigation('shop')">Shop</a></li>
            <li class="breadcrumb-item"><a href="#" class="text-decoration-none text-muted hover-dark">Furniture</a></li>
            <li class="breadcrumb-item active text-dark fw-bold" aria-current="page">{{ product.name }}</li>
          </ol>
        </nav>
      </div>

      <section class="container px-lg-5 py-4">
        <div class="row g-5">
          
          <div class="col-lg-7">
            <div class="row g-2 sticky-lg-top" style="top: 100px; z-index: 0;">
              
              <div class="col-lg-2 d-none d-lg-flex flex-column gap-3 order-1">
                <div 
                  v-for="(img, index) in product.images" 
                  :key="index"
                  class="thumbnail-wrapper cursor-pointer border transition-all"
                  :class="{ 'border-dark': currentImage === img, 'border-transparent': currentImage !== img }"
                  @click="currentImage = img"
                >
                  <img :src="img" class="w-100 h-100 object-fit-cover" :alt="product.name">
                </div>
              </div>

              <div class="col-lg-10 order-2">
                <div class="main-image-wrapper bg-light position-relative overflow-hidden cursor-zoom-in group">
                  <img :src="currentImage" class="w-100 h-100 object-fit-cover transition-transform" :alt="product.name">
                  <span v-if="product.badge" class="position-absolute top-0 start-0 m-3 badge bg-white text-dark text-uppercase tracking-wide rounded-0 shadow-sm">{{ product.badge }}</span>
                </div>
              </div>

              <div class="col-12 d-lg-none order-3 mt-3">
                <div class="d-flex gap-2 overflow-auto hide-scrollbar">
                  <div 
                    v-for="(img, index) in product.images" 
                    :key="'mob-'+index"
                    class="mobile-thumb rounded-3 overflow-hidden border"
                    :class="{ 'border-dark': currentImage === img }"
                    @click="currentImage = img"
                    style="min-width: 80px; width: 80px; height: 80px;"
                  >
                    <img :src="img" class="w-100 h-100 object-fit-cover">
                  </div>
                </div>
              </div>

            </div>
          </div>

          <div class="col-lg-5">
            <div class="ps-lg-4 sticky-lg-top" style="top: 100px;">
              
              <div class="mb-4">
                <div class="d-flex align-items-center gap-2 mb-2">
                  <span class="text-uppercase tracking-wide text-muted extra-small fw-bold">SKU: {{ product.sku }}</span>
                  <span class="text-success extra-small fw-bold border border-success px-2 py-0 rounded-pill" v-if="product.inStock">In Stock</span>
                </div>
                <h1 class="display-5 fw-bold mb-2">{{ product.name }}</h1>
                <p class="text-muted lead fs-6">{{ product.tagline }}</p>
                
                <div class="d-flex align-items-center gap-3 mt-3">
                  <h3 class="fw-bold mb-0">${{ product.originalPrice || product.price }}</h3>
                  <span v-if="product.originalPrice" class="text-muted text-decoration-line-through fs-5">${{ product.price }}</span>
                  <span v-if="product.originalPrice" class="badge bg-danger rounded-pill px-3">-{{ discountPercentage }}%</span>
                </div>

                <div class="d-flex align-items-center gap-2 mt-3 cursor-pointer" @click="scrollToReviews">
                  <div class="d-flex text-warning">
                    <i class="bi bi-star-fill" v-for="n in 5" :key="n" :class="{'text-muted opacity-25': n > product.rating}"></i>
                  </div>
                  <span class="text-muted small text-decoration-underline">{{ product.reviewCount }} Reviews</span>
                </div>
              </div>

              <hr class="opacity-10 my-4">

              <div class="mb-4">
                <label class="fw-bold small text-uppercase mb-2">Color: {{ selectedColor }}</label>
                <div class="d-flex gap-2">
                  <button 
                    v-for="color in product.colors" 
                    :key="color.name"
                    class="btn rounded-circle p-0 border-2"
                    :class="selectedColor === color.name ? 'border-dark' : 'border-transparent'"
                    style="width: 32px; height: 32px; padding: 2px !important;"
                    @click="selectedColor = color.name"
                  >
                    <span class="d-block w-100 h-100 rounded-circle border" :style="{ backgroundColor: color.hex }"></span>
                  </button>
                </div>
              </div>

              <div class="row g-2 mb-4">
                <div class="col-4 col-md-3">
                  <div class="input-group h-100">
                    <button class="btn btn-outline-dark rounded-0 px-2" @click="quantity > 1 ? quantity-- : null">-</button>
                    <input type="text" class="form-control text-center border-dark border-start-0 border-end-0 rounded-0 bg-transparent fw-bold" v-model="quantity" readonly>
                    <button class="btn btn-outline-dark rounded-0 px-2" @click="quantity++">+</button>
                  </div>
                </div>
                <div class="col-8 col-md-9">
                  <button class="btn btn-dark w-100 h-100 rounded-0 text-uppercase fw-bold tracking-wide hover-lift" @click="addToCart">
                    Add to Cart
                  </button>
                </div>
                <div class="col-12 mt-2">
                  <button class="btn btn-outline-dark w-100 rounded-0 text-uppercase fw-bold tracking-wide">Buy Now</button>
                </div>
              </div>

              <div class="row g-3 mb-5 border-top border-bottom py-4 text-center text-sm-start">
                <div class="col-6 col-sm-4">
                  <div class="d-flex flex-column flex-sm-row align-items-center gap-2">
                    <i class="bi bi-truck fs-4 text-muted"></i>
                    <div class="text-center text-sm-start">
                      <span class="d-block fw-bold small">Free Shipping</span>
                      <span class="d-block text-muted extra-small">On orders over $150</span>
                    </div>
                  </div>
                </div>
                <div class="col-6 col-sm-4">
                  <div class="d-flex flex-column flex-sm-row align-items-center gap-2">
                    <i class="bi bi-shield-check fs-4 text-muted"></i>
                    <div class="text-center text-sm-start">
                      <span class="d-block fw-bold small">2 Year Warranty</span>
                      <span class="d-block text-muted extra-small">Full coverage</span>
                    </div>
                  </div>
                </div>
                <div class="col-6 col-sm-4">
                  <div class="d-flex flex-column flex-sm-row align-items-center gap-2">
                    <i class="bi bi-arrow-repeat fs-4 text-muted"></i>
                    <div class="text-center text-sm-start">
                      <span class="d-block fw-bold small">Free Returns</span>
                      <span class="d-block text-muted extra-small">Within 30 days</span>
                    </div>
                  </div>
                </div>
              </div>

              <div class="accordion accordion-flush border-bottom" id="productAccordion">
                <div class="accordion-item">
                  <h2 class="accordion-header">
                    <button class="accordion-button collapsed fw-bold text-uppercase small py-3" type="button" data-bs-toggle="collapse" data-bs-target="#descCollapse">Description</button>
                  </h2>
                  <div id="descCollapse" class="accordion-collapse collapse" data-bs-parent="#productAccordion">
                    <div class="accordion-body text-muted small lh-lg">{{ product.description }}</div>
                  </div>
                </div>
                <div class="accordion-item">
                  <h2 class="accordion-header">
                    <button class="accordion-button collapsed fw-bold text-uppercase small py-3" type="button" data-bs-toggle="collapse" data-bs-target="#specsCollapse">Dimensions & Specs</button>
                  </h2>
                  <div id="specsCollapse" class="accordion-collapse collapse" data-bs-parent="#productAccordion">
                    <div class="accordion-body text-muted small">
                      <table class="table table-sm table-borderless mb-0">
                        <tbody>
                          <tr v-for="(val, key) in product.specs" :key="key">
                            <td class="text-muted">{{ key }}</td>
                            <td class="fw-medium text-dark text-end">{{ val }}</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
                <div class="accordion-item">
                  <h2 class="accordion-header">
                    <button class="accordion-button collapsed fw-bold text-uppercase small py-3" type="button" data-bs-toggle="collapse" data-bs-target="#careCollapse">Care Instructions</button>
                  </h2>
                  <div id="careCollapse" class="accordion-collapse collapse" data-bs-parent="#productAccordion">
                    <div class="accordion-body text-muted small lh-lg">{{ product.care }}</div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </section>

      <section class="container px-lg-5 py-5 border-top mt-5 position-relative scroll-group">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h3 class="fw-bold m-0">Complete the Look</h3>
          <a href="#" class="btn-link-dark text-decoration-none fw-bold small">View All</a>
        </div>
        
        <div class="position-relative">
          <button class="btn btn-light rounded-circle shadow-sm position-absolute top-50 start-0 translate-middle-y ms-n3 z-2 d-none d-md-flex align-items-center justify-content-center scroll-arrow" style="width: 40px; height: 40px;" @click="scrollRelated('left')">
            <i class="bi bi-chevron-left"></i>
          </button>
          
          <div class="row flex-nowrap overflow-auto hide-scrollbar pb-3 g-4" ref="relatedScrollContainer" style="scroll-behavior: smooth;">
            <div class="col-10 col-md-4 col-lg-3" style="flex: 0 0 auto;" v-for="related in relatedProducts" :key="related.id">
              
              <ProductCard 
                :product="related" 
                @click-product="handleRelatedClick" 
                @add-to-cart="addToCart" 
              />

            </div>
          </div>

          <button class="btn btn-light rounded-circle shadow-sm position-absolute top-50 end-0 translate-middle-y me-n3 z-2 d-none d-md-flex align-items-center justify-content-center scroll-arrow" style="width: 40px; height: 40px;" @click="scrollRelated('right')">
            <i class="bi bi-chevron-right"></i>
          </button>
        </div>
      </section>

    </div>

    <div v-if="product" class="d-lg-none fixed-bottom bg-white border-top shadow-lg p-3 animate-slide-up" style="z-index: 10;">
      <div class="d-flex gap-2">
        <div class="d-flex flex-column justify-content-center">
          <span class="fw-bold small">${{ product.originalPrice || product.price }}</span>
          <span class="text-muted extra-small text-uppercase">Free Shipping</span>
        </div>
        <button class="btn btn-dark w-100 rounded-pill fw-bold text-uppercase" @click="addToCart">Add to Cart</button>
      </div>
    </div>

  </div>
</template>

<script>
import ProductCard from '@/components/ProductCard.vue';
import api from "@/services/api";

export default {
  name: "ProductDetails",
  components: {
    ProductCard
  },
  data() {
    return {
      loading: true,
      quantity: 1,
      selectedColor: "",
      currentImage: "",
      product: {
        id: null,
        name: "",
        tagline: "",
        sku: "",
        price: 0,
        originalPrice: null,
        inStock: true,
        rating: 0,
        reviewCount: 0,
        badge: null,
        description: "",
        care: "",
        images: [],
        colors: [],
        specs: {}
      },
      relatedProducts: []
    };
  },
  computed: {
    discountPercentage() {
      // Swapped logic: ((Price - OriginalPrice) / Price)
      if (!this.product.originalPrice) return 0;
      return Math.round(((this.product.price - this.product.originalPrice) / this.product.price) * 100);
    }
  },
  watch: {
    '$route.params.id': {
      handler: 'loadPageData',
      immediate: true
    }
  },
  methods: {
    async loadPageData() {
      this.loading = true;
      const productId = this.$route.params.id;
      
      try {
        const resProduct = await api.get(`/products/${productId}`);
        this.product = resProduct.data.data;
        
        if (this.product.images.length > 0) this.currentImage = this.product.images[0];
        if (this.product.colors.length > 0) this.selectedColor = this.product.colors[0].name;

        const resRelated = await api.get(`/products/${productId}/related`);
        this.relatedProducts = resRelated.data.data;

      } catch (err) {
        console.error("Failed to load product", err);
      } finally {
        this.loading = false;
      }
    },

    async addToCart() {
      try {
        await api.post(`/user/cart/${this.product.id}`, { quantity: this.quantity });
        alert("Added to cart successfully!");
      } catch (err) {
        if (err.response && err.response.status === 401) {
          alert("Please login to add items to cart.");
          this.$router.push('/login');
        } else {
          alert("Failed to add to cart.");
        }
      }
    },

    // 1. Navigation Handler
    handleRelatedClick(p) {
      this.$router.push(`/product/${p.id}`);
      window.scrollTo({ top: 0, behavior: 'smooth' }); // Scroll to top when changing products
    },

    handleNavigation(page) {
      if (page === 'home') this.$router.push('/');
      if (page === 'shop') this.$router.push('/shop');
    },

    scrollToReviews() {
      // Logic for scrolling to review section
    },

    scrollRelated(direction) {
      const container = this.$refs.relatedScrollContainer;
      const scrollAmount = container.clientWidth * 0.75; 
      if (direction === 'left') {
        container.scrollLeft -= scrollAmount;
      } else {
        container.scrollLeft += scrollAmount;
      }
    }
  }
};
</script>

<style scoped>
/* EDITORIAL / PREMIUM STYLING */
.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }

.hover-dark:hover { color: #000 !important; }

.thumbnail-wrapper {
  width: 100%;
  aspect-ratio: 1/1;
  overflow: hidden;
}

.main-image-wrapper {
  aspect-ratio: 3/4; 
}
@media (min-width: 992px) {
  .main-image-wrapper { aspect-ratio: 4/3; } 
}

.transition-all { transition: all 0.3s ease; }
.transition-transform { transition: transform 0.5s ease; }
.group:hover .transition-transform { transform: scale(1.05); }
.cursor-zoom-in { cursor: zoom-in; }

.accordion-button {
  background-color: transparent;
  box-shadow: none;
  padding-left: 0;
  padding-right: 0;
  color: #000;
}
.accordion-button:not(.collapsed) {
  color: #000;
  background-color: transparent;
  box-shadow: none;
}
.accordion-item {
  border-left: 0;
  border-right: 0;
  border-top: 0;
  border-bottom: 1px solid rgba(0,0,0,0.1);
}

.hide-scrollbar::-webkit-scrollbar { display: none; }
.hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }

.hover-lift { transition: transform 0.2s; }
.hover-lift:hover { transform: translateY(-2px); }

.animate-slide-up {
  animation: slideUp 0.4s ease-out forwards;
}
@keyframes slideUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

.scroll-arrow {
  opacity: 1 !important; 
  transition: background-color 0.2s;
  background-color: rgba(255, 255, 255, 0.9);
  border: 1px solid #eee;
}
.scroll-arrow:hover {
  background-color: #fff;
  border-color: #000;
}

.ms-n3 { margin-left: -1rem; }
.me-n3 { margin-right: -1rem; }

.col-10.col-md-4.col-lg-3[style*="flex: 0 0 auto;"] {
  max-width: 300px;
}
</style>