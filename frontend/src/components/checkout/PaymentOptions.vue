<template>
  <div>
    <div class="row g-3 mb-4">
      <div class="col-6 col-md-3" v-for="method in methods" :key="method.id">
        <div 
          class="card h-100 cursor-pointer border text-center py-3 transition-all"
          :class="modelValue === method.id ? 'border-dark bg-light' : 'border-light'"
          @click="$emit('update:modelValue', method.id)"
        >
          <i :class="method.icon" class="fs-4 mb-2 d-block"></i>
          <span class="extra-small fw-bold text-uppercase">{{ method.name }}</span>
        </div>
      </div>
    </div>

    <div v-if="modelValue === 'card'" class="animate-fade-in">
       </div>
    
    <div v-if="modelValue === 'cod'" class="alert alert-secondary border-0 mb-0 animate-fade-in">
      <i class="bi bi-info-circle me-2"></i> Pay securely with cash upon delivery.
    </div>
  </div>
</template>

<script>
export default {
  props: ['modelValue'],
  emits: ['update:modelValue'],
  data() {
    return {
      methods: [
        { id: 'card', name: 'Card', icon: 'bi bi-credit-card' },
        { id: 'upi', name: 'UPI', icon: 'bi bi-qr-code' },
        { id: 'netbank', name: 'Net Bank', icon: 'bi bi-bank' },
        { id: 'cod', name: 'Cash', icon: 'bi bi-cash-stack' }
      ]
    };
  }
};
</script>