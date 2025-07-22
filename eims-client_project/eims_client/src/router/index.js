import { createRouter, createWebHistory } from 'vue-router';
import ClientNavigation from '../components/navigation.vue';
import Home from '../pages/home.vue'
import Wishlist from  '../pages/add-wishlist.vue';
import LoginRegister from '../pages/login-register.vue';
import PackageDeal from '../pages/package-deal.vue';
import AttireCatalog from '../pages/attire-catalog.vue';
import BookedServices from '../pages/booked_services.vue';
import VendorSchedule from '../pages/vendor-schedule.vue';
import SuppliersProfile from '../pages/suppliers_profile.vue';
import UserProfile from '../pages/user_profile.vue';


const routes = [
  {
    path: '/',
    component: ClientNavigation, 
    children: [
      {
        path: '',
        component: Home, 
        meta: {
          title: 'Welcome to RedCarpet',
        },
      },
      {
        path: 'add-wishlist',
        name: 'Wishlist',
        component: Wishlist,
        meta: {
          title: 'Wishlist',
          requiresAuth: true,
        },
      },
      {
        path: 'login-register',
        name: 'LoginRegister',
        component: LoginRegister,
        meta: {
          title: 'Login',
        },
      },
      {
        path: 'package-deal',
        name: 'Package Deal',
        component: PackageDeal,
        meta: {
          title: 'Packages',
        },
      },
      {
        path: 'attire-catalog',
        name: 'Attire Catalog',
        component: AttireCatalog,
        meta: {
          title: 'Packages',
        },
      },

      {
        path: 'booked-services',
        name: 'Booked Services',
        component: BookedServices,
        meta: {
          title: 'My Bookings',
          requiresAuth: true,
        },
      },
      {
        path: 'vendor-schedule',
        name: 'Vendor Schedule',
        component: VendorSchedule,
        meta: {
          title: 'My Schedule',
          requiresAuth: true,
        },
      },
      {
        path: 'suppliers-profile',
        name: 'Suppliers Profile',
        component: SuppliersProfile,
        meta: {
          title: 'Suppliers Profile',
        },
      },
      {
        path: 'user-profile',
        name: 'User Profile',
        component: UserProfile,
        meta: {
          title: 'User Profile',
          requiresAuth: true,
        },
      },
      
    ],
  },
];
  



const router = Router();
export default router;
function Router() {
  const router = createRouter({
    history: createWebHistory(),
    routes,
  });
  return router;
}

router.beforeEach((to, from, next) => {
  // Set the document title
  document.title = to.meta.title || 'RedCarpet';

  // Check authentication
  const isLoggedIn = !!localStorage.getItem('access_token'); // or check Vuex store
  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/'); // Redirect to login if not logged in
  } else {
    next(); // Continue as normal
  }
});