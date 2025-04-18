<template>
  <div class="min-h-screen bg-gray-100 py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto mt-20">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">Package Deals</h1>
      
      <!-- Filter and Sort Section -->
      <div class="flex flex-wrap gap-4 mb-6">
        <!-- Filter by Event Type -->
        <div class="filter-container relative">
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
      <div v-if="!packages.length && !error" class="text-center text-gray-600 py-8">
        Loading packages...
      </div>

      <!-- No Packages Message -->
      <div v-if="filteredPackages.length === 0 && !error" class="text-center text-gray-600 py-8">
        No packages available at the moment.
      </div>

      <!-- Package Cards -->
      <div v-if="filteredPackages.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div class="package-card" v-for="pkg in filteredPackages" :key="pkg.package_id">
          <div class="package-image">
            <img 
              :src="getVenueImageUrl(pkg.venue?.image)" 
              :alt="pkg.venue?.name || 'Venue Image'" 
              class="venue-image"
              @error="handleImageError"
            >
          </div>
          <div class="package-content">
            <h3>{{ pkg.package_name }}</h3>
            <p class="description">{{ pkg.description }}</p>
            <div class="package-details">
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
              <div class="detail-item">
                <i class="fas fa-tag"></i>
                <span>₱{{ pkg.total_price.toLocaleString() }}</span>
              </div>
            </div>
            <div class="package-actions">
              <button class="view-details-btn" @click="viewPackageDetails(pkg.package_id)">
                View Details
              </button>
              <button class="add-to-wishlist-btn" @click="addToWishlist(pkg.package_id)">
                <i class="fas fa-heart"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

// Configure axios defaults
axios.defaults.baseURL = 'http://localhost:5000';
axios.defaults.withCredentials = true;

export default {
  name: 'Package Deals',
  data() {
    return {
      packages: [],
      error: null,
      showEventTypeFilter: false,
      selectedEventType: 'all',
      sortBy: 'price-asc',
      apiBaseUrl: import.meta.env.VITE_API_BASE_URL || window.location.origin,
    };
  },
  computed: {
    uniqueEventTypes() {
      return [...new Set(this.packages.map(pkg => pkg.event_type).filter(Boolean))].sort();
    },
    filteredPackages() {
      let filtered = [...this.packages];
      
      // Filter by event type
      if (this.selectedEventType !== 'all') {
        filtered = filtered.filter(pkg => pkg.event_type === this.selectedEventType);
      }
      
      // Sort packages
      filtered.sort((a, b) => {
        switch (this.sortBy) {
          case 'price-asc':
            return a.total_price - b.total_price;
          case 'price-desc':
            return b.total_price - a.total_price;
          case 'capacity-asc':
            return a.capacity - b.capacity;
          case 'capacity-desc':
            return b.capacity - a.capacity;
          default:
            return 0;
        }
      });
      
      return filtered;
    }
  },
  methods: {
    toggleEventTypeFilter() {
      this.showEventTypeFilter = !this.showEventTypeFilter;
    },
    filterByEventType(type) {
      this.selectedEventType = type;
      this.showEventTypeFilter = false;
    },
    handleImageError(e) {
      console.error('Image failed to load:', e.target.src);
      // Fallback to a static image we know exists
      e.target.src = '/img/venues-img/grandballroom.png';
    },
    viewPackageDetails(pkg) {
      // TODO: Implement package details view
      console.log('View package details:', pkg);
    },
    async fetchPackages() {
      try {
        const response = await axios.get('/api/packages');
        console.log('API Response:', response.data); // Debug log
        
        if (response.data && response.data.status === 'success') {
          this.packages = response.data.data;
          console.log('Packages loaded:', this.packages); // Debug log
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
    getVenueImageUrl(image) {
      // Default image if none provided
      if (!image) {
        return '/img/venues-img/grandballroom.png';
      }
      
      // If it's already a path to a static image in venues-img, return as is
      if (image.startsWith('/img/venues-img/')) {
        return image;
      }
      
      // If it's already a path to an API endpoint image, prepend the API base URL
      if (image.startsWith('/api/venue-image/')) {
        const apiBaseUrl = 'http://localhost:5000';
        return `${apiBaseUrl}${image}`;
      }
      
      // If it's a full URL, use it directly
      if (image.startsWith('http')) {
        return image;
      }
      
      // For venue images with venue_TIMESTAMP_NAME format
      if (image.startsWith('venue_') && image.includes('_')) {
        // Extract the actual venue name after the timestamp
        const parts = image.split('_');
        if (parts.length >= 3) {
          // Get the venue name part (last part)
          const venueNameWithExt = parts.slice(2).join('_');
          
          // Check if we have a matching static image with this venue name
          const staticFiles = ['grandballroom.png', 'hogwarts.png', 'oceanview.png', 'paseo.png', 'sealavie.png'];
          
          for (const staticFile of staticFiles) {
            // Check if the venue name (without extension) is contained in the static filename
            const venueName = venueNameWithExt.split('.')[0].toLowerCase();
            if (staticFile.toLowerCase().includes(venueName)) {
              return `/img/venues-img/${staticFile}`;
            }
          }
          
          // If no match found but we have a copy of the original file in public folder
          try {
            // First try with the original filename
            return `/img/venues-img/${image}`;
          } catch (error) {
            // If that fails, use the API endpoint
            const apiBaseUrl = 'http://localhost:5000';
            return `${apiBaseUrl}/api/venue-image/${image}`;
          }
        }
      }
      
      // For all other cases, use the API endpoint
      const apiBaseUrl = 'http://localhost:5000';
      return `${apiBaseUrl}/api/venue-image/${image}`;
    },
    addToWishlist(packageId) {
      // TODO: Implement add to wishlist functionality
      console.log('Add to wishlist:', packageId);
    }
  },
  async created() {
    await this.fetchPackages();
  },
  mounted() {
    // Close filter dropdown when clicking outside
    document.addEventListener('click', () => {
      this.showEventTypeFilter = false;
    });
  },
  beforeUnmount() {
    // Clean up event listener
    document.removeEventListener('click', () => {
      this.showEventTypeFilter = false;
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
</style>