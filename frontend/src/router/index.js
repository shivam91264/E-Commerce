import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Home.vue'
import ShopView from '../views/ShopView.vue'
import ProductDetails from '../views/ProductDetails.vue'
import CartView from '../views/CartView.vue'
import CheckoutView from '../views/CheckoutView.vue'
import OrderSuccessView from '../views/OrderSuccessView.vue'
import NewArrivalsView from '../views/NewArrivalsView.vue'
import AboutView from '../views/AboutView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ProfileView from '../views/ProfileView.vue'
import OrdersView from '../views/OrdersView.vue'
import WishlistView from '../views/WishlistView.vue'
import AddressesView from '../views/AddressesView.vue'
import ContactView from '../views/ContactView.vue'
import AdminDashboard from '../views/admin/AdminDashboard.vue'
import AdminProducts from '../views/admin/AdminProducts.vue'
import AdminOrders from '../views/admin/AdminOrders.vue'
import AdminUsers from '../views/admin/AdminUsers.vue'
import AdminMessages from '../views/admin/AdminMessages.vue'
import AdminAnalytics from '../views/admin/AdminAnalytics.vue'
import SearchResultsView from '../views/SearchResultsView.vue'
import CategoryView from '../views/CategoryView.vue'
import ProductComparisonView from '../views/ProductComparisonView.vue'
import TermsView from '../views/TermsView.vue'
import PrivacyView from '../views/PrivacyView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/shop',
      name: 'shop',
      component: ShopView,
    },
    {
      path: '/product',
      name: 'product',
      component: ProductDetails,
    },
    {
      path: '/cart',
      name: 'cart',
      component: CartView,
    },
    {
      path: '/checkout',
      name: 'checkout',
      component: CheckoutView,
    },
    {
      path: '/ordersuccess',
      name: 'ordersuccess',
      component: OrderSuccessView,
    },
    {
      path: '/newarrivals',
      name: 'newarrivals',
      component: NewArrivalsView,
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
    },
    {
      path: '/order',
      name: 'order',
      component: OrdersView,
    },
    {
      path: '/wishlist',
      name: 'wishlist',
      component: WishlistView,
    },
    {
      path: '/addresses',
      name: 'addresses',
      component: AddressesView,
    },
    {
      path: '/contact',
      name: 'contact',
      component: ContactView,
    },
    {
      path: '/admin/dashboard',
      name: 'admindashboard',
      component: AdminDashboard,
    },
    {
      path: '/admin/products',
      name: 'adminproducts',
      component: AdminProducts,
    },
    {
      path: '/admin/orders',
      name: 'adminorders',
      component: AdminOrders,
    },
    {
      path: '/admin/users',
      name: 'adminusers',
      component: AdminUsers,
    },
    {
      path: '/admin/messages',
      name: 'adminmessages',
      component: AdminMessages,
    },
    {
      path: '/admin/analytics',
      name: 'adminanalytics',
      component: AdminAnalytics,
    },
    {
      path: '/searchresults',
      name: 'searchresults',
      component: SearchResultsView,
    },
    {
      path: '/categoryview',
      name: 'categoryview',
      component: CategoryView,
    },
    {
      path: '/productcomparisonview',
      name: 'productcomparisonview',
      component: ProductComparisonView,
    },
    {
      path: '/termsview',
      name: 'termsview',
      component: TermsView,
    },
    {
      path: '/privacyview',
      name: 'privacyview',
      component: PrivacyView,
    },
    
  ],
})

export default router
