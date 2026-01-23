<template>
  <div class="card border-0 shadow-sm rounded-3 sticky-lg-top" style="top: 100px; z-index: 1;">
    <div class="card-body p-4">
      <h5 class="fw-bold mb-4">Order Summary</h5>

      <div v-if="loading" class="text-center py-4">
        <div class="spinner-border spinner-border-sm text-muted" role="status"></div>
      </div>

      <div class="d-flex flex-column gap-3 mb-4" v-else>
        <div v-for="item in items" :key="item.product_id" class="d-flex gap-3 align-items-center">
          <div class="position-relative" style="width: 60px; height: 60px;">
            <img :src="item.image" class="w-100 h-100 object-fit-cover rounded-2 border">
            <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-dark border border-white">
              {{ item.quantity }}
            </span>
          </div>
          <div class="flex-grow-1">
            <h6 class="mb-0 small fw-bold text-truncate" style="max-width: 150px;">{{ item.name }}</h6>
            <span class="text-muted extra-small">Qty: {{ item.quantity }}</span>
          </div>
          <span class="small fw-bold">${{ (item.price * item.quantity).toFixed(2) }}</span>
        </div>
      </div>

      <div class="input-group mb-4">
        <input type="text" class="form-control form-control-sm" placeholder="Gift card or discount code">
        <button class="btn btn-dark btn-sm px-3">Apply</button>
      </div>

      <hr class="border-secondary opacity-10">

      <div class="d-flex justify-content-between mb-2 small">
        <span class="text-muted">Subtotal</span>
        <span class="fw-bold">${{ subtotal.toFixed(2) }}</span>
      </div>
      <div class="d-flex justify-content-between mb-2 small">
        <span class="text-muted">Shipping</span>
        <span class="fw-bold" :class="shipping === 0 ? 'text-success' : ''">
          {{ shipping === 0 ? 'Free' : `$${shipping.toFixed(2)}` }}
        </span>
      </div>
      <div class="d-flex justify-content-between mb-4 small">
        <span class="text-muted">Taxes</span>
        <span class="fw-bold">$0.00</span>
      </div>

      <hr class="border-secondary opacity-10">

      <div class="d-flex justify-content-between align-items-center mb-4">
        <span class="fs-5 fw-bold">Total</span>
        <div>
          <span class="text-muted extra-small me-2">USD</span>
          <span class="fs-4 fw-bold">${{ total.toFixed(2) }}</span>
        </div>
      </div>

      <button 
        class="btn btn-dark w-100 py-3 rounded-0 text-uppercase fw-bold tracking-wide d-none d-lg-block hover-lift" 
        @click="$emit('place-order')"
      >
        Place Order
      </button>

    </div>
  </div>
</template>

<script>
export default {
  name: "OrderSummary",
  props: {
    items: { type: Array, default: () => [] },
    subtotal: { type: Number, default: 0 },
    shipping: { type: Number, default: 0 },
    total: { type: Number, default: 0 },
    loading: { type: Boolean, default: false }
  }
};
</script>

<style scoped>
.extra-small { font-size: 0.75rem; }
.hover-lift { transition: transform 0.2s; }
.hover-lift:hover { transform: translateY(-2px); }
</style>