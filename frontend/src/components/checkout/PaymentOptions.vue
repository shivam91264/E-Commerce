<template>
  <div>
    <div class="row g-3 mb-4">
      <div class="col-6 col-md-3" v-for="method in methods" :key="method.id">
        <div 
          class="card h-100 cursor-pointer border text-center py-3 transition-all"
          :class="selectedMethod === method.id ? 'border-dark bg-light' : 'border-light'"
          @click="selectedMethod = method.id"
        >
          <i :class="method.icon" class="fs-4 mb-2 d-block"></i>
          <span class="extra-small fw-bold text-uppercase">{{ method.name }}</span>
        </div>
      </div>
    </div>

    <div v-if="selectedMethod === 'card'" class="animate-fade-in">
      <div class="row g-3">
        <div class="col-12">
          <input type="text" class="form-control py-3" placeholder="Card Number" value="•••• •••• •••• 4242">
        </div>
        <div class="col-6">
          <input type="text" class="form-control py-3" placeholder="MM / YY" value="12 / 26">
        </div>
        <div class="col-6">
          <input type="text" class="form-control py-3" placeholder="CVC" value="•••">
        </div>
        <div class="col-12">
          <input type="text" class="form-control py-3" placeholder="Cardholder Name">
        </div>
      </div>
    </div>

    <div v-if="selectedMethod === 'cod'" class="alert alert-secondary border-0 mb-0 animate-fade-in">
      <i class="bi bi-info-circle me-2"></i> Pay securely with cash upon delivery.
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedMethod: 'card',
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

<style scoped>
.extra-small { font-size: 0.7rem; }
.transition-all { transition: all 0.2s; }
.animate-fade-in { animation: fadeIn 0.3s ease-out; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

/* Inputs */
.form-control {
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
}
.form-control:focus {
  background-color: #fff;
  border-color: #000;
  box-shadow: none;
}
</style>