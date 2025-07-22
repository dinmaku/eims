import { createRouter, createWebHistory } from 'vue-router';
import AdminLogin from '@/components/admin-login.vue';
import AdminDashboard from '../pages/dashboard.vue';
import Home from '../pages/home.vue';
import Profile from '../pages/profile.vue';
import ManageEvents from '../pages/manage-events.vue';
import Settings from '../pages/settings.vue';
import ManageOutfits from '../pages/manage-outfits.vue';
import ManageUsers from '../pages/manage-users.vue';
import UploadGallery from '../pages/upload-gallery.vue';
import CreateEvent from '../pages/create-event.vue';
import WeddingForm from '../pages/wedding-form.vue';
import BirthdayForm from '../pages/birthday-form.vue';
import DebutForm from '../pages/debut-form.vue';
import EventCalendar from '../pages/event-calendar.vue';
import Invoice from '../pages/invoice.vue';
import AddServices from '../pages/add-services.vue'
import AddVenue from '../pages/add-venue.vue';
import AddOutfitPackage from '../pages/add-outfitPackage.vue';
import AdditionalServices from '../pages/additional_services.vue';
import AddWishlist from '../pages/add-wishlist.vue';
import AddDiscounts from '../pages/discounts.vue';

const routes = [
  {
    name: 'AdminLogin',
    path: '/',
    component: AdminLogin
  },
  {
    path: '/dashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true }, // Add auth requirement for dashboard and its children
    children: [
      {
        path: '',
        component: Home
      },
      {
        name: 'Profile',
        path: '/profile', 
        component: Profile,
        meta: { requiresAuth: true }
      },
      {
        name: 'ManageEvents',
        path: '/manage-events',
        component: ManageEvents,
        requiresAuth: true,
      },
      {
        name: 'EventCalendar',
        path: '/event-calendar',
        component: EventCalendar,
        requiresAuth: true,
      },
      {
        name: 'ManageOutfits',
        path: '/manage-outfits',
        component: ManageOutfits,
        requiresAuth: true,
      },
      {
        name: 'ManageUsers',
        path: '/manage-users', 
        component: ManageUsers,
        requiresAuth: true,
      },
      {
        name: 'UploadGallery',
        path: '/upload-gallery', 
        component: UploadGallery,
        requiresAuth: true,
      },
      {
        name: 'Settings',
        path: '/settings',
        component: Settings,
        requiresAuth: true,
      },
      {
        name: 'CreateEvent',
        path: 'create-event',
        component: CreateEvent,
        meta: { requiresAuth: true },
        props: true,
        children: [
           {
             path: 'wedding-form', // Changed to relative path
             component: WeddingForm,
             meta: { requiresAuth: true }
           },
           {
            path: 'birthday-form', // Changed to relative path
            component: BirthdayForm,
            meta: { requiresAuth: true }
          },
          {
            path: 'debut-form', // Changed to relative path
            component: DebutForm,
            meta: { requiresAuth: true }
          }
        ]
      },
      {
        name: 'Invoice',
        path: '/invoice/:eventId?',
        component: Invoice,
        props: true,
        requiresAuth: true,     
      
      },
      {
        name: 'AddServices',
        path: '/add-services',
        component: AddServices,
        props: true,   
        requiresAuth: true,  
      
      },
      {
        name: 'AddVenue',
        path: '/add-venue',
        component: AddVenue,
        props: true,     
        requiresAuth: true,
      
      },
      {
        name: 'AddOutfitPackage',
        path: '/add-outfitPackage',
        component: AddOutfitPackage,
        props: true,     
        requiresAuth: true,
      
      },
      {
        name: 'AdditionalServices',
        path: '/additional-services',
        component: AdditionalServices,
        props: true,     
        requiresAuth: true,
      },
      {
        name: 'AddWishlist',
        path: '/add-wishlist',
        component: AddWishlist,
        props: true,
        requiresAuth: true,     
      },
      {
        name: 'AddDiscounts',
        path: '/add-discounts',
        component: AddDiscounts,
        props: true,     
        requiresAuth: true,
      },
    ],
  }
  // You can add additional routes here if needed
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  // Set the document title
  document.title = to.meta.title || 'RedCarpet Admin';

  // Check authentication
  const isLoggedIn = !!localStorage.getItem('access_token'); // or check Vuex store
  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/'); // Redirect to login if not logged in
  } else {
    next(); // Continue as normal
  }
});

export default router;