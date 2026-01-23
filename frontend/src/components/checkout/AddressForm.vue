<template>
  <form class="row g-3">
    <div class="col-12">
      <div class="form-floating">
        <input type="text" class="form-control bg-light-input border-0" id="fullName" placeholder="John Doe" 
               v-model="localData.full_name" @input="updateParent">
        <label for="fullName">Full Name</label>
      </div>
    </div>

    <div class="col-12">
      <div class="form-floating">
        <input type="text" class="form-control bg-light-input border-0" id="address" placeholder="123 Main St"
               v-model="localData.address_line1" @input="updateParent">
        <label for="address">Address Line 1</label>
      </div>
    </div>
    
    <div class="col-12">
      <div class="form-floating">
        <input type="text" class="form-control bg-light-input border-0" id="address2" placeholder="Suite"
               v-model="localData.address_line2" @input="updateParent">
        <label for="address2">Address Line 2 (Optional)</label>
      </div>
    </div>

    <div class="col-md-5">
      <div class="form-floating">
        <input type="text" class="form-control bg-light-input border-0" id="city" placeholder="New York"
               v-model="localData.city" @input="updateParent">
        <label for="city">City</label>
      </div>
    </div>
    <div class="col-md-4">
      <div class="form-floating">
        <select class="form-select bg-light-input border-0" id="state" v-model="localData.state" @change="updateParent">
          <option value="" disabled>State</option>
          <option>CA</option>
          <option>NY</option>
          <option>TX</option>
          </select>
        <label for="state">State</label>
      </div>
    </div>
    <div class="col-md-3">
      <div class="form-floating">
        <input type="text" class="form-control bg-light-input border-0" id="zip" placeholder="Zip"
               v-model="localData.zip_code" @input="updateParent">
        <label for="zip">Zip Code</label>
      </div>
    </div>

    <div class="col-12">
      <div class="form-floating">
        <input type="tel" class="form-control bg-light-input border-0" id="phone" placeholder="Phone"
               v-model="localData.phone" @input="updateParent">
        <label for="phone">Phone Number</label>
      </div>
    </div>
  </form>
</template>

<script>
export default {
  props: ['modelValue'],
  emits: ['update:modelValue'],
  data() {
    return {
      localData: { ...this.modelValue }
    };
  },
  watch: {
    modelValue: {
      handler(newVal) {
        this.localData = { ...newVal };
      },
      deep: true
    }
  },
  methods: {
    updateParent() {
      this.$emit('update:modelValue', this.localData);
    }
  }
};
</script>

<style scoped>
.bg-light-input { background-color: #f3f4f6; border-radius: 4px; }
.form-control:focus, .form-select:focus { background-color: #fff; box-shadow: 0 0 0 2px rgba(0,0,0,0.1); }
label { color: #6c757d; }
</style>