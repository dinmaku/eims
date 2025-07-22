<template>
    <div class="h-full overflow-y-auto overflow-x-hidden">
      <!-- Header with responsive layout -->
      <div class="flex justify-between items-center w-full h-20 bg-gray-100 shadow-lg antialiased mt-28 px-4 sm:px-6 lg:px-8">
        <h1 class="flex font-medium font-amaticBold text-2xl ml-5 sm:text-xl">My Booked Schedule</h1>
      </div>
  
      <!-- Sidebar (will slide in/out based on isSidebarOpen) -->
      <aside class="fixed top-0 right-0 w-full md:w-[450px] h-full bg-[#f8f9ef] shadow-lg transition-transform z-50 custom-shadow" :class="isSidebarOpen ? 'translate-x-0' : 'translate-x-full'">
        <div class="p-4">
          <div class="flex items-center">
            <button @click="toggleSidebar" class="px-3 h-8 text-md bg-gray-200 font-bold rounded-full transform-transition duration-300 transform hover:scale-110">X</button>
          </div>
          <h2 class="text-xl font-semibold">Schedule Event</h2>
          <p class="mb-10 text-base text-gray-500">Capture your upcoming events in one place.</p>
  
          <form @submit.prevent="addEvent">
            <div class="mt-8 ml-2">
              <div class="flex items-center">
                <label for="event-title" class="block text-md font-semibold text-gray-700 mr-2 font-raleway">Event Name: </label>
                <input type="text" class="h-8 w-full sm:w-56 rounded-lg shadow-md text-sm" id="eventTitle" v-model="eventTitle" required />
              </div>
            </div>
            <div class="mt-8 ml-2">
              <div class="flex items-center">
                <label for="event-title" class="block text-md font-semibold text-gray-700 mr-2 font-raleway">Venue: </label>
                <input type="text" class="h-8 w-full sm:w-56 rounded-lg shadow-md text-sm" id="eventVenue" v-model="eventVenue" required />
              </div>
            </div>
            <div class="mt-8 ml-2">
              <div class="flex items-center">
                <label for="event-title" class="block text-md font-semibold text-gray-700 mr-3 font-raleway">Date: </label>
                <input type="date" class="h-8 w-full sm:w-56 rounded-lg shadow-md text-sm" id="eventDate" v-model="eventDate" required />
              </div>
            </div>
            <div class="mt-12 ml-2">
              <div class="flex items-center">
                <label for="event-title" class="block text-md font-semibold text-gray-700 mr-3 font-raleway">Start Time: </label>
                <input type="time" class="h-8 w-full sm:w-56 rounded-lg shadow-md text-sm" id="startTime" v-model="eventStartTime" required />
              </div>
            </div>
            <div class="mt-4 ml-2">
              <div class="flex items-center">
                <label for="event-title" class="block text-md font-semibold text-gray-700 mr-3 font-raleway">End Time: </label>
                <input type="time" class="h-8 w-full sm:w-56 rounded-lg shadow-md text-sm" id="endTime" v-model="eventEndTime" required />
              </div>
            </div>
  
            <div class="mt-10">
              <button type="submit" class="h-10 bg-blue-400 text-md font-bold px-2 rounded-lg shadow-lg w-full sm:w-auto">
                Set Schedule
              </button>
            </div>
          </form>
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
        initialDateSet: false
      };
    },
    mounted() {
      // Store a reference to the calendar API
      this.$nextTick(() => {
        if (this.$refs.fullCalendar) {
          this.calendarApi = this.$refs.fullCalendar.getApi();
          console.log('Calendar API reference obtained');
        }
      });
    },
    async created() {
      await this.fetchSupplierBookings();
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

          // Directly fetch the supplier's events with better error logging
          console.log('Fetching supplier events...');
          
          const response = await fetch(`${this.apiBaseUrl}/api/supplier/events`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });

          // Log the response status
          console.log('Response status:', response.status);
          
          if (response.status === 403) {
            console.error('403 Forbidden response received');
            this.error = 'Unable to access supplier schedule data';
            return;
          }

          if (!response.ok) {
            console.error('Error response', response.status, response.statusText);
            throw new Error(`Failed to fetch schedules: ${response.status} ${response.statusText}`);
          }

          // Parse response
          const responseText = await response.text();
          console.log('Raw response:', responseText);
          
          let result;
          try {
            result = JSON.parse(responseText);
          } catch (e) {
            console.error('Failed to parse JSON response:', e);
            throw new Error('Invalid response format from server');
          }

          console.log('Supplier Events:', result);

          if (result.status === 'success' && Array.isArray(result.data)) {
            this.bookedEvents = result.data;
            
            if (result.data.length === 0) {
              console.log('No booked events found for this supplier');
            } else {
              console.log(`Found ${result.data.length} supplier events`);
              
              // Log the first event date to debug
              if (result.data[0] && result.data[0].schedule) {
                console.log('First event date:', result.data[0].schedule);
              }
            }
            
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
            console.log('Calendar events updated:', events.length);
            
            // Set calendar to earliest event month
            this.$nextTick(() => {
              this.setInitialCalendarDate(events);
            });
          } else {
            console.error('Invalid response format:', result);
            throw new Error(result.message || 'Failed to fetch events');
          }
        } catch (error) {
          console.error('Error fetching booked schedules:', error);
          this.error = 'Failed to load your schedule. Please try again later.';
        } finally {
          this.isLoading = false;
        }
      },
      
      handleDatesSet(dateInfo) {
        console.log('Calendar dates set:', dateInfo);
      },

      // New method to set the initial calendar date
      setInitialCalendarDate(events) {
        if (!events || events.length === 0) {
          // If no events, use current month
          console.log('No events found, using current month');
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
          
          console.log('Earliest event date:', earliestDate.toISOString().slice(0, 10));
          
          // Try different approaches to set the calendar date
          // 1. Direct API access if available
          if (this.$refs.fullCalendar) {
            try {
              const calendarApi = this.$refs.fullCalendar.getApi();
              calendarApi.gotoDate(earliestDate);
              console.log('Calendar date set via ref API');
              return;
            } catch (e) {
              console.error('Error using ref API:', e);
            }
          }
          
          // 2. Use this.calendarApi if available
          if (this.calendarApi) {
            try {
              this.calendarApi.gotoDate(earliestDate);
              console.log('Calendar date set via stored API');
              return;
            } catch (e) {
              console.error('Error using stored API:', e);
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
                  console.log('Calendar date set via DOM lookup');
                } else {
                  console.warn('Could not find calendar API in DOM');
                }
              }
            } catch (e) {
              console.error('Error in setTimeout approach:', e);
            }
          }, 500);
        } catch (error) {
          console.error('Error setting initial calendar date:', error);
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
              console.error('No access token found');
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
            console.error('Error adding event:', error);
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
        this.isModalOpen = true;
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
  },
  }
  </script> 
  <style scoped>
  .custom-shadow {
    box-shadow: 1px 0 8px rgba(0, 0, 0, 0.2); 
  }
  
  </style>