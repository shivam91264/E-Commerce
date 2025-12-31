<template>
  <div class="d-flex flex-column min-vh-100 bg-white">
    
    <PremiumNavbar 
      :is-authenticated="false" 
      :cart-item-count="3" 
      user-role="guest"
      @navigate="handleNavigation"
    />

    <main class="flex-grow-1">

      <header class="position-relative d-flex align-items-center justify-content-center text-center text-white overflow-hidden" style="height: 65vh; min-height: 550px;">
        <img 
          src="https://images.unsplash.com/photo-1590874103328-eac38a683ce7?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80" 
          alt="Modern Living" 
          class="position-absolute w-100 h-100 object-fit-cover"
          style="filter: brightness(0.7);"
        >
        
        <div class="container position-relative z-2 animate-fade-up">
          <div class="row justify-content-center">
            <div class="col-lg-9">
              <span class="d-inline-block border border-light border-opacity-50 px-3 py-1 rounded-pill text-uppercase tracking-wide extra-small fw-bold mb-4">
                Our Philosophy
              </span>
              <h1 class="display-3 fw-bolder tracking-tight mb-4">Curating the backdrop<br>for your life's best moments.</h1>
              <p class="lead fw-normal text-white-90 mb-5 mx-auto lh-base" style="max-width: 650px;">
                We believe that good design brings calm, clarity, and joy to the everyday. We exist to connect you with pieces crafted to last.
              </p>
            </div>
          </div>
        </div>
      </header>

      <section class="py-6 position-relative overflow-hidden">
        <div class="container px-lg-5">
          <div class="row align-items-center">
            
            <div class="col-lg-7">
              <div class="position-relative shadow-lg rounded-5 overflow-hidden" style="min-height: 600px;">
                <img 
                  src="https://images.unsplash.com/photo-1618221469555-7f3ad97540d6?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80" 
                  alt="Craftsmanship and Design" 
                  class="w-100 h-100 object-fit-cover position-absolute top-0 start-0"
                >
              </div>
            </div>
            
            <div class="col-lg-6 offset-lg-5 mt-n5 mt-lg-0" style="z-index: 2;">
              <div class="card border-0 shadow-xl p-4 p-md-5 rounded-4 bg-white ms-lg-n5">
                <div class="p-lg-2">
                  <span class="text-uppercase tracking-wide text-muted extra-small fw-bold mb-3 d-block">Why We Exist</span>
                  <h2 class="display-6 fw-bold mb-4">The antidote to disposable culture.</h2>
                  
                  <div class="border-start border-dark border-4 ps-4 mb-4">
                     <p class="lead text-dark fw-medium fst-italic mb-0">
                       "We grew tired of the choice between fast, temporary goods and inaccessible luxury. MarketHub was born in that gap."
                     </p>
                  </div>

                  <div class="text-muted lead fs-6 lh-lg space-y-4 mb-5">
                    <p>
                      We partner directly with creators, artisans, and independent brands who value craftsmanship, thoughtful materials, and timeless style over fleeting trends.
                    </p>
                    <p>
                      This isn't just a marketplace; it's a collection of stories. Every item we feature has a reason to exist.
                    </p>
                  </div>
                  
                  <div class="d-flex align-items-center gap-3">
                    <div>
                       <span class="fs-2" style="font-family: 'Times New Roman', serif; font-style: italic;">Alex & Sarah</span>
                       <span class="d-block text-muted small text-uppercase tracking-wide mt-1">Co-Founders</span>
                    </div>
                  </div>

                </div>
              </div>
            </div>
            
          </div>
        </div>
      </section>

      <section class="bg-light py-6">
        <div class="container px-lg-5">
          <div class="text-center mb-5 pb-3 animate-fade-up">
            <span class="text-uppercase tracking-wide text-muted extra-small fw-bold">Our Core Pillars</span>
            <h2 class="fw-bold mt-2 display-6 tracking-tight">Defined by Detail</h2>
          </div>

          <div class="row g-4">
            <div class="col-md-4" v-for="(value, index) in values" :key="index">
              <div class="card h-100 border-0 shadow-sm rounded-4 p-4 p-lg-5 text-center hover-lift transition-all bg-white group">
                <div class="mb-4 d-inline-flex align-items-center justify-content-center text-dark">
                  <i :class="value.icon" class="display-5 transition-transform group-hover:scale-110"></i>
                </div>
                <h5 class="fw-bold mb-3 text-uppercase tracking-wide small">{{ value.title }}</h5>
                <p class="text-muted mb-0 lh-lg px-lg-3">{{ value.desc }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="py-6">
         <div class="container px-lg-5">
            <div class="row align-items-center g-5">
               
               <div class="col-lg-5 animate-fade-up">
                  <span class="text-uppercase tracking-wide text-muted extra-small fw-bold mb-2 d-block">Our Commitment</span>
                  <h2 class="display-5 fw-bold mb-4 tracking-tight">Conscious by design.</h2>
                  <p class="lead text-muted mb-5">Good design shouldn't cost the earth. We are committed to transparency and sustainability at every step.</p>
                  
                  <ul class="list-unstyled space-y-4">
                     <li class="d-flex gap-3 align-items-start">
                        <i class="bi bi-check-circle-fill text-success mt-1"></i>
                        <div>
                           <strong class="d-block text-dark">Ethical Sourcing</strong>
                           <span class="text-muted small">We verify suppliers for fair labor and safe conditions.</span>
                        </div>
                     </li>
                     <li class="d-flex gap-3 align-items-start">
                        <i class="bi bi-check-circle-fill text-success mt-1"></i>
                        <div>
                           <strong class="d-block text-dark">Timeless over Trendy</strong>
                           <span class="text-muted small">Curating items meant to last years, not seasons.</span>
                        </div>
                     </li>
                  </ul>
               </div>

               <div class="col-lg-7">
                  <div class="row g-4">
                     <div class="col-6">
                        <div class="ratio ratio-3x4 rounded-4 overflow-hidden shadow-sm hover-lift">
                           <img src="https://images.unsplash.com/photo-1581539250439-c96689b516dd?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" class="object-fit-cover" alt="Sustainable material">
                        </div>
                     </div>
                     <div class="col-6">
                        <div class="ratio ratio-3x4 rounded-4 overflow-hidden shadow-sm hover-lift">
                           <img src="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" class="object-fit-cover" alt="Quality product">
                        </div>
                     </div>
                  </div>
               </div>

            </div>
         </div>
      </section>

      <section class="py-6 container px-lg-5">
        <div class="bg-black text-white rounded-5 p-5 p-lg-6 text-center position-relative overflow-hidden">
          <div class="position-relative z-2">
            <span class="text-uppercase tracking-wide text-white-50 extra-small fw-bold mb-3 d-block">Join the Community</span>
            <h2 class="display-5 fw-bold mb-3 tracking-tight">Stories, delivered.</h2>
            <p class="text-white-50 mb-5 mx-auto lead" style="max-width: 500px;">
               Get early access to new arrivals, exclusive offers, and design notes delivered to your inbox.
            </p>
            <form class="d-flex justify-content-center gap-2 flex-column flex-sm-row mx-auto" style="max-width: 450px;">
              <input type="email" class="form-control form-control-lg rounded-pill border-0 px-4" placeholder="Your email address">
              <button class="btn btn-white rounded-pill px-5 py-3 fw-bold text-uppercase tracking-wide hover-fill-dark">Subscribe</button>
            </form>
          </div>
        </div>
      </section>

    </main>

    <PremiumFooter @navigate="handleNavigation" />

  </div>
</template>

<script>
import PremiumNavbar from '@/components/Navbar.vue';
import PremiumFooter from '@/components/Footer.vue';

export default {
  name: "AboutView",
  components: {
    PremiumNavbar,
    PremiumFooter
  },
  data() {
    return {
      values: [
        {
          title: "Craftsmanship",
          desc: "We champion the makers. Every item is vetted for material quality, construction, and finish.",
          icon: "bi bi-hammer"
        },
        {
          title: "Curation",
          desc: "We filter the noise. We handpick only the best, so you can shop with confidence and ease.",
          icon: "bi bi-filter-circle"
        },
        {
          title: "Longevity",
          desc: "Our focus is on aesthetic durability—pieces that look good today and ten years from now.",
          icon: "bi bi-infinity"
        }
      ]
    };
  },
  methods: {
    handleNavigation(page) {
      console.log(`Navigating to: ${page}`);
    }
  }
};
</script>

<style scoped>
/* PREMIUM VISUAL GUIDELINES */

/* Spacing & Sizing */
.py-6 { padding-top: 6rem; padding-bottom: 6rem; }
.space-y-4 > * + * { margin-top: 1.5rem; }

/* Typography */
.tracking-wide { letter-spacing: 0.1em; }
.tracking-tight { letter-spacing: -0.03em; }
.extra-small { font-size: 0.75rem; }
.text-white-90 { color: rgba(255, 255, 255, 0.9); }

/* Overlap Logic Fixes */
@media (min-width: 992px) {
  /* This creates the overlap effect but keeps it within the container width */
  .ms-lg-n5 {
    margin-left: -6rem !important; 
  }
}
@media (max-width: 991px) {
  /* On mobile, pull it up slightly to connect the sections */
  .mt-n5 {
    margin-top: -3rem !important;
  }
}

/* Animations & Transitions */
.animate-fade-up {
  animation: fadeUp 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  opacity: 0;
  transform: translateY(30px);
}
@keyframes fadeUp {
  to { opacity: 1; transform: translateY(0); }
}

.hover-lift { transition: transform 0.3s ease, box-shadow 0.3s ease; }
.hover-lift:hover { 
  transform: translateY(-5px); 
  box-shadow: 0 15px 30px rgba(0,0,0,0.05) !important;
}

.transition-all { transition: all 0.3s ease; }
.group:hover .scale-110 { transform: scale(1.1); }

/* Buttons */
.btn-white {
    background: #fff; color: #000; border: none;
}
.hover-fill-dark:hover {
    background: #333; color: #fff;
}

/* Form inputs */
.form-control:focus {
  box-shadow: none;
  border-color: #000;
}
</style>