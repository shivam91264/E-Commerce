<template>
  <div 
    class="card h-100 border-0 bg-transparent product-card group cursor-pointer" 
    @click="$emit('click-product', product)"
  >
    
    <div class="position-relative overflow-hidden mb-3 bg-light rounded-0 image-wrapper">
      
      <span 
        v-if="product.badge" 
        class="position-absolute top-0 start-0 m-3 badge bg-white text-dark shadow-sm rounded-0 text-uppercase tracking-wide z-2"
        style="font-size: 0.65rem;"
      >
        {{ product.badge }}
      </span>

      <img 
        :src="product.image || 'https://via.placeholder.com/300x400'" 
        class="w-100 h-100 object-fit-cover transition-transform" 
        :alt="product.name"
      >

      <div class="action-overlay position-absolute bottom-0 start-0 w-100 p-3 d-none d-lg-block z-2">
        <button 
          class="btn btn-white w-100 fw-bold shadow-sm rounded-0 text-uppercase small" 
          @click.stop="$emit('add-to-cart', product)"
        >
          Quick Add
        </button>
      </div>
      
      </div>

    <div class="card-body p-0">
      
      <div class="d-flex justify-content-between align-items-start mb-1">
        <h6 class="card-title fw-semibold mb-0 text-truncate text-dark" style="max-width: 70%;" :title="product.name">
          {{ product.name }}
        </h6>
        <span class="fw-bold small text-dark">${{ product.price }}</span>
      </div>

      <p class="text-muted small mb-2 text-truncate">{{ product.subtitle || product.category }}</p>

      <div class="d-flex align-items-center mb-3" v-if="product.rating">
        <i class="bi bi-star-fill text-warning" style="font-size: 0.75rem;"></i>
        <span class="ms-1 text-muted extra-small">{{ product.rating }}</span>
      </div>

      <button 
        class="btn btn-outline-dark btn-sm w-100 d-lg-none rounded-0" 
        @click.stop="$emit('add-to-cart', product)"
      >
        Add to Cart
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProductCard",
  props: {
    product: {
      type: Object,
      required: true
    }
  }
};
</script>

<style scoped>
/* PREMIUM DESIGN TOKENS */
.tracking-wide { letter-spacing: 0.1em; }
.extra-small { font-size: 0.75rem; }

/* Aspect Ratio */
.image-wrapper {
  aspect-ratio: 3/4;
  position: relative;
}

/* Image Zoom Effect */
.transition-transform {
  transition: transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
.group:hover .transition-transform {
  transform: scale(1.05);
}

/* Hover Overlay Button */
.action-overlay {
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.3s ease;
  background: linear-gradient(to top, rgba(0,0,0,0.05), transparent);
}

.group:hover .action-overlay {
  opacity: 1;
  transform: translateY(0);
}

/* Button Styling */
.btn-white {
  background-color: rgba(255, 255, 255, 0.95);
  color: #000;
  border: none;
  transition: all 0.2s;
}
.btn-white:hover {
  background-color: #000;
  color: #fff;
}

/* Cursor Pointer for Clickability */
.cursor-pointer {
  cursor: pointer;
}
</style>