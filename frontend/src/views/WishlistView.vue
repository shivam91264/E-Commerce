<template>
  <div class="d-flex flex-column min-vh-100 bg-light-subtle">
    
    <main class="flex-grow-1 py-5">
      <div class="container px-lg-5">
        
        <div class="d-flex flex-column flex-md-row justify-content-between align-items-md-end mb-5 gap-4 animate-fade-up">
          <div class="text-center text-md-start">
            <h1 class="display-5 fw-bold tracking-tight mb-2">My Wishlist</h1>
            <p class="text-muted lead fs-6 mb-0">Your saved products are waiting — explore them anytime.</p>
          </div>

          <div class="d-flex align-items-center gap-3" v-if="wishlistItems.length > 0">
            <span class="text-muted extra-small text-uppercase tracking-wide fw-bold">
              {{ wishlistItems.length }} Items
            </span>
            <div class="vr opacity-25"></div>
            <button class="btn btn-link text-muted text-decoration-none extra-small text-uppercase tracking-wide fw-bold hover-dark p-0" @click="clearWishlist">
              Clear All
            </button>
          </div>
        </div>

        <div v-if="loading" class="text-center py-5">
           <div class="spinner-border text-dark" role="status"></div>
        </div>

        <div v-else-if="wishlistItems.length === 0" class="text-center py-6 animate-fade-up">
          <div class="bg-white d-inline-flex p-4 rounded-circle shadow-sm mb-4">
            <i class="bi bi-heart display-4 text-muted opacity-25"></i>
          </div>
          <h3 class="fw-bold mb-3">Your wishlist is empty</h3>
          <p class="text-muted mb-4" style="max-width: 400px; margin: 0 auto;">
            Tap the heart icon on products you love to save them for later.
          </p>
          <button class="btn btn-dark rounded-pill px-5 py-3 text-uppercase fw-bold tracking-wide hover-lift" @click="handleNavigation('shop')">
            Browse Products
          </button>
        </div>

        <div v-else class="row row-cols-1 row-cols-sm-2 row-cols-lg-4 g-4 g-lg-5">
          
          <div 
            class="col" 
            v-for="(product, index) in wishlistItems" 
            :key="product.id"
          >
            <div 
              class="position-relative animate-fade-up" 
              :style="{ animationDelay: `${index * 50}ms` }"
            >
              <ProductCard 
                :product="product" 
                @add-to-cart="moveToCart"
                @click-product="viewProductDetails"
              />

              <button 
                class="btn btn-white shadow-sm rounded-circle position-absolute top-0 end-0 mt-3 me-3 d-flex align-items-center justify-content-center hover-scale"
                style="width: 32px; height: 32px; z-index: 10;"
                @click.stop="removeFromWishlist(product.id)"
                title="Remove from Wishlist"
              >
                <i class="bi bi-x-lg text-muted extra-small"></i>
              </button>

              <span v-if="product.inStock" class="position-absolute top-0 start-0 mt-3 ms-3 badge bg-white text-success border border-success-subtle rounded-pill extra-small fw-bold px-2 py-1 shadow-sm" style="z-index: 10;">
                In Stock
              </span>
            </div>
          </div>

        </div>

      </div>
    </main>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import ProductCard from '@/components/ProductCard.vue';
import api from '@/services/api';

const router = useRouter();
const wishlistItems = ref([]);
const loading = ref(false);

// --- 1. Fetch Wishlist from API ---
const fetchWishlist = async () => {
  loading.value = true;
  try {
    const res = await api.get('/user/wishlist');
    
    // Map Backend Data to UI Format
    // The API returns structure: { data: [ { id: 1, product: { ... }, added_at: ... } ] }
    wishlistItems.value = res.data.data.map(item => {
      const p = item.product;
      
      return {
        id: p.id, // The Product ID (used for API calls)
        name: p.name,
        price: p.price,
        category: p.category_name || "General",
        image: p.image || "https://via.placeholder.com/300x400",
        
        // Stock Logic
        inStock: p.stock_quantity > 0,
        badge: (p.stock_quantity > 0 && p.stock_quantity < 5) ? "Low Stock" : "",
        
        // Important: Keep heart red in card
        is_wishlisted: true 
      };
    });

  } catch (err) {
    if (err.response && err.response.status === 401) {
      // alert("Please login to view your wishlist.");
      // router.push('/login');
    } else {
      console.error("Wishlist Load Error:", err);
    }
  } finally {
    loading.value = false;
  }
};

// --- 2. Move to Cart ---
const moveToCart = async (product) => {
  try {
    // API: /user/wishlist/move-to-cart
    await api.post('/user/wishlist/move-to-cart', { 
      product_id: product.id, 
      quantity: 1 
    });
    
    // UI Update: Remove from list immediately
    wishlistItems.value = wishlistItems.value.filter(item => item.id !== product.id);
    alert(`${product.name} moved to cart!`);
    
  } catch (err) {
    console.error("Move to Cart Error:", err);
    alert(err.response?.data?.msg || "Failed to move to cart.");
  }
};

// --- 3. Remove from Wishlist ---
const removeFromWishlist = async (productId) => {
  try {
    // API: DELETE /user/wishlist/<product_id>
    await api.delete(`/user/wishlist/${productId}`);
    
    // UI Update
    wishlistItems.value = wishlistItems.value.filter(item => item.id !== productId);
    
  } catch (err) {
    console.error("Remove Error:", err);
    alert("Failed to remove item.");
  }
};

// --- 4. Clear All ---
const clearWishlist = async () => {
  if (!confirm("Are you sure you want to clear your wishlist?")) return;
  
  try {
    await api.delete('/user/wishlist'); // API: DELETE /user/wishlist (clears all)
    wishlistItems.value = [];
  } catch (err) {
    console.error("Clear Error:", err);
    alert("Failed to clear wishlist.");
  }
};

// --- Navigation ---
const handleNavigation = (page) => {
  if (page === 'shop') router.push('/shop');
};

const viewProductDetails = (product) => {
  router.push(`/product/${product.id}`);
};

// --- Lifecycle ---
onMounted(() => {
  fetchWishlist();
});
</script>

<style scoped>
/* PREMIUM VISUAL LANGUAGE */

/* Backgrounds */
.bg-light-subtle { background-color: #f9fafb !important; }

/* Typography */
.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }

/* Buttons & Interactions */
.btn-white {
  background-color: #fff;
  border-color: #dee2e6;
  color: #000;
}
.btn-white:hover {
  border-color: #000;
  color: #000;
}

.hover-dark:hover {
  color: #000 !important;
  text-decoration: underline !important;
}

.hover-scale {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.hover-scale:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
}

.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* Animations */
.animate-fade-up {
  animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
  transform: translateY(20px);
}
@keyframes fadeUp {
  to { opacity: 1; transform: translateY(0); }
}

/* Spacing */
.py-6 { padding-top: 5rem; padding-bottom: 5rem; }
</style>