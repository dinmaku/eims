<template>
    <div class = "w-screen h-screen flex overflow-hidden font-inter">
      <!-- Side bar -->
      <div class="w-[250px] h-full bg-gray-200 text-center text-white top-0 left-0 overflow-y-auto">
       <div class ="h-[50px] bg-gray-200 flex justify-start items-center">
          <div class="flex text-center items-center px-[20px]">
        <h3 class="font-bold text-2xl text-gray-800">EIMS</h3>
      </div>

       </div>
       <div class="h-[calc(100vh-50px)] bg-[#B22222] py-[20px]">
        <div class="flex flex-col justify-between h-full px-[20px] space-y-[10px]">
          <div class="flex flex-col justify-between space-y-[10px]">
            <router-link to="/dashboard" class="inline-flex relative items-center py-[20px] px-[10px] w-full text-sm font-interBold font-semibold rounded-md border-gray-200 hover:bg-white hover:text-gray-900 transition duration-400 ease-in-out group whitespace-nowrap">
              <img aria-hidden="true" class="mr-2 w-[20px] h-[20px] text-white transition duration-300 ease-in-out group-hover:brightness-0" src="/img/stats.png">
              Dashboard
            </router-link>

            <p @click="toggleSection('setup')" class="ml-2 mb-5 text-lg text-left font-bold text-[#FFE4C4] cursor-pointer">Setup</p>
            <div v-if="visibleSections.setup" class="ml-4 border-l-2 border-gray-50">
              <router-link 
                v-if="userType !== 'staff'" 
                to="/manage-users" 
                class="inline-flex items-center py-[15px] px-[10px] w-full text-sm font-interBold font-semibold hover:bg-white hover:text-gray-900 transition duration-400 ease-in-out group whitespace-nowrap">
                <img aria-hidden="true" class="mr-2 w-[20px] h-[20px] text-white transition duration-300 ease-in-out group-hover:brightness-0" src="/img/manage-user.png">
                Accounts
              </router-link>
              <router-link to="/add-venue" class="inline-flex items-center py-[15px] px-[10px] w-full text-sm font-interBold font-semibold hover:bg-white hover:text-gray-900 transition duration-400 ease-in-out group whitespace-nowrap">
                <img aria-hidden="true" class="mr-2 w-[20px] h-[20px] text-white transition duration-300 ease-in-out group-hover:brightness-0" src="/img/venue.png">
                Venues
              </router-link>
              <router-link to="/additional-services" class="inline-flex items-center py-[15px] px-[10px] w-full text-sm font-interBold font-semibold hover:bg-white hover:text-gray-900 transition duration-400 ease-in-out group whitespace-nowrap">
                <img aria-hidden="true" class="mr-2 w-[20px] h-[20px] text-white transition duration-300 ease-in-out group-hover:brightness-0" src="/img/birthday-cake.png">
                Inclusions
              </router-link>
              <router-link to="/add-discounts" class="inline-flex items-center py-[15px] px-[6.3px] w-full text-sm font-interBold font-semibold hover:bg-white hover:text-gray-900 transition duration-400 ease-in-out group whitespace-nowrap">
                <img aria-hidden="true" class="mr-2 w-[20px] h-[20px] text-white transition duration-300 ease-in-out group-hover:brightness-0" src="/img/discounts.png">
                Discounts
              </router-link>
              <router-link to="/add-outfitPackage" class="inline-flex items-center py-[15px] px-[6.3px] w-full text-sm font-interBold font-semibold hover:bg-white hover:text-gray-900 transition duration-400 ease-in-out group whitespace-nowrap">
                <img aria-hidden="true" class="mr-2 w-[20px] h-[20px] text-white transition duration-300 ease-in-out group-hover:brightness-0" src="/img/add-wardrobe.png">
                Outfit Packages
              </router-link>
              <router-link to="/add-services" class="inline-flex items-center py-[15px] px-[6.3px] w-full text-sm font-interBold font-semibold hover:bg-white hover:text-gray-900 transition duration-400 ease-in-out group whitespace-nowrap">
                <img aria-hidden="true" class="mr-2 w-[20px] h-[20px] text-white transition duration-300 ease-in-out group-hover:brightness-0" src="/img/events-ticket.png">
                Event Packages
              </router-link>
              
            </div>

            <p @click="toggleSection('management')" class="ml-2 text-left text-lg font-bold text-[#FFE4C4] cursor-pointer">Management</p>
            <div v-if="visibleSections.management" class="ml-4 border-l-2 border-gray-50">
              <router-link to="/manage-events" 
                @click="markAllWishlistsViewed"
                class="inline-flex items-center py-[15px] px-[10px] w-full text-sm font-interBold font-semibold hover:bg-white hover:text-gray-900 transition duration-400 ease-in-out group whitespace-nowrap relative">
                <img aria-hidden="true" class="mr-2 w-[20px] h-[20px] text-white transition duration-300 ease-in-out group-hover:brightness-0" src="/img/events-booked.png">
                Events
                <span v-if="newWishlistCount > 0" 
                      class="absolute right-2 top-1/2 -translate-y-1/2 bg-red-500 text-white text-xs rounded-full px-2 py-0.5 min-w-[20px] text-center">
                  {{ newWishlistCount }}
                </span>
              </router-link>
            </div>
          </div>

          <div class="h-[50px]">
            <div class="relative">
              <div @click="toggleDrop" ref="settingsButton" class="flex items-center py-[10px] px-[10px] w-full text-md font-interBold font-semibold rounded-md border-gray-200 hover:bg-white hover:text-gray-900 transition duration-400 ease-in-out group cursor-pointer whitespace-nowrap select-none">
                <img aria-hidden="true" class="mr-2 w-[20px] h-[20px] text-white transition duration-300 ease-in-out group-hover:brightness-0" src="/img/settings2.png">
               <p class ="text-center items-center">Action</p>
              </div>
              <!-- Drop down -->
              <div v-show="showDropDown" ref="dropdownMenu" @click.self="showDropDown = false" class="fixed z-60 w-44 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none" role="menu" aria-orientation="vertical" aria-labelledby="menu-button" tabindex="-1">
                <div class="py-1 text-left" role="none">
                  <!-- Active: "bg-gray-100 text-gray-900", Not Active: "text-gray-700" -->
                  <a href="/profile" class="text-gray-700 block px-4 py-2 text-sm hover:bg-gray-200" role="menuitem" tabindex="-1" id="menu-item-0">Profile</a>
                  <a href="#" class="text-gray-700 block px-4 py-2 text-sm hover:bg-gray-200" role="menuitem" tabindex="-1" id="menu-item-1">Support</a>
                  <a href="#" class="text-gray-700 block px-4 py-2 text-sm hover:bg-gray-200" role="menuitem" tabindex="-1" id="menu-item-2">License</a>
                  <button type="submit" @click="handleLogout" class="text-gray-700 block w-full px-4 py-2 text-left text-sm hover:bg-gray-200" role="menuitem" tabindex="-1" id="menu-item-3">Log out</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      </div>
       <!--Head Bar-->

      <div class ="w-full h-full bg-gray-500 text-center">
        <div class ="h-[50px] bg-gray-100 flex items-center shadow-xl px-[20px] w-full py-[10px] z-10 border-b">
        <!--Hamburger Menu-->
        <div class="w-[calc(100%-200px)] flex justify-center ">
          </div>
  
       </div>


       <div class="min-h-[calc(100vh-50px)] h-full bg-white overflow-y-auto">
        <router-view />
      </div>

      </div>
        
      
    </div>
  </template>
  
  <script>
  import axios from 'axios';


  axios.defaults.withCredentials = true;

  export default {
    name: 'AdminDashboard',
  data() {
    return {
      userType: null,
      showDropDown: false,
      showSide: true,
      visibleSections: {
        setup: true,
        management: true,
        reports: false
      },
      newWishlistCount: 0,
      wishlistCheckInterval: null,
    }
  },
  async created() {
    try {
      // Get user profile from localStorage
      const userProfile = JSON.parse(localStorage.getItem('userProfile'));
      if (userProfile && userProfile.user_type) {
        // Convert to lowercase and trim any whitespace
        this.userType = userProfile.user_type.toLowerCase().trim();
        console.log('User type:', this.userType); // Add this for debugging
      }
      
      // Initial fetch of wishlist count
      await this.fetchNewWishlistCount();
      
      // Set up interval to check for new wishlists every minute
      this.wishlistCheckInterval = setInterval(this.fetchNewWishlistCount, 60000);
    } catch (error) {
      console.error('Error loading user profile:', error);
    }
  },
  mounted() {
    document.addEventListener('click', this.handleClickOutside)
  },
  beforeDestroy() {
    // Clear the interval when component is destroyed
    if (this.wishlistCheckInterval) {
      clearInterval(this.wishlistCheckInterval);
    }
    document.removeEventListener('click', this.handleClickOutside)
  },
  methods: {
    // hide show side bar
    toggleSideBar() {
      this.showSide = !this.showSide

    },
    toggleSection(section) {
      this.visibleSections[section] = !this.visibleSections[section];
    },
    // toggle user 
    toggleDrop() {
      this.showDropDown = !this.showDropDown
      if (this.showDropDown) {
        this.positionDropdown()
      }
    },
    positionDropdown() {
      const settingsButton = this.$refs.settingsButton
      const dropdownMenu = this.$refs.dropdownMenu
      const rect = settingsButton.getBoundingClientRect()
      
      // Position at top center of the settings button
      const buttonCenterX = rect.left + (rect.width / 85)
      const dropdownWidth = dropdownMenu.offsetWidth
      
      dropdownMenu.style.top = `${rect.top - 155}px`
      dropdownMenu.style.left = `${buttonCenterX - (dropdownWidth / 2)}px`
    },
    handleLogout() {
      this.loggedIn = false; // Update Vue component state
      localStorage.removeItem('loggedIn'); // Remove login status from localStorage
      localStorage.removeItem('access_token');
      localStorage.removeItem('userid');
      this.showDropDown = false; // Close dropdown
      this.$router.push('/'); // Optionally redirect to home or login page
      },
    handleClickOutside(event) {
      if (this.showDropDown && this.$refs.settingsButton && this.$refs.dropdownMenu) {
        if (!this.$refs.settingsButton.contains(event.target) && !this.$refs.dropdownMenu.contains(event.target)) {
          this.showDropDown = false
        }
      }
    },

    async fetchNewWishlistCount() {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          console.log('No access token found');
          return;
        }

        const response = await axios.get('http://127.0.0.1:5000/api/events/wishlist/count', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          withCredentials: true
        });

        if (response.data && typeof response.data.count === 'number') {
          this.newWishlistCount = response.data.count;
        } else {
          console.warn('Invalid response format:', response.data);
        }
      } catch (error) {
        console.error('Error fetching wishlist count:', error);
        if (error.response) {
          console.error('Error response:', error.response.data);
        }
      }
    },

    async markAllWishlistsViewed() {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          console.log('No access token found');
          return;
        }

        const response = await axios.post('http://127.0.0.1:5000/api/events/wishlist/mark-all-viewed', {}, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          withCredentials: true
        });

        if (response.data.success) {
          this.newWishlistCount = 0;  // Reset the count immediately
        }
      } catch (error) {
        console.error('Error marking wishlists as viewed:', error);
      }
    },
  }

};
  </script>
  
  <style scoped>
  html {
    scroll-behavior: smooth;
  }
    
  </style>