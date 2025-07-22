<template>
  <div class="min-h-screen bg-gray-100 py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto mt-20">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">Package Deals</h1>
      
      <!-- Filter and Sort Section -->
      <div class="flex flex-wrap gap-4 mb-6">
        <!-- Filter by Package Type -->
        <div class="filter-container relative">
          <button 
            @click.stop="togglePackageTypeFilter" 
            class="flex items-center hover:bg-gray-400 p-2 rounded-lg bg-gray-600 text-white"
          >
            <i class="fas fa-box h-5 w-5"></i>
            <span class="ml-2 text-md font-medium">Package Type</span>
          </button>
          
          <div 
            v-if="showPackageTypeFilter" 
            @click.stop
            class="absolute top-12 left-0 bg-white shadow-lg rounded-lg p-4 z-[1] min-w-[200px]"
          >
            <div class="space-y-2">
              <button 
                @click="filterByPackageType('event')"
                :class="['w-full text-left px-4 py-2 rounded-lg', 
                  selectedPackageType === 'event' ? 'bg-indigo-100 text-indigo-700' : 'hover:bg-gray-100']"
              >
                Event Packages
              </button>
              <button 
                @click="filterByPackageType('gown')"
                :class="['w-full text-left px-4 py-2 rounded-lg', 
                  selectedPackageType === 'gown' ? 'bg-indigo-100 text-indigo-700' : 'hover:bg-gray-100']"
              >
                Attire Packages
              </button>
            </div>
          </div>
        </div>

        <!-- Filter by Event Type -->
        <div v-if="selectedPackageType !== 'gown'" class="filter-container relative">
          <button 
            @click.stop="toggleEventTypeFilter" 
            class="flex items-center hover:bg-gray-400 p-2 rounded-lg bg-gray-600 text-white"
          >
            <i class="fas fa-filter h-5 w-5"></i>
            <span class="ml-2 text-md font-medium">Event Type</span>
          </button>
          
          <div 
            v-if="showEventTypeFilter" 
            @click.stop
            class="absolute top-12 left-0 bg-white shadow-lg rounded-lg p-4 z-[1] min-w-[200px]"
          >
            <div class="space-y-2">
              <button 
                @click="filterByEventType('all')"
                :class="['w-full text-left px-4 py-2 rounded-lg', 
                  selectedEventType === 'all' ? 'bg-indigo-100 text-indigo-700' : 'hover:bg-gray-100']"
              >
                All Types
              </button>
              <button 
                v-for="type in uniqueEventTypes" 
                :key="type"
                @click="filterByEventType(type)"
                :class="['w-full text-left px-4 py-2 rounded-lg', 
                  selectedEventType === type ? 'bg-indigo-100 text-indigo-700' : 'hover:bg-gray-100']"
              >
                {{ type }}
              </button>
            </div>
          </div>
        </div>

        <!-- Sort Options -->
        <div class="flex items-center space-x-4">
          <select 
            v-model="sortBy" 
            class="bg-gray-600 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="price-asc">Price: Low to High</option>
            <option value="price-desc">Price: High to Low</option>
            <option value="capacity-asc">Capacity: Low to High</option>
            <option value="capacity-desc">Capacity: High to Low</option>
          </select>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
        {{ error }}
      </div>

      <!-- Loading Message -->
      <div v-if="(!packages.length && !gownPackages.length) && !error" class="text-center text-gray-600 py-8">
        Loading packages...
      </div>

      <!-- No Packages Message -->
      <div v-if="filteredPackages.length === 0 && !error" class="text-center text-gray-600 py-8">
        No packages available at the moment.
      </div>

      <!-- Package Cards -->
      <div v-if="filteredPackages.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Package Card -->
        <div class="package-card" v-for="pkg in filteredPackages" :key="pkg.id">
          <!-- Event Package Image -->
          <div class="package-image" v-if="pkg.type === 'event'">
            <img 
              :src="getVenueImageUrl(pkg.venue?.image)" 
              :alt="pkg.venue?.name || 'Venue Image'" 
              class="venue-image"
              @error="handleImageError"
            >
          </div>
          <!-- Outfit Package Image Grid -->
          <div v-else class="outfit-package-preview" :style="getRandomBackground(pkg.gown_package_id)">
            <div class="outfit-package-header">
              
              <span class="outfit-count text-white opacity-75" v-if="packageOutfits.length">{{ packageOutfits.length }} Outfits Included</span>
            </div>
          </div>
          <div class="package-content">
            <h3>{{ pkg.type === 'event' ? pkg.package_name : pkg.gown_package_name }}</h3>
            <p class="description">{{ pkg.description }}</p>
            <div class="package-details">
              <template v-if="pkg.type === 'event'">
                <div class="detail-item">
                  <i class="fas fa-users"></i>
                  <span>Capacity: {{ pkg.capacity }} guests</span>
                </div>
                <div class="detail-item">
                  <i class="fas fa-map-marker-alt"></i>
                  <span>{{ pkg.venue?.name || 'Venue not specified' }}</span>
                </div>
                <div class="detail-item">
                  <i class="fas fa-calendar-alt"></i>
                  <span>{{ pkg.event_type || 'Event type not specified' }}</span>
                </div>
              </template>
              <template v-else>
                <div class="detail-item">
                  <i class="fas fa-tshirt"></i>
                  <span>{{ pkg.gown_package_name }}</span>
                </div>
                <div class="detail-item">
                  <i class="fas fa-box"></i>
                  <span>Gown Package</span>
                </div>
              </template>
              <div class="detail-item">
                <i class="fas fa-tag"></i>
                <span>₱{{ (pkg.type === 'event' ? pkg.total_price : pkg.gown_package_price).toLocaleString() }}</span>
              </div>
            </div>
            <div class="package-actions">
              <button class="view-details-btn" @click="viewPackageDetails(pkg)">
                View Details
              </button>
  
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Package Details Modal -->
    <div v-if="showModal" @click.self="closeModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <!-- Modal Header -->
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-2xl font-bold">{{ selectedPackage?.type === 'event' ? selectedPackage.package_name : selectedPackage?.gown_package_name }}</h2>
            <button @click="closeModal" class="text-gray-500 hover:text-gray-700">
              <i class="fas fa-times text-xl"></i>
            </button>
          </div>

          <!-- Modal Content -->
          <div v-if="selectedPackage">
            <!-- Package Description -->
            <p class="text-gray-600 mb-4">{{ selectedPackage.description }}</p>

            <!-- Package Price -->
            <div class="bg-gray-100 p-4 rounded-lg mb-4">
              <h3 class="text-lg font-semibold mb-2">Package Price</h3>
              <p class="text-2xl font-bold text-indigo-600">
                ₱{{ (selectedPackage.type === 'event' ? selectedPackage.total_price : selectedPackage.gown_package_price).toLocaleString() }}
              </p>
            </div>

            <!-- Event Package Details -->
            <template v-if="selectedPackage.type === 'event'">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div class="bg-gray-100 p-4 rounded-lg">
                  <h3 class="text-lg font-semibold mb-2">Venue</h3>
                  <p>{{ selectedPackage.venue?.name || 'Not specified' }}</p>
                </div>
                <div class="bg-gray-100 p-4 rounded-lg">
                  <h3 class="text-lg font-semibold mb-2">Capacity</h3>
                  <p>{{ selectedPackage.capacity }} guests</p>
                </div>
              </div>
            </template>

            <!-- Gown Package Details -->
            <template v-else>
              <!-- Package Outfits -->
              <div v-if="packageOutfits.length > 0" class="mt-6">
                <h3 class="text-lg font-semibold mb-4">Included Outfits</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div v-for="outfit in packageOutfits" :key="outfit.outfit_id" class="bg-gray-100 p-4 rounded-lg">
                    <div class="flex items-start space-x-4">
                      <img 
                        v-if="outfit.outfit_img"
                        :src="getOutfitImageUrl(outfit.outfit_img)" 
                        :alt="outfit.outfit_name"
                        class="w-24 h-24 object-cover rounded-lg"
                        @error="handleImageError"
                      >
                      <div>
                        <h4 class="font-semibold">{{ outfit.outfit_name }}</h4>
                        <p class="text-sm text-gray-600">Type: {{ outfit.outfit_type }}</p>
                        <p class="text-sm text-gray-600">Color: {{ outfit.outfit_color }}</p>
                        <p class="text-sm text-gray-600">Size: {{ outfit.size }}</p>
                        <p class="text-sm text-gray-600">{{ outfit.outfit_desc }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </template>
          </div>

          <!-- Modal Footer -->
          <div class="mt-6 flex justify-end space-x-4">
            <button 
              @click="closeModal" 
              class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-100"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

// Configure axios defaults
axios.defaults.baseURL = 'http://localhost:5001';
axios.defaults.withCredentials = true;

export default {
  name: 'Package Deals',
  data() {
    return {
      packages: [],
      gownPackages: [],
      error: null,
      showEventTypeFilter: false,
      showPackageTypeFilter: false,
      selectedEventType: 'all',
      selectedPackageType: 'event',
      sortBy: 'price-asc',
      apiBaseUrl: import.meta.env.VITE_API_BASE_URL || window.location.origin,
      showModal: false,
      selectedPackage: null,
      packageOutfits: [],
      packageBackgrounds: {}, // Store background assignments
    };
  },
  computed: {
    uniqueEventTypes() {
      return [...new Set(this.packages.map(pkg => pkg.event_type).filter(Boolean))].sort();
    },
    filteredPackages() {
      let filtered = [];
      
      // Add event packages if selected
      if (this.selectedPackageType === 'event') {
        let eventPackages = [...this.packages].map(pkg => ({ ...pkg, type: 'event' }));
        if (this.selectedEventType !== 'all') {
          eventPackages = eventPackages.filter(pkg => pkg.event_type === this.selectedEventType);
        }
        filtered = [...filtered, ...eventPackages];
      }
      
      // Add gown packages if selected
      if (this.selectedPackageType === 'gown') {
        let gownPackages = [...this.gownPackages].map(pkg => ({ ...pkg, type: 'gown' }));
        filtered = [...filtered, ...gownPackages];
      }
      
      // Sort packages
      filtered.sort((a, b) => {
        const priceA = a.type === 'event' ? a.total_price : a.gown_package_price;
        const priceB = b.type === 'event' ? b.total_price : b.gown_package_price;
        const capacityA = a.type === 'event' ? a.capacity : 0;
        const capacityB = b.type === 'event' ? b.capacity : 0;
        
        switch (this.sortBy) {
          case 'price-asc':
            return priceA - priceB;
          case 'price-desc':
            return priceB - priceA;
          case 'capacity-asc':
            return capacityA - capacityB;
          case 'capacity-desc':
            return capacityB - capacityA;
          default:
            return 0;
        }
      });
      
      return filtered;
    }
  },
  methods: {
    togglePackageTypeFilter() {
      this.showPackageTypeFilter = !this.showPackageTypeFilter;
      this.showEventTypeFilter = false;
    },
    toggleEventTypeFilter() {
      this.showEventTypeFilter = !this.showEventTypeFilter;
      this.showPackageTypeFilter = false;
    },
    filterByPackageType(type) {
      this.selectedPackageType = type;
      this.showPackageTypeFilter = false;
    },
    filterByEventType(type) {
      this.selectedEventType = type;
      this.showEventTypeFilter = false;
    },
    handleImageError(e) {
      console.error('Image failed to load:', e.target.src);
      e.target.src = `${axios.defaults.baseURL}/saved/venue_img/grandballroom.png`;
    },
    getGownPackageImage() {
      return `${axios.defaults.baseURL}/saved/venue_img/gown_package.png`;
    },
    async viewPackageDetails(pkg) {
      this.selectedPackage = pkg;
      
      // If it's a gown package, fetch the included outfits
      if (pkg.type === 'gown') {
        try {
          const token = localStorage.getItem('access_token');
          // Get the outfits from the gown package using the outfits table
          const response = await axios.get(`/api/gown-package/${pkg.gown_package_id}/outfits`, {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          });
          
          if (response.data && response.data.status === 'success') {
            this.packageOutfits = response.data.data;
          } else {
            console.error('Error fetching gown package outfits:', response.data?.message);
            this.packageOutfits = [];
          }
        } catch (error) {
          console.error('Error fetching gown package outfits:', error);
          this.packageOutfits = [];
        }
      }
      
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.selectedPackage = null;
      this.packageOutfits = [];
    },
    getOutfitImageUrl(image) {
      if (!image) {
        return `${axios.defaults.baseURL}/api/outfits/image/default_outfit.png`;
      }
      image = image.replace(/^[A-Za-z]:\\/, '');
      image = image.split(/[\/\\]/).pop();
      return `${axios.defaults.baseURL}/api/outfits/image/${image}`;
    },
    async fetchPackages() {
      try {
        const response = await axios.get('/api/packages');
        console.log('API Response:', response.data);
        
        if (response.data && response.data.status === 'success') {
          this.packages = response.data.data;
          console.log('Packages loaded:', this.packages);
          this.error = null;
        } else {
          this.error = response.data?.message || 'Failed to fetch packages';
          console.error('Error:', this.error);
        }
      } catch (error) {
        this.error = error.response?.data?.message || error.message;
        console.error('Error fetching packages:', error);
      }
    },
   async fetchGownPackages() {
        try {
          const response = await axios.get('/available-gown-packages', {
            headers: {
              'Content-Type': 'application/json'
            }
          });

          console.log('Gown Packages Response:', response.data);

          if (response.data) {
            this.gownPackages = response.data;
            console.log('Gown Packages loaded:', this.gownPackages);
            this.error = null;
          } else {
            this.error = 'Failed to fetch gown packages';
            console.error('Error:', this.error);
          }
        } catch (error) {
          this.error = error.response?.data?.message || error.message;
          console.error('Error fetching gown packages:', error);
        }
      },
    getVenueImageUrl(image) {
      if (!image) {
        return `${axios.defaults.baseURL}/saved/venue_img/grandballroom.png`;
      }

      // Clean up the image path
      image = image.replace(/^[A-Za-z]:\\/, '');
      image = image.split(/[\/\\]/).pop();

      return `${axios.defaults.baseURL}/saved/venue_img/${image}`;
    },
    addToWishlist(pkg) {
      // TODO: Implement add to wishlist functionality
      console.log('Add to wishlist:', pkg);
    },
    getRandomBackground(packageId) {
      // If this package already has an assigned background, return it
      if (this.packageBackgrounds[packageId]) {
        return {
          backgroundImage: `url(${axios.defaults.baseURL}/api/outfits-packages-bg/${this.packageBackgrounds[packageId]})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        };
      }

      // Generate random number between 1 and 10
      const randomNum = Math.floor(Math.random() * 10) + 1;
      const bgImage = `bg${randomNum}.png`;
      
      // Store the assignment for this package
      this.packageBackgrounds[packageId] = bgImage;

      return {
        backgroundImage: `url(${axios.defaults.baseURL}/api/outfits-packages-bg/${bgImage})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center'
      };
    },
  },
  async created() {
    await Promise.all([
      this.fetchPackages(),
      this.fetchGownPackages()
    ]);
  },
  mounted() {
    // Close filter dropdowns when clicking outside
    document.addEventListener('click', () => {
      this.showEventTypeFilter = false;
      this.showPackageTypeFilter = false;
    });
  },
  beforeUnmount() {
    // Clean up event listener
    document.removeEventListener('click', () => {
      this.showEventTypeFilter = false;
      this.showPackageTypeFilter = false;
    });
  }
};
</script>

<style scoped>
.filter-container {
  position: relative;
  display: inline-block;
  z-index: 1;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

.package-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.package-card:hover {
  transform: translateY(-5px);
}

.package-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.venue-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.package-card:hover .venue-image {
  transform: scale(1.05);
}

.package-content {
  padding: 1.5rem;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.package-content h3 {
  margin: 0 0 1rem 0;
  color: #333;
  font-size: 1.5rem;
  font-weight: 600;
}

.description {
  color: #666;
  margin-bottom: 1rem;
  flex-grow: 1;
}

.package-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #555;
}

.detail-item i {
  color: #4a90e2;
  width: 20px;
}

.package-actions {
  display: flex;
  gap: 1rem;
  margin-top: auto;
}

.view-details-btn {
  flex-grow: 1;
  padding: 0.75rem 1.5rem;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.view-details-btn:hover {
  background-color: #357abd;
}

.add-to-wishlist-btn {
  padding: 0.75rem;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-to-wishlist-btn:hover {
  background-color: #e9ecef;
  border-color: #ced4da;
}

.add-to-wishlist-btn i {
  color: #dc3545;
}

@media (max-width: 768px) {
  .package-details {
    grid-template-columns: 1fr;
  }
}

.outfit-package-preview {
  width: 100%;
  height: 200px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.outfit-package-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.25rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
</style>