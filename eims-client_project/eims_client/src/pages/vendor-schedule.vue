<template>
    <div class="h-full overflow-y-auto overflow-x-hidden">
      <!-- Header with responsive layout -->
      <div class="flex justify-between items-center w-full h-20 bg-gray-100 shadow-lg antialiased mt-28 px-4 sm:px-6 lg:px-8">
        <h1 class="flex font-medium font-amaticBold text-2xl ml-5 sm:text-xl">My Booked Schedule</h1>
        <button 
          @click="openAvailabilitySidebar" 
          class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg font-medium transition-colors duration-200 flex items-center"
        >
         
          Manage Availability
        </button>
      </div>
  
      <!-- Sidebar (will slide in/out based on isSidebarOpen) -->
      <aside class="fixed top-0 right-0 w-full md:w-[450px] h-full bg-[#f8f9ef] shadow-lg transition-transform z-50 custom-shadow" :class="isSidebarOpen ? 'translate-x-0' : 'translate-x-full'">
        <div class="p-4">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-xl font-semibold">{{ sidebarMode === 'event' ? 'Schedule Event' : 'Manage Availability' }}</h2>
            <button @click="toggleSidebar" class="px-3 h-8 text-md bg-gray-200 font-bold rounded-full transform-transition duration-300 transform hover:scale-110">X</button>
          </div>
          
  

  

         <!-- Availability Form -->
        <div v-if="sidebarMode === 'availability'">
          <p class="mb-6 text-base text-gray-500">Mark dates as unavailable to prevent bookings.</p>
          
          <!-- Current Availability List -->
          <div v-if="supplierAvailability.length > 0" class="mb-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-3">Current Unavailable Dates</h3>
            <div class="space-y-2 max-h-40 overflow-y-auto">
              <div 
                v-for="avail in supplierAvailability.filter(a => !a.is_available)" 
                :key="avail.availability_id"
                class="flex items-center justify-between p-3 bg-red-50 border border-red-200 rounded-lg"
              >
                <div class="flex-1">
                  <div class="font-medium text-red-800">{{ avail.date }}</div>
                  <div v-if="avail.reason" class="text-sm text-red-600">{{ avail.reason }}</div>
                </div>
                <button 
                  @click="removeAvailability(avail.date)"
                  class="ml-2 px-2 py-1 bg-red-500 text-white text-xs rounded hover:bg-red-600 transition-colors"
                >
                  Remove
                </button>
              </div>
            </div>
          </div>
            
            <form @submit.prevent="setAvailability">
              <div class="mt-8 ml-2">
                <div class="flex items-center">
                  <label for="availability-date" class="block text-md font-semibold text-gray-700 mr-3 font-raleway">Date: </label>
                  <input type="date" class="h-10 w-full sm:w-56 rounded-lg shadow-md text-sm" id="availabilityDate" v-model="availabilityDate" required />
                </div>
              </div>
              
              <div class="mt-8 ml-2">
                <div class="flex items-center">
                  <label for="availability-status" class="block text-md font-semibold text-gray-700 mr-3 font-raleway">Status: </label>
                  <select class="h-10 w-full sm:w-56 rounded-lg shadow-md text-sm" id="availabilityStatus" v-model="availabilityStatus" required>
                    <option value="false">Unavailable</option>
                    <option value="true">Available</option>
                  </select>
                </div>
              </div>
              
              <div class="mt-8 ml-2">
                <div class="flex items-center">
                  <label for="availability-reason" class="block text-md font-semibold text-gray-700 mr-3 font-raleway">Reason: </label>
                  <textarea class="h-16 w-full sm:w-56 rounded-lg shadow-md text-sm p-2" id="availabilityReason" v-model="availabilityReason" placeholder="Optional reason for unavailability"></textarea>
                </div>
              </div>

              <div class="mt-10">
                <button type="submit" class="h-10 bg-red-500 text-md font-bold px-2 rounded-lg shadow-lg w-full sm:w-auto text-white">
                  {{ availabilityStatus === 'true' ? 'Mark as Available' : 'Mark as Unavailable' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </aside>
  
      <!-- Modal for Event Details -->
      <div v-if="isModalOpen" class="fixed inset-0 flex items-center justify-center z-50" @click.self="closeModal">
        <div class="modal-overlay absolute inset-0 bg-black opacity-50" @click.self="closeModal"></div>
        <div class="modal-content bg-white rounded-xl overflow-hidden shadow-2xl z-50 w-full max-w-3xl">
          <!-- Modal Header with Gradient -->
          <div class="bg-gradient-to-r from-blue-500 to-purple-600 p-4 text-white">
            <div class="flex justify-between items-center">
              <h2 class="text-2xl font-bold">{{ selectedEvent?.extendedProps?.eventName }}</h2>
              <button @click="closeModal" class="text-white hover:text-gray-200 transition duration-150">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <p class="text-blue-100 mt-1">{{ selectedEvent?.extendedProps?.eventType || 'Event' }} • {{ new Date(selectedEvent?.start).toLocaleDateString() }}</p>
          </div>

          <div class="p-4">
            <!-- Event Information Cards -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <!-- Event Details Card -->
              <div class="bg-gray-50 rounded-lg p-4 shadow-sm border border-gray-100">
                <h3 class="text-lg font-semibold text-gray-800 mb-2 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  Event Information
                </h3>
                <div class="space-y-2 text-gray-700">
                  <div class="flex">
                    <span class="w-24 font-medium text-gray-600">Theme:</span>
                    <span>{{ selectedEvent?.extendedProps?.eventTheme || 'Not specified' }}</span>
                  </div>
                  <div class="flex">
                    <span class="w-24 font-medium text-gray-600">Package:</span>
                    <span>{{ selectedEvent?.extendedProps?.packageName || 'Custom Package' }}</span>
                  </div>
                  <div class="flex">
                    <span class="w-24 font-medium text-gray-600">Date:</span>
                    <span>{{ new Date(selectedEvent?.start).toLocaleDateString() }}</span>
                  </div>
                  <div class="flex">
                    <span class="w-24 font-medium text-gray-600">Time:</span>
                    <span>{{ new Date(selectedEvent?.start).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) }} - 
                    {{ new Date(selectedEvent?.end).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) }}</span>
                  </div>
                  <div class="flex">
                    <span class="w-24 font-medium text-gray-600">Capacity:</span>
                    <span>{{ selectedEvent?.extendedProps?.venueInfo?.capacity || 'Not specified' }} people</span>
                  </div>
                </div>
              </div>

              <!-- Client Information Card -->
              <div class="bg-gray-50 rounded-lg p-4 shadow-sm border border-gray-100">
                <h3 class="text-lg font-semibold text-gray-800 mb-2 flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  Client Information
                </h3>
                <div class="space-y-2 text-gray-700">
                  <div class="flex">
                    <span class="w-24 font-medium text-gray-600">Name:</span>
                    <span>{{ selectedEvent?.extendedProps?.clientInfo?.firstName }} {{ selectedEvent?.extendedProps?.clientInfo?.lastName }}</span>
                  </div>
                  <div class="flex">
                    <span class="w-24 font-medium text-gray-600">Contact:</span>
                    <span>{{ selectedEvent?.extendedProps?.clientInfo?.contact || 'Not provided' }}</span>
                  </div>
                  <div class="flex">
                    <span class="w-24 font-medium text-gray-600">Address:</span>
                    <span class="truncate">{{ selectedEvent?.extendedProps?.clientInfo?.address || 'Not provided' }}</span>
                  </div>
                  <div class="flex">
                    <span class="w-24 font-medium text-gray-600">Type:</span>
                    <span>{{ selectedEvent?.extendedProps?.bookingType || 'Online' }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Venue Card -->
            <div v-if="selectedEvent?.extendedProps?.venueInfo?.name" class="bg-gradient-to-r from-purple-50 to-indigo-50 rounded-lg p-4 shadow-sm border border-purple-100 mb-4">
              <h3 class="text-lg font-semibold text-gray-800 mb-2 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-purple-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                Venue Information
              </h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div class="flex">
                  <span class="w-24 font-medium text-gray-600">Name:</span>
                  <span class="text-purple-700">{{ selectedEvent?.extendedProps?.venueInfo?.name }}</span>
                </div>
                <div class="flex">
                  <span class="w-24 font-medium text-gray-600">Price:</span>
                  <span class="text-purple-700 font-semibold">₱{{ selectedEvent?.extendedProps?.venueInfo?.price?.toLocaleString() || 'Not specified' }}</span>
                </div>
                <div class="flex col-span-2">
                  <span class="w-24 font-medium text-gray-600">Location:</span>
                  <span>{{ selectedEvent?.extendedProps?.venueInfo?.location || 'Not specified' }}</span>
                </div>
              </div>
            </div>

            <!-- Your Service Card -->
            <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-4 shadow-sm border border-blue-100 mb-4">
              <h3 class="text-lg font-semibold text-gray-800 mb-2 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                Your Service Details
              </h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div class="flex">
                  <span class="w-24 font-medium text-gray-600">Service:</span>
                  <span class="text-blue-700">{{ selectedEvent?.extendedProps?.supplierInfo?.service }}</span>
                </div>
                <div class="flex">
                  <span class="w-24 font-medium text-gray-600">Your Fee:</span>
                  <span class="text-green-700 font-semibold">₱{{ selectedEvent?.extendedProps?.totalPrice?.toLocaleString() || '0' }}</span>
                </div>
              </div>
              <div v-if="selectedEvent?.extendedProps?.bookingRemarks" class="mt-3 pt-2 border-t border-blue-100">
                <p class="font-medium text-gray-600 mb-1">Special Remarks:</p>
                <p class="text-gray-700 bg-white p-2 rounded-md">{{ selectedEvent?.extendedProps?.bookingRemarks }}</p>
              </div>
            </div>

            <!-- Modal Footer -->
            <div class="flex justify-end space-x-4 mt-4">
              <button @click="closeModal" class="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition duration-150 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
  
      <!-- FullCalendar View -->
      <div class="flex justify-start ml-12 items-center h-screen mb-10 py-5">
        <div class="w-full max-w-4xl h-full">
          <FullCalendar ref="fullCalendar" :options="calendarOptions" class="w-full h-full font-merriweatherRegular" />
        </div>
      </div>

      <!-- Snackbar for notifications -->
      <div v-if="snackbar.show" 
           class="fixed top-4 right-4 z-50 max-w-sm w-full bg-white shadow-lg rounded-lg pointer-events-auto ring-1 ring-black ring-opacity-5 overflow-hidden"
           :class="snackbar.type === 'success' ? 'border-l-4 border-green-400' : 'border-l-4 border-red-400'">
        <div class="p-4">
          <div class="flex items-start">
            <div class="flex-shrink-0">
              <svg v-if="snackbar.type === 'success'" class="h-6 w-6 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <svg v-else class="h-6 w-6 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
            <div class="ml-3 w-0 flex-1 pt-0.5">
              <p class="text-sm font-medium text-gray-900">{{ snackbar.message }}</p>
            </div>
            <div class="ml-4 flex-shrink-0 flex">
              <button @click="hideSnackbar" class="bg-white rounded-md inline-flex text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                <span class="sr-only">Close</span>
                <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mt-4 mx-8">
        <span class="block sm:inline">{{ error }}</span>
      </div>
      <div v-if="isLoading" class="flex justify-center items-center mt-4">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>
    </div>
  </template>
  
  
  <script>
  import FullCalendar from '@fullcalendar/vue3'
  import dayGridPlugin from '@fullcalendar/daygrid'
  import interactionPlugin from '@fullcalendar/interaction'
  
  export default {
    components: {
      FullCalendar
    },
    data() {
    return {
        calendarApi: null,
      calendarOptions: {
        plugins: [dayGridPlugin, interactionPlugin],
        initialView: 'dayGridMonth',
        dateClick: this.handleDateClick,
        events: [],
        eventContent: this.renderEvent,
        eventClick: this.handleEventClick,
        timeZone: 'Asia/Manila',
          datesSet: this.handleDatesSet
      },
      isSidebarOpen: false,
      isModalOpen: false,
      selectedEvent: null,
      eventTitle: '',
      eventDate: '',
      eventVenue: '',
      eventStartTime: '',
      eventEndTime: '',
        apiBaseUrl: 'http://127.0.0.1:5001',
        bookedEvents: [],
        error: null,
        isLoading: false,
        initialDateSet: false,
        // Availability management
        sidebarMode: 'event',
        availabilityDate: '',
        availabilityStatus: 'false',
        availabilityReason: '',
        supplierAvailability: [],
        // Snackbar for notifications
        snackbar: {
          show: false,
          message: '',
          type: 'success' // 'success' or 'error'
        }
      };
    },
    mounted() {
      // Store a reference to the calendar API
      this.$nextTick(() => {
        if (this.$refs.fullCalendar) {
          this.calendarApi = this.$refs.fullCalendar.getApi();
        }
      });
    },
    async created() {
      await this.fetchSupplierBookings();
      await this.fetchSupplierAvailability();
  },
  methods: {
      async fetchSupplierBookings() {
        this.isLoading = true;
        this.error = null;
        try {
          const token = localStorage.getItem('access_token');
          if (!token) {
            this.error = 'Please log in to view your schedule';
            return;
          }

          const response = await fetch(`${this.apiBaseUrl}/api/supplier/events`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          
          if (response.status === 403) {
            this.error = 'Unable to access supplier schedule data';
            return;
          }

          if (!response.ok) {
            throw new Error(`Failed to fetch schedules: ${response.status} ${response.statusText}`);
          }

          // Parse response
          const responseText = await response.text();
          
          let result;
          try {
            result = JSON.parse(responseText);
          } catch (e) {
            throw new Error('Invalid response format from server');
          }

          if (result.status === 'success' && Array.isArray(result.data)) {
            this.bookedEvents = result.data;
            

            
            // Transform the data into FullCalendar event format
            const events = result.data.map(booking => ({
              id: booking.events_id,
              title: `${booking.event_name || 'Untitled'} - ${booking.event_type || 'No Type'}`,
              start: `${booking.schedule}T${booking.start_time || '00:00:00'}`,
              end: `${booking.schedule}T${booking.end_time || '23:59:59'}`,
              extendedProps: {
                eventId: booking.events_id,
                eventName: booking.event_name,
                eventType: booking.event_type,
                eventTheme: booking.event_theme,
                eventColor: booking.event_color,
                status: booking.booking_status,
                packageName: booking.package_name,
                venueStatus: booking.venue_status,
                clientInfo: {
                  firstName: booking.client_firstname,
                  lastName: booking.client_lastname,
                  contact: booking.client_contact,
                  address: booking.client_address
                },
                totalPrice: booking.supplier_price,
                bookingType: booking.booking_type,
                supplierInfo: {
                  service: booking.supplier_service,
                  username: booking.supplier_username
                },
                venueInfo: {
                  name: booking.venue_name,
                  location: booking.venue_location,
                  price: booking.booked_venue_price || booking.venue_price,
                  capacity: booking.venue_capacity,
                  description: booking.venue_description,
                  image: booking.venue_image
                },
                bookingRemarks: booking.booking_remarks,
                isUpcoming: booking.is_upcoming
              },
              backgroundColor: booking.booking_status === 'Approved' ? '#4CAF50' : '#FFA726',
              borderColor: booking.booking_status === 'Approved' ? '#388E3C' : '#FB8C00'
            }));

            // Update the calendar events
            this.calendarOptions.events = events;
            
            // Set calendar to earliest event month
            this.$nextTick(() => {
              this.setInitialCalendarDate(events);
              // Update with availability data after calendar is ready
              this.updateCalendarWithAvailability();
            });
          } else {
            throw new Error(result.message || 'Failed to fetch events');
          }
        } catch (error) {
          this.error = 'Failed to load your schedule. Please try again later.';
        } finally {
          this.isLoading = false;
        }
      },
      
      handleDatesSet(dateInfo) {
        // Calendar dates set callback
      },

      // New method to set the initial calendar date
      setInitialCalendarDate(events) {
        if (!events || events.length === 0) {
          // If no events, use current month
          return;
        }
        
        try {
          // Sort events by start date
          const sortedEvents = [...events].sort((a, b) => {
            return new Date(a.start) - new Date(b.start);
          });
          
          // Get the earliest event date
          const earliestEvent = sortedEvents[0];
          const earliestDate = new Date(earliestEvent.start);
          
          // Try different approaches to set the calendar date
          // 1. Direct API access if available
          if (this.$refs.fullCalendar) {
            try {
              const calendarApi = this.$refs.fullCalendar.getApi();
              calendarApi.gotoDate(earliestDate);
              return;
            } catch (e) {
              // Error using ref API
            }
          }
          
          // 2. Use this.calendarApi if available
          if (this.calendarApi) {
            try {
              this.calendarApi.gotoDate(earliestDate);
              return;
            } catch (e) {
              // Error using stored API
            }
          }
          
          // 3. Last resort - try to find the API in the DOM
          setTimeout(() => {
            try {
              // Try to locate the calendar API
              if (this.$el) {
                const calendarEl = this.$el.querySelector('.fc');
                if (calendarEl && calendarEl.__vueParentComponent && 
                    calendarEl.__vueParentComponent.component && 
                    calendarEl.__vueParentComponent.component.proxy && 
                    calendarEl.__vueParentComponent.component.proxy.getApi) {
                  
                  const api = calendarEl.__vueParentComponent.component.proxy.getApi();
                  api.gotoDate(earliestDate);
                } else {
                  // Could not find calendar API in DOM
                }
              }
            } catch (e) {
              // Error in setTimeout approach
            }
          }, 500);
        } catch (error) {
          // Error setting initial calendar date
        }
      },

    toggleSidebar() {
      this.isSidebarOpen = !this.isSidebarOpen;
    },

      async addEvent() {
      if (this.eventTitle && this.eventDate && this.eventVenue && this.eventStartTime && this.eventEndTime) {
          try {
            const token = localStorage.getItem('access_token');
            if (!token) {
              return;
            }

            const eventData = {
              event_name: this.eventTitle,
          venue: this.eventVenue,
              schedule: this.eventDate,
              start_time: this.eventStartTime,
              end_time: this.eventEndTime,
              status: 'pending'
            };

            const response = await fetch(`${this.apiBaseUrl}/events`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
              },
              body: JSON.stringify(eventData)
            });

            if (!response.ok) {
              throw new Error('Failed to add event');
            }

            // Refresh the calendar events
            await this.fetchSupplierBookings();
        
        // Reset form fields
        this.eventTitle = ''; 
        this.eventDate = '';
        this.eventVenue = '';
        this.eventStartTime = '';
        this.eventEndTime = '';
        
        this.toggleSidebar(); // Close the sidebar after adding
          } catch (error) {
            // Error adding event
          }
      }
    },

    renderEvent(eventInfo) {
        const event = eventInfo.event;
        const props = event.extendedProps;
  
      const element = document.createElement('div');
        element.className = 'p-2 rounded-lg';
        element.style.backgroundColor = event.backgroundColor;
        
        const titleElement = document.createElement('div');
        titleElement.className = 'font-semibold text-white';
        titleElement.innerText = event.title;
        
        const statusElement = document.createElement('div');
        statusElement.className = 'text-xs text-white mt-1';
        statusElement.innerText = `Status: ${props.status}`;

        const typeElement = document.createElement('div');
        typeElement.className = 'text-xs text-white';
        typeElement.innerText = props.eventType || 'No Type';
        
        element.appendChild(titleElement);
        element.appendChild(typeElement);
        element.appendChild(statusElement);

        return { domNodes: [element] };
    },

    handleEventClick(info) {
        this.selectedEvent = info.event;
        
        // Check if it's an availability event
        if (info.event.extendedProps.type === 'availability') {
          this.handleAvailabilityEventClick(info.event);
        } else {
          this.isModalOpen = true;
        }
    },

    handleAvailabilityEventClick(event) {
      // Show confirmation dialog for removing availability
      if (confirm(`Remove unavailability for ${event.extendedProps.date}?${event.extendedProps.reason ? `\nReason: ${event.extendedProps.reason}` : ''}`)) {
        this.removeAvailability(event.extendedProps.date);
      }
    },

    editAvailabilityEvent(event) {
      // Pre-fill the form with existing availability data
      this.availabilityDate = event.extendedProps.date;
      this.availabilityStatus = 'true'; // Mark as available to remove
      this.availabilityReason = event.extendedProps.reason || '';
      this.sidebarMode = 'availability';
      this.isSidebarOpen = true;
    },

    closeModal() {
        this.isModalOpen = false;
    },

    editEvent() {
      if (this.selectedEvent) {
        this.eventTitle = this.selectedEvent.title;
          this.eventDate = this.selectedEvent.start.toISOString().split('T')[0];
        this.eventVenue = this.selectedEvent.extendedProps.venue;
          this.eventStartTime = this.selectedEvent.start.toTimeString().split(' ')[0];
          this.eventEndTime = this.selectedEvent.end.toTimeString().split(' ')[0];
          this.isModalOpen = false;
          this.toggleSidebar();
      }
    },

    deleteEvent() {
      if (this.selectedEvent) {
          // Add delete functionality here when backend endpoint is ready
          this.isModalOpen = false;
      }
    },

    // Availability management methods
    setSidebarMode(mode) {
      this.sidebarMode = mode;
      // Clear form when switching modes
      if (mode === 'availability') {
        this.availabilityDate = '';
        this.availabilityStatus = 'false';
        this.availabilityReason = '';
      }
    },

    async fetchSupplierAvailability() {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          return;
        }

        const response = await fetch(`${this.apiBaseUrl}/api/supplier/availability`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          return;
        }

        const result = await response.json();
        
        if (result.status === 'success') {
          this.supplierAvailability = result.data;
          
          // Wait for next tick to ensure calendar is mounted
          this.$nextTick(() => {
            this.updateCalendarWithAvailability();
          });
        }
              } catch (error) {
          // Error fetching supplier availability
        }
    },

    async setAvailability() {
      if (!this.availabilityDate) {
        this.showSnackbar('Please select a date', 'error');
        return;
      }

      // Check if date is already marked as unavailable
      const existingAvailability = this.supplierAvailability.find(
        avail => avail.date === this.availabilityDate && !avail.is_available
      );
      
      if (existingAvailability && this.availabilityStatus === 'false') {
        this.showSnackbar('This date is already marked as unavailable', 'error');
        return;
      }

      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          this.error = 'Please log in to manage availability';
          return;
        }

        const availabilityData = {
          date: this.availabilityDate,
          is_available: this.availabilityStatus === 'true',
          reason: this.availabilityReason || null
        };

        const response = await fetch(`${this.apiBaseUrl}/api/supplier/availability`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(availabilityData)
        });

        if (!response.ok) {
          throw new Error('Failed to update availability');
        }

        // Refresh availability data
        await this.fetchSupplierAvailability();
        
        // Reset form
        this.availabilityDate = '';
        this.availabilityStatus = 'false';
        this.availabilityReason = '';
        
        // Show success message
        this.error = null;
        this.showSnackbar('Availability updated successfully', 'success');
      } catch (error) {
        this.showSnackbar('Failed to update availability. Please try again.', 'error');
      }
    },

    updateCalendarWithAvailability() {
      // Get the calendar API
      const calendarApi = this.$refs.fullCalendar?.getApi();
      if (!calendarApi) {
        return;
      }

      // Remove existing availability events first
      const existingEvents = calendarApi.getEvents();
      existingEvents.forEach(event => {
        if (event.extendedProps?.type === 'availability') {
          event.remove();
        }
      });

      // Add availability events to calendar
      const availabilityEvents = this.supplierAvailability
        .filter(avail => !avail.is_available)
        .map(avail => {
          // Convert date format from "Fri, 11 Jul 2025 00:00:00 GMT" to "2025-07-11"
          let formattedDate = avail.date;
          if (avail.date && typeof avail.date === 'string') {
            try {
              const dateObj = new Date(avail.date);
              formattedDate = dateObj.toISOString().split('T')[0]; // YYYY-MM-DD format
            } catch (error) {
              formattedDate = avail.date;
            }
          }
          
          return {
            id: `availability-${avail.availability_id}`,
            title: avail.reason ? `Unavailable - ${avail.reason}` : 'Unavailable',
            start: formattedDate,
            end: formattedDate,
            allDay: true,
            backgroundColor: '#dc2626', // Red color for unavailable
            borderColor: '#b91c1c',
            extendedProps: {
              type: 'availability',
              availabilityId: avail.availability_id,
              reason: avail.reason,
              isAvailable: false,
              date: formattedDate
            }
          };
        });

      // Add events to calendar using API
      availabilityEvents.forEach(eventData => {
        calendarApi.addEvent(eventData);
      });
    },

    handleDateClick(info) {
      // Set the clicked date in the availability form
      this.availabilityDate = info.dateStr;
      this.sidebarMode = 'availability';
      this.isSidebarOpen = true;
    },

    openAvailabilitySidebar() {
      this.sidebarMode = 'availability';
      this.isSidebarOpen = true;
    },

    async removeAvailability(date) {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) {
          this.error = 'Please log in to manage availability';
          return;
        }

        const response = await fetch(`${this.apiBaseUrl}/api/supplier/availability/${date}`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          throw new Error('Failed to remove availability');
        }

        const result = await response.json();
        
        if (result.status === 'success') {
          // Refresh availability data
          await this.fetchSupplierAvailability();
          
          // Show success message
          this.error = null;
          this.showSnackbar('Availability removed successfully', 'success');
        } else {
          throw new Error(result.message || 'Failed to remove availability');
        }
      } catch (error) {
        this.showSnackbar('Failed to remove availability. Please try again.', 'error');
      }
    },



    // Snackbar methods
    showSnackbar(message, type = 'success') {
      this.snackbar = {
        show: true,
        message,
        type
      };
      
      // Auto-hide after 3 seconds
      setTimeout(() => {
        this.hideSnackbar();
      }, 3000);
    },

    hideSnackbar() {
      this.snackbar.show = false;
    },
  },
  }
  </script> 
  <style scoped>
  .custom-shadow {
    box-shadow: 1px 0 8px rgba(0, 0, 0, 0.2); 
  }
  
  </style>