<template>
  <div class="cart-item py-4 border-bottom">
    <div class="row align-items-center gy-3">
      
      <div class="col-4 col-md-2">
        <div class="ratio ratio-3x4 bg-light rounded-2 overflow-hidden cursor-pointer" @click="$emit('click-item')">
          <img :src="item.image" :alt="item.name" class="object-fit-cover w-100 h-100">
        </div>
      </div>

      <div class="col-8 col-md-4">
        <div class="d-flex flex-column h-100 justify-content-center">
          <h6 class="fw-bold text-dark mb-1 text-truncate cursor-pointer" @click="$emit('click-item')">
            {{ item.name }}
          </h6>
          <p class="text-muted small mb-2 text-truncate">{{ item.variant }}</p>
          <div class="d-flex align-items-center gap-3 mt-1">
              <button class="btn btn-link text-muted p-0 text-decoration-none extra-small text-uppercase tracking-wide" @click="$emit('remove')">
                <i class="bi bi-trash me-1"></i> Remove
              </button>
              </div>
        </div>
      </div>

      <div class="col-12 col-md-6">
        <div class="d-flex align-items-center justify-content-between justify-content-md-end gap-md-5">
          
          <div class="input-group" style="width: 110px;">
            <button class="btn btn-outline-secondary btn-sm border-end-0 rounded-start-pill px-3" @click="updateQty(-1)" :disabled="item.quantity <= 1">-</button>
            <input type="text" class="form-control form-control-sm text-center border-secondary border-start-0 border-end-0 bg-transparent" :value="item.quantity" readonly>
            <button class="btn btn-outline-secondary btn-sm border-start-0 rounded-end-pill px-3" @click="updateQty(1)">+</button>
          </div>

          <div class="text-end" style="min-width: 80px;">
            <span class="d-block fw-bold">${{ (item.price * item.quantity).toFixed(2) }}</span>
            <span class="d-block text-muted extra-small" v-if="item.quantity > 1">${{ item.price }} each</span>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: "CartItem",
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  methods: {
    updateQty(change) {
      // Note: Ensure parent passes item.product_id if item.id is not correct based on previous context
      this.$emit('update-quantity', this.item.id, this.item.quantity + change);
    }
  }
};
</script>

<style scoped>
/* Typography */
.extra-small { font-size: 0.75rem; }
.tracking-wide { letter-spacing: 0.05em; }

/* Transitions */
.cart-item { transition: background-color 0.2s; }
.cart-item:hover { background-color: #fafafa; }

.cursor-pointer { cursor: pointer; }
</style>