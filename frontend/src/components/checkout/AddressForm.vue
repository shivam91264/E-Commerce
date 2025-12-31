<template>
  <form class="row g-3">
    <div class="col-12">
      <div class="form-floating">
        <input type="email" class="form-control bg-light-input border-0" id="email" placeholder="name@example.com" value="user@example.com">
        <label for="email">Email Address</label>
      </div>
    </div>

    <div class="col-12">
      <div class="form-floating">
        <input type="text" class="form-control bg-light-input border-0" id="fullName" placeholder="John Doe">
        <label for="fullName">Full Name</label>
      </div>
    </div>

    <div class="col-12">
      <div class="form-floating">
        <input type="text" class="form-control bg-light-input border-0" id="address" placeholder="123 Main St">
        <label for="address">Address Line 1</label>
      </div>
    </div>

    <div class="col-md-5">
      <div class="form-floating">
        <input type="text" class="form-control bg-light-input border-0" id="city" placeholder="New York">
        <label for="city">City</label>
      </div>
    </div>
    <div class="col-md-4">
      <div class="form-floating">
        <select class="form-select bg-light-input border-0" id="state">
          <option selected>State</option>
          <option>CA</option>
          <option>NY</option>
          <option>TX</option>
        </select>
        <label for="state">State</label>
      </div>
    </div>
    <div class="col-md-3">
      <div class="form-floating">
        <input type="text" class="form-control bg-light-input border-0" id="zip" placeholder="Zip">
        <label for="zip">Zip Code</label>
      </div>
    </div>

    <div class="col-12">
      <div class="form-floating">
        <input type="tel" class="form-control bg-light-input border-0" id="phone" placeholder="Phone">
        <label for="phone">Phone Number</label>
      </div>
    </div>

    <div class="col-12">
      <div class="form-check">
        <input class="form-check-input" type="checkbox" id="saveInfo">
        <label class="form-check-label small text-muted" for="saveInfo">
          Save this information for next time
        </label>
      </div>
    </div>
  </form>
</template>

<style scoped>
/* Custom Input Styling for Premium Feel */
.bg-light-input {
  background-color: #f3f4f6;
  border-radius: 4px;
}
.form-control:focus, .form-select:focus {
  background-color: #fff;
  box-shadow: 0 0 0 2px rgba(0,0,0,0.1); /* Subtle focus ring */
}
label { color: #6c757d; }
</style>