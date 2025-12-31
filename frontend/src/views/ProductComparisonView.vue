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
          <div class="d-flex flex-column flex-md-row justify-content-between align-items-end animate-fade-up">
            <div class="mb-4 mb-md-0 text-center text-md-start w-100">
              <span class="d-block text-muted extra-small text-uppercase tracking-wide fw-bold mb-2">
                Make the right choice
              </span>
              <h1 class="display-5 fw-bold tracking-tight mb-2 text-dark">
                Compare Products
              </h1>
              <p class="text-muted lead fs-6 mb-0" style="max-width: 600px;">
                Compare features, specs, and prices side-by-side to find the perfect match for your needs.
              </p>
            </div>
            
            <div v-if="compareList.length > 0" class="w-100 w-md-auto text-center">
              <button @click="clearComparison" class="btn btn-outline-danger border-0 btn-sm text-uppercase fw-bold tracking-wide rounded-pill px-4 hover-lift">
                <i class="bi bi-trash me-2"></i> Clear Comparison
              </button>
            </div>
          </div>
        </div>
      </header>

      <div class="container px-lg-5 py-5">
        
        <div v-if="compareList.length === 0" class="text-center py-6 animate-fade-up">
          <div class="d-inline-flex p-4 rounded-circle bg-light mb-4">
            <i class="bi bi-arrow-left-right display-4 text-muted opacity-50"></i>
          </div>
          <h3 class="fw-bold mb-3">No products selected</h3>
          <p class="text-muted mb-4 mx-auto" style="max-width: 450px;">
            Your comparison list is empty. Browse products and click the "Compare" icon to add them here.
          </p>
          <button class="btn btn-dark rounded-pill px-5 py-3 text-uppercase fw-bold tracking-wide hover-lift" @click="goShop">
            Go to Shop
          </button>
        </div>

        <div v-else class="animate-fade-up">
          
          <div class="table-responsive custom-scrollbar pb-3">
            <table class="table table-borderless align-middle mb-0" style="min-width: 800px;">
              
              <thead>
                <tr>
                  <th class="sticky-col bg-white p-4" style="width: 200px; vertical-align: bottom;">
                    <span class="text-muted text-uppercase extra-small tracking-wide fw-bold">Product Summary</span>
                  </th>
                  
                  <th v-for="product in compareList" :key="product.id" class="p-4" style="width: 280px;">
                    <div class="position-relative product-header-card text-center">
                      <button @click="removeProduct(product.id)" class="btn-remove position-absolute top-0 end-0 btn btn-sm btn-light rounded-circle shadow-sm" title="Remove">
                        <i class="bi bi-x-lg small"></i>
                      </button>

                      <div class="mb-3 d-flex justify-content-center align-items-center" style="height: 160px;">
                        <img :src="product.image" :alt="product.name" class="img-fluid mh-100 object-fit-contain">
                      </div>

                      <h5 class="fw-bold text-dark mb-1">{{ product.name }}</h5>
                      <div class="mb-2">
                        <span class="text-warning small"><i class="bi bi-star-fill"></i> {{ product.rating }}</span>
                        <span class="text-muted small ms-1">({{ product.reviews }} reviews)</span>
                      </div>
                      <div class="h5 fw-bold mb-3">${{ product.price }}</div>
                      
                      <button class="btn btn-dark w-100 rounded-pill py-2 text-uppercase extra-small fw-bold tracking-wide hover-lift">
                        View Details
                      </button>
                    </div>
                  </th>
                </tr>
              </thead>

              <tbody>
                <template v-for="(category, catIndex) in specCategories" :key="catIndex">
                  
                  <tr class="bg-light-subtle">
                    <td class="sticky-col bg-light-subtle py-3 px-4" colspan="100%">
                      <span class="fw-bold text-uppercase tracking-wide small text-dark">{{ category.title }}</span>
                    </td>
                  </tr>

                  <tr v-for="(spec, specIndex) in category.specs" :key="specIndex" class="border-bottom border-light">
                    <td class="sticky-col bg-white py-3 px-4">
                      <span class="text-muted small fw-bold">{{ spec.label }}</span>
                    </td>
                    
                    <td v-for="product in compareList" :key="product.id" class="py-3 px-4 text-center">
                      <span v-if="typeof product.specs[spec.key] === 'boolean'">
                        <i v-if="product.specs[spec.key]" class="bi bi-check-circle-fill text-success lead"></i>
                        <i v-else class="bi bi-dash-circle text-muted opacity-25 lead"></i>
                      </span>
                      <span v-else class="text-dark small fw-medium">
                        {{ product.specs[spec.key] || '—' }}
                      </span>
                    </td>
                  </tr>
                </template>
                
                <tr>
                  <td class="sticky-col bg-white border-0 pt-4"></td>
                  <td v-for="product in compareList" :key="'action-'+product.id" class="border-0 pt-4 px-3">
                    <button class="btn btn-outline-dark w-100 rounded-0 py-3 text-uppercase extra-small fw-bold tracking-wide">
                      Add to Cart
                    </button>
                  </td>
                </tr>

              </tbody>
            </table>
          </div>

        </div>

      </div>
    </main>

    <PremiumFooter @navigate="handleNavigation" />

  </div>
</template>

<script>
import PremiumNavbar from '@/components/Navbar.vue';
import PremiumFooter from '@/components/Footer.vue';

export default {
  name: "ProductComparisonView",
  components: {
    PremiumNavbar,
    PremiumFooter
  },
  data() {
    return {
      // Mock Data: 3 Smartphones
      compareList: [
        {
          id: 101,
          name: "ProPhone 14",
          price: 999,
          rating: 4.8,
          reviews: 124,
          image: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=400&q=80",
          specs: {
            display: "6.1-inch OLED",
            resolution: "2532 x 1170 px",
            processor: "A15 Bionic",
            ram: "6 GB",
            storage: "128GB / 256GB / 512GB",
            battery: "3200 mAh",
            camera: "12MP Dual System",
            waterResist: true,
            material: "Aluminum & Glass",
            warranty: "1 Year"
          }
        },
        {
          id: 102,
          name: "Galaxy Ultra S23",
          price: 1199,
          rating: 4.9,
          reviews: 89,
          image: "https://images.unsplash.com/photo-1610945265078-3853eadab529?auto=format&fit=crop&w=400&q=80",
          specs: {
            display: "6.8-inch Dynamic AMOLED",
            resolution: "3088 x 1440 px",
            processor: "Snapdragon 8 Gen 2",
            ram: "12 GB",
            storage: "256GB / 512GB / 1TB",
            battery: "5000 mAh",
            camera: "200MP Quad System",
            waterResist: true,
            material: "Armor Aluminum",
            warranty: "1 Year"
          }
        },
        {
          id: 103,
          name: "Pixel Pro 7",
          price: 899,
          rating: 4.6,
          reviews: 210,
          image: "https://images.unsplash.com/photo-1598327105666-5b89351aff70?auto=format&fit=crop&w=400&q=80",
          specs: {
            display: "6.7-inch LTPO OLED",
            resolution: "3120 x 1440 px",
            processor: "Google Tensor G2",
            ram: "12 GB",
            storage: "128GB / 256GB",
            battery: "5000 mAh",
            camera: "50MP Triple System",
            waterResist: true,
            material: "Recycled Aluminum",
            warranty: "2 Years"
          }
        }
      ],
      
      // Configuration for the rows
      specCategories: [
        {
          title: "Display & Design",
          specs: [
            { label: "Screen Size", key: "display" },
            { label: "Resolution", key: "resolution" },
            { label: "Body Material", key: "material" }
          ]
        },
        {
          title: "Performance",
          specs: [
            { label: "Processor", key: "processor" },
            { label: "RAM", key: "ram" },
            { label: "Storage Options", key: "storage" }
          ]
        },
        {
          title: "Camera & Battery",
          specs: [
            { label: "Main Camera", key: "camera" },
            { label: "Battery Capacity", key: "battery" },
            { label: "Water Resistant", key: "waterResist" }
          ]
        },
        {
          title: "Other",
          specs: [
            { label: "Warranty", key: "warranty" }
          ]
        }
      ]
    };
  },
  methods: {
    handleNavigation(page) {
      console.log(`Navigating to: ${page}`);
    },
    removeProduct(id) {
      this.compareList = this.compareList.filter(p => p.id !== id);
    },
    clearComparison() {
      if(confirm("Are you sure you want to clear the comparison list?")) {
        this.compareList = [];
      }
    },
    goShop() {
      // Logic to navigate to Shop view
      console.log("Navigating to Shop");
    }
  }
};
</script>

<style scoped>
/* 🎨 VISUAL STYLE GUIDELINES */

/* Backgrounds */
.bg-light-subtle { background-color: #f9fafb !important; }

/* Typography */
.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }

/* Spacing */
.py-6 { padding-top: 5rem; padding-bottom: 5rem; }

/* Animations */
.animate-fade-up {
  animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
  transform: translateY(20px);
}
@keyframes fadeUp {
  to { opacity: 1; transform: translateY(0); }
}

/* Button Interactions */
.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.btn-remove {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.7;
  transition: all 0.2s;
}
.btn-remove:hover {
  opacity: 1;
  background-color: #dc3545;
  color: white;
}

/* 🖼️ TABLE STYLING */

/* Scrollbar styling for the table container */
.custom-scrollbar::-webkit-scrollbar {
  height: 8px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #ddd; 
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #bbb; 
}

/* Sticky Column Logic */
/* This ensures the first column stays fixed while scrolling right on mobile */
.sticky-col {
  position: -webkit-sticky;
  position: sticky;
  left: 0;
  z-index: 10;
  /* Add a subtle shadow to separate sticky col from content */
  box-shadow: 2px 0 5px -2px rgba(0,0,0,0.05);
  border-right: 1px solid rgba(0,0,0,0.05);
}

/* Remove default table border color issues */
.table > :not(caption) > * > * {
  box-shadow: none;
}
</style>